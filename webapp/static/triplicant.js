/*
*triplicant.js
*javascript used in triplicant web app
*Mark Lubin
*/

START = true;
END = false;
DEFAULT_DETOUR = 1.5;

var map,mapOptions;
var markers;
var locations = Array();
var start = '';
var end = '';
var inputMode = null;
var tripPath;
var mapLine;
var spinner = null;
var cost = '';
var score = '';
var startAC,endAC;
var startLatLng,endLatLng;
var geocoder;
var bounds;

function initialize() {
//set up google places autocomplete for inputs
    var autocompleteSettings = {
      types: ['(cities)']
    };

    startAC = new google.maps.places.Autocomplete(document.getElementById('start'),autocompleteSettings);
    endAC = new google.maps.places.Autocomplete(document.getElementById('end'),autocompleteSettings);

    //set up tabs and according 
    $('#tabs').tabs();
    $('.accordion').accordion();
    $('#detour_slider').slider({
      min: 0,
      max: 10
    });

    //set up buttons 
    $('#clear').bind('click',function(){
        $('#start').value = '';
        $('#end').value = '';
        start = '';
        end = '';
        tripPath = null;
        if(mapLine){
          mapLine.setMap(null);
          mapLine = null;
        }
        clearMarkers();

    });
    $('#route').bind('click',getStartLatLng);


    //set up map and geocoder

    geocoder = new google.maps.Geocoder();

    mapOptions = {
      center: new google.maps.LatLng(20,0),
      zoom: 2,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
   	map = new google.maps.Map(document.getElementById("map_canvas"),
        mapOptions);
};


function createMarker(location){
    var marker = new google.maps.Marker({       
        position: location, 
        map: map,  // google.maps.Map 
        draggable: false,
        clickable: true   
    }); 
   /* google.maps.event.addListener(marker, 'click', function() { 
      markerClicked(marker.position); 
    }); */
    markers.push(marker)//add to array of markers
}


function getRoute(){
  if(mapLine != null){
    mapLine.setMap(null);
    mapLine = null;
  }

  //clear markers and get a new set ready
  clearMarkers();
  markers = Array();

  var value = $( "#detour_slider" ).slider( "option", "value" )/10.0;//get detour slider value
  
  tripPath = Array() //hold the new trip
  bounds = new google.maps.LatLngBounds();//set up bounds

  startSpinner();//ajax spinner

  //make the ajax request
  $.getJSON($SCRIPT_ROOT + "_getRoute",{
    start_lat : startLatLng.lat(),
    start_lng : startLatLng.lng(),
    end_lat : endLatLng.lat(),
    end_lng : endLatLng.lng(),
    detour : value
  }, function(data){//callback to get response, stop spinner and show route
    score = data['score'];
    cost = data['cost'];
    $.each(data['path'],function(){//construct the path and set up markers
      var latLng = new google.maps.LatLng(this[0],this[1])
      createMarker(latLng);//set up a marker
      tripPath.push(latLng);//map path 
      bounds.extend(latLng);
    });
  if(spinner != null){//remove the spinner
    spinner.stop();
    spinner = null;
  }
  displayPath();//actually display polyline
  });
}

function displayPath(){
  //swap in the information div
 // $('#get_started').hide()
  //$('#info').show()

  //update stats
  $('#score').html(score);
  $('#cost').html(cost);

  mapLine = new google.maps.Polyline({
    path: tripPath,
    strokeColor: "#0000FF",
    strokeWeight: 4,
    strokeOpacity: 1.0,
    map: map
  });

  //set the bounds and pan
  map.fitBounds(bounds);

}

function markerClicked(marker_id){
  if(inputMode == START){
    $('#start').html(locations[marker_id]);
    start = marker_id
  }
  else if(inputMode == END){
    $('#end').html(locations[marker_id]);
    end = marker_id
  }
  
}

function getStartLatLng(){
  
  //reset values 
  startLatLng = 0;
  endLatLng = 0;
  
  //get input values
  var sname = $('#start').val();

  //try start addr
  geocoder.geocode({'address': sname },function(results,status){
   if (status == google.maps.GeocoderStatus.OK) {
      startLatLng = results[0].geometry.location;
      getEndLatLng();
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });

}

function getEndLatLng(){

var ename = $('#end').val();

 //try end addr and call getRoute on success
  geocoder.geocode({'address': ename },function(results,status){
   if (status == google.maps.GeocoderStatus.OK) {
      endLatLng = results[0].geometry.location;
      getRoute();
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}


//remove all markers from map
function clearMarkers(){
  if(!markers){
    return; //nothing to do
  }
  for (var i = 0; i < markers.length; i++ ) {
    if(markers[i]){//no real marker
      markers[i].setMap(null);
    }
  }

}

function startSpinner(){
  var opts = {
  lines: 13, // The number of lines to draw
  length: 30, // The length of each line
  width: 19, // The line thickness
  radius: 40, // The radius of the inner circle
  corners: 1, // Corner roundness (0..1)
  rotate: 45, // The rotation offset
  color: '#000', // #rgb or #rrggbb
  speed: 1.6, // Rounds per second
  trail: 62, // Afterglow percentage
  shadow: true, // Whether to render a shadow
  hwaccel: false, // Whether to use hardware acceleration
  className: 'spinner', // The CSS class to assign to the spinner
  zIndex: 2e9, // The z-index (defaults to 2000000000)
  top: 'auto', // Top position relative to parent in px
  left: 'auto' // Left position relative to parent in px
  };
  var target = document.getElementById('map_canvas');
  spinner = new Spinner(opts).spin(target);
}

$(document).ready(initialize);