import os
import datetime
from flask import Flask
from flask import g
from flask import jsonify
from flask import json
from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask import make_response
from werkzeug import secure_filename
import pymongo
from pymongo import Connection, GEO2D
from bson import BSON
from bson import json_util
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import uuid
import random

app = Flask(__name__)

def mongo_conn():
    if os.environ.get('MONGOHQ_URL'):
        return Connection(os.environ['MONGOHQ_URL'])
    else:
        return Connection()


@app.route('/test', methods=['GET'])
def test_data():
    # Test method to populate the DB
    return render_template("test.html")    

@app.route('/', methods=['GET'])
def hello():
    # Audio streetview page
    return render_template("index.html", google_maps_key=os.environ['GOOGLE_MAPS_KEY'])

@app.route('/upload_geoaudio', methods=['POST'])
def upload_geoaudio():
    # API point for uploading geo-tagged sound clips.
    connection = mongo_conn()

    db = connection[os.environ['MONGODB_NAME']]

    audio = request.json['audio']

    # Save the audio to S3
    conn = S3Connection(os.environ['AWS_S3_KEY'], os.environ['AWS_S3_SECRET'])
    bucket = conn.create_bucket(os.environ['AWS_S3_BUCKET'])
    k = Key(bucket)
    k.key = str(uuid.uuid4())
    k.set_metadata("Content-Type", 'audio/aac')
    k.set_contents_from_string(audio)

    # Get the geolocation data
    geoaudioData = {
        "loc": [float(request.json['longitude']), float(request.json['latitude'])],
        "s3_key": k.key
    }

    # Get the collection
    geoaudio = db.geoaudio

    # Insert it into the db
    geoaudio.insert(geoaudioData)

    # Return success
    return jsonify(result="Success")
    
@app.route('/near_points', methods=['POST'])
def near_points():
    # Find 50 nearest sounds to a given lat/long.
    latitude = float(request.json['latitude'])
    longitude = float(request.json['longitude'])
    connection = mongo_conn()
    db = connection[os.environ['MONGODB_NAME']]
    geoaudio = db.geoaudio
    near = geoaudio.find({"loc": {"$near": [latitude, longitude]}}).limit(50)
    results = [{'lat': doc['loc'][0], 'lng': doc['loc'][1], 'link': ('/sounds/' + doc['s3_key'])} for doc in near]
    return jsonify(items=results)

@app.route('/sounds/<filename>', methods=['GET'])
def play_sound(filename):
    # Renders the iframe with the play button and sound file
    return render_template('player.html', filename=filename)
    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
