function handleNoGeolocation(errorFlag, map) {
        if (errorFlag) {
          var content = 'Error: The Geolocation service failed.';
        } else {
          var content = 'Error: Your browser doesn\'t support geolocation.';
        }

        var options = {
          map: map,
          position: new google.maps.LatLng(30.16, -97.44),
          content: content
        };

        var infowindow = new google.maps.InfoWindow(options);
        map.setCenter(options.position);
}


var styles = [
      {
          stylers: [
            { hue: "#00ffe6" },
            { saturation: -20 }
          ]
        },{
          featureType: "road",
          elementType: "geometry",
          stylers: [
            { lightness: 100 },
            { visibility: "simplified" }
          ]
        },{
          featureType: "road",
          elementType: "labels",
          stylers: [
            { visibility: "off" }
          ]
        }
      ];

function attachMessage(marker, path, boxes) {
       var boxText = document.createElement("div");
        boxText.style.cssText = "margin-top: 2px; background: #8FC4BC; padding: 2px; border-radius: 70px;";

       boxText.innerHTML ='<iframe width="250" height="250" src="' + path + '" frameborder="0" allowfullscreen></iframe>';

        var myOptions = {
                 content: boxText
                ,disableAutoPan: false
                ,maxWidth: 0
                ,pixelOffset: new google.maps.Size(-140, 0)
                ,zIndex: null
                ,boxStyle: { 
                  opacity: 1
                 }
                ,closeBoxMargin: "2px 2px 2px 2px"
                ,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
                ,infoBoxClearance: new google.maps.Size(1, 1)
                ,isHidden: false
                ,pane: "floatPane"
                ,enableEventPropagation: false
        };

        var ib = new InfoBox(myOptions);
        boxes.push(ib);
        google.maps.event.addListener(marker, 'click', function() {
          ib.open(marker.get('map'), marker);
        });
}

function clearOverlays(marray) {
  for (var i = 0; i < marray.length; i++ ) {

    marray[i].setMap(null);

  }
  marray = [];
}

function addClosingOthers(markers, boxes){
   for (var i = 0; i < markers.length; i++) {
      marker = markers[i];
      google.maps.event.addListener(marker, 'click', function() {
    // reference clicked marker
    var curMarker =  this;
    // loop through all markers
    $.each(boxes, function(index, box) {
        // if marker is not the clicked marker, close the marker
        if(markers[index] !== curMarker) {
            box.close();
        }
    });
  });
}
}