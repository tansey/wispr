import os
import base64

import urllib
import urllib2
import json

url = 'http://localhost:5000/upload_geoaudio'

all_files = [
    {'latitude': 30.3, 'longitude': -97.74, 'filename': 'test.m4a'}
]

for geosound in all_files:
    s = open(geosound['filename'], 'r').read()
    enc = base64.b64encode(s)

    values = {'latitude': geosound['latitude'],
          'longitude': geosound['longitude'],
          'whisper':  "test"}

    json_data = json.dumps(values)

    post_data = json_data.encode('utf-8')

    headers = {}
    headers['Content-Type'] = 'application/json'

    # now do the request for a url
    req = urllib.request.Request(url, post_data, headers)

    # send the request
    res = urllib.request.urlopen(req)

    print 'Sent ' + geosound['filename']
    print res.read()
