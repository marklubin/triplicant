/*
*triplicant.js
*javascript used in triplicant web app
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
var inputMode = null;
var tripPath;
var mapLine;
var spinner = null;
var cost = '';
var score = '';

function initialize() {
    $('#detour_slider').slider({
      min: 0,
      max: 10
    });
    $('#clear').bind('click',function(){
        $('#start').html('');
        $('#end').html('');
        inputMode = null;
        start = '';
        end = '';
        tripPath = null;
        if(mapLine){
          mapLine.setMap(null);
          mapLine = null;
        }

    });
    $('#start').bind('click',startClicked);
    $('#end').bind('click',endClicked);
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
  startSpinner();
  var value = $( "#detour_slider" ).slider( "option", "value" )/10.0;
  tripPath = Array()
  $.getJSON($SCRIPT_ROOT + "_getRoute",{
    start_id : start,
    end_id : end,
    detour : value
  }, function(data){
    score = data['score'];
    cost = data['cost'];
    $.each(data['path'],function(){
      latLng = new google.maps.LatLng(this[0],this[1])
      tripPath.push(latLng);
    });
  if(spinner != null){//remove the spinner
    spinner.stop();
    spinner = null;
  }
  displayPath();
  });
}

function displayPath(){
  $('#score').html(score);
  $('#cost').html(cost);

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
  }
  else if(inputMode == END){
    $('#end').html(locations[marker_id]);
    end = marker_id
  }
  
}

function startClicked(){
  inputMode = START;
  $('#start').addClass('loc_selected');
  $('#end').removeClass('loc_selected');

}

function endClicked(){
  inputMode = END;
  $('#end').addClass('loc_selected');
  $('#start').removeClass('loc_selected');

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

$(document).ready(function(){
	initialize();
});
