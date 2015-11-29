var map;

function initialize() {
    // var styles = [{"featureType":"landscape","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","stylers":[{"saturation":-100},{"lightness":51},{"visibility":"simplified"}]},{"featureType":"road.highway","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"road.arterial","stylers":[{"saturation":-100},{"lightness":30},{"visibility":"on"}]},{"featureType":"road.local","stylers":[{"saturation":-100},{"lightness":40},{"visibility":"on"}]},{"featureType":"transit","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"administrative.province","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"labels","stylers":[{"visibility":"on"},{"lightness":-25},{"saturation":-100}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]}];
    var sanFrancisco = { lat: 37.7833, lng: -122.4167 };
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 10,
        center: sanFrancisco
    });
    // map.setOptions({styles, styles});
    return map;
}



(function () {

    var infoWindow = new google.maps.InfoWindow({
      width: 150
    });
    var circles = [];
    var markers = [];

    function getHtml(logged_in, population, location, long_profile_list, short_profile_list, count, adjective){
        if (logged_in==="True"){

            html =
                '<div id="content"><div id="content-first">' +
                '<p>There are <b>' + population + '</b> profiles in ' + location + '<br>matching your search</p>'+
                '<button type="button" class="btn btn-primary btn-sm" '+
                    'data-toggle="modal" data-target="#myModal" '+
                    'data-recipients="'+ long_profile_list +'">'+
                    'Message Profiles in '+ location +'</button></div>'+
                '<p>The most commonly used adjective is <b>' + adjective + '</b>'+
                '<br>('+count+' occurences)</p>'+
                '<button type="button" class="btn btn-primary btn-sm" '+
                    'data-toggle="modal" data-target="#myModal"'+
                    'data-recipients="'+short_profile_list +
                    '">Message Profiles with '+adjective+'</button></div>';
        }else{

            html =
                '<div id="content"><div id="content-first">'+
                '<p>There are <b>' + population + '</b> profiles in ' + location + '<br>matching your search</p>'+
                '<button type="button" class="btn btn-primary btn-sm" disabled>'+
                    'Login to Message Profiles in ' + location + '</button></div>' +
                '<p>The most commonly used adjective is <b>' + adjective + '</b>'+
                '<br>('+count+' occurences)<p>'+
                '<button type="button" class="btn btn-primary btn-sm" disabled>'+
                'Login to Message Profiles with ' + adjective + '</button></div>';
          }
        
        return html;

    }

    function removeAllCirclesAndMarkers() {
        for (var i = 0; i < circles.length; i++) {
            var circle = circles[i];
            circle.setMap(null);
        }
        for (var j = 0; j < markers.length; j++) {
            var marker = markers[j];
            marker.setMap(null);
        }
    }

    function createCircle(latitude, longitude, count){
        var cityCircle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            map: map,
            center: {lat: latitude, lng: longitude},
            radius: 500* Math.log(count)
        });
        return cityCircle;
    }

    function createMarker(latitude, longitude, adjective){
        var adjLength = adjective.length ;
        console.log("adj len is"+adjLength);
        marker = new MarkerWithLabel({
        position: {lat: latitude, lng: longitude},
        labelContent: adjective,
        map: map,
        labelClass: "labels",
        labelInBackground: false,
        labelAnchor: new google.maps.Point((adjLength+1)*3, 0),
        labelStyle: {opacity: 0.75},
        icon: '/static/img/heart-marker-transparent.png'
        // #TODO -- add animation to marker with label
        // animation: google.maps.Animation.DROP

        });
        return marker;
    }

    function bindInfoWindow(marker, map, infoWindow, html) {
        google.maps.event.addListener(marker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, marker);
            console.log("inside bind infos");

        });
    }

        // Adds a marker to the map.
        // have a key pointing to dictionary
        // have a key pointing to login
    function addMarkers(dictionary){
        removeAllCirclesAndMarkers();
        console.log("addMarkers");
        for (var entry in dictionary["results"]){
            var html, cityCircle, marker;
            var latitude = dictionary["results"][entry]['lat'];
            var longitude = dictionary["results"][entry]['lng'];
            var adjective = dictionary["results"][entry]['adj'];
            var count = dictionary["results"][entry]['count'];
            var population = dictionary["results"][entry]['population'];
            var location = dictionary["results"][entry]['location'];
            var short_profile_list = dictionary["results"][entry]['short_profile_list'];
            var long_profile_list = dictionary["results"][entry]['long_profile_list'];
            var logged_in = dictionary['logged_in'];

            html = getHtml(logged_in, population, location, long_profile_list,
                            short_profile_list, count, adjective);

            cityCircle = createCircle(latitude,longitude, count);
            circles.push(cityCircle);
            marker = createMarker(latitude, longitude, adjective);
            markers.push(marker);

            bindInfoWindow(marker, map, infoWindow, html);
        }

        $('#loading').hide();
        $('#loading-spin').hide();
        $("#form-submit").show();

        $("#form-submit").val("Submit");

    }


   


    // var bool=false;
    // function getCoordinates(bool){
    //     var NEprime;
    //     if(bool===true){
    //         google.maps.event.addListener(map, 'idle', function(){
    //         console.log("in event get coordinates listener");
    //         var NE= map.getBounds().getNorthEast().lat();
    //         console.log("NE IS"+NE);
    //         bool=false;
    //                     });
    //     }
    // }

//     setTimeout(function(){
//     map.getBounds().getNorthEast().lat();
//     map.getBounds().getSouthWest().lat();
//     map.getBounds().getNorthEast().lng();
//     map.getBounds().getSouthWest().lng();
// }, 1000);

    // google.maps.event.addDomListener(window, 'load', initialize);
        

    // $('#orientation-hover').tooltip();

    var ajaxRequest;
    function plotInputs(chart){
        var inputs = {
            "orientation": ($('input[name="orientation"]:checked').serialize()),
            "gender": ($('input[name="gender"]:checked').serialize()),
            "age": $("#age").val(),
            "minimum_latitude": chart.getBounds().getSouthWest().lat(),
            "maximum_latitude": chart.getBounds().getNorthEast().lat(),
            "minimum_longitude": chart.getBounds().getSouthWest().lng(),
            "maximum_longitude": chart.getBounds().getNorthEast().lng()
        };

            // var latitude_max = getBoundsObject.getNorthEast().lat();

        ajaxRequest = $.get("/map-checked.json", inputs, addMarkers);

    }
    // slider
    $(function() {
        $( "#map-slider-range" ).slider({
            range: true,
            min: 18,
            max: 98,
            values: [ 18, 30 ],
            slide: function( event, ui ) {
                $( "#age" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
                }
            });
        $( "#age" ).val( $( "#map-slider-range" ).slider( "values", 0 ) +
          " - " + $( "#map-slider-range" ).slider( "values", 1 ) );
    });


    $(' #map-choices-form').on('submit', function (event) {
        event.preventDefault();
        ajaxRequest.abort();
        event.stopPropagation();
        $('#loading').show();
        $('#loading-spin').show();
        $("#form-submit").hide();

        plotInputs(map);
    });



    //check all orientation checkboxes
    $("#check-all-orientation").change(function () {
        $("input[name='orientation']:checkbox").prop('checked', $(this).prop("checked"));
    });

    //check all gender checkboxes
    $("#check-all-gender").change(function () {
        $("input[name='gender']:checkbox").prop('checked', $(this).prop("checked"));
    });

    

    $('#myModal').on('shown.bs.modal', function (evt) {
        var recipients = $(evt.relatedTarget).data('recipients');
        recipients = recipients.replace(/,/g,", ");
        $("#add-recipients").html(recipients);
    });

    function sent(data){
        $("#sent").html("Sent!");
        $("#message-form").trigger("reset");

        $('#loading-2').hide();
    }

    function messageSubmission(evt){
        evt.preventDefault();

        $('#loading-2').show();

        var recipients = $("#add-recipients").html();
        var message = $("#message").val();

        var sendInputs = {
            "recipients": recipients,
            "message": message
        };

        $.post("/send-message.json", sendInputs, sent);
    }

    $("#message-form").on('submit', messageSubmission);


    $(document).ready(function() {
        $('#pageModal').modal();
        var chart = initialize();
        // plotInputs(chart);
        google.maps.event.addListenerOnce(map, 'bounds_changed', function() {
            plotInputs(chart);
        });

        google.maps.event.addListener(map, 'bounds_changed', function() {
        $("#form-submit").val("Redo search in map");

        });

    $('#loading-2').hide();
    $('#loading-spin').hide();
    });

})();