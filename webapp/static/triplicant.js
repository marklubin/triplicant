/*
*triplicant.js
*jquery functions used in triplicant web app
*Mark Lubin
*/

START = true;
END = false;
DEFAULT_DETOUR = 1.5;

var map,mapOptions;
var markers = Array();
var locations = Array();
var start = '';
var end = '';
var inputMode = START
var tripPath;
var mapLine;

function initialize() {
    $('#clear').bind('click',function(){
        $('#start').html('');
        $('#end').html('');
        inputMode = START;
        start = '';
        end = '';
        tripPath = null;
        if(mapLine){
          mapLine.setMap(null);
          mapLine = null;
        }

    });
    $('#route').bind('click',getRoute);
    mapOptions = {
      center: new google.maps.LatLng(20,0),
      zoom: 2,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
   	map = new google.maps.Map(document.getElementById("map_canvas"),
        mapOptions);
   	$.getJSON($SCRIPT_ROOT + "/_init",function(data){
   		$.each(data,function(index){
        locations[this['id']] = this['name'];
        latLng = new google.maps.LatLng(this['latitude'],
                                        this['longitude']);
        marker = createMarker(this)
        markers.push(marker);
   		});
   	});
};
function createMarker(location){
    latLng = new google.maps.LatLng(location['latitude'],
                                        location['longitude']);
    var marker = new google.maps.Marker({       
        position: latLng, 
        map: map,  // google.maps.Map 
        draggable: false,
        clickable: true,
        title: location['id'].toString()      
    }); 
    google.maps.event.addListener(marker, 'click', function() { 
      markerClicked(marker.title); 
    }); 
    return marker;  
}

function getRoute(){
  if(start == '' || end == ''){
    alert("Please enter both a start and end point");
    return;
  }
  if(mapLine != null){
    mapLine.setMap(null);
    mapLine = null;
  }
  tripPath = Array()
  $.getJSON($SCRIPT_ROOT + "_getRoute",{
    start_id : start,
    end_id : end,
    detour : DEFAULT_DETOUR
  }, function(data){
    $.each(data,function(){
      latLng = new google.maps.LatLng(this[0],this[1])
      tripPath.push(latLng);
    });
  displayPath();
  });
}

function displayPath(){
  mapLine = new google.maps.Polyline({
    path: tripPath,
    strokeColor: "#0000FF",
    strokeWeight: 4,
    strokeOpacity: 1.0,
    map: map
  });
}

function markerClicked(marker_id){
  if(inputMode == START){
    $('#start').html(locations[marker_id]);
    start = marker_id
    inputMode = END
  }
  else{
    $('#end').html(locations[marker_id]);
    end = marker_id
  }
  

}

$(document).ready(function(){
	initialize();
});
