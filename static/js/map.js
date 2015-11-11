
(function () {

    var infoWindow = new google.maps.InfoWindow({
      width: 150
    });
    var circles = [];
    var markers = [];

    function getHtml(logged_in, population, location, long_profile_list, short_profile_list, count, adjective){
        if (logged_in==="True"){

            html =
                '<div id="content">' +
                '<h1>There are <b>' + population + '</b> profiles in ' + location + '</h1>' +
                '<h2>matching your search</h2>'+
                '<button type="button" class="btn btn-primary btn-sm" '+
                    'data-toggle="modal" data-target="#myModal" '+
                    'data-recipients="'+ long_profile_list +'">'+
                    'Message Profiles in '+ location +'</button>'+
                '<h1>The most commonly used adjective is <b>' + adjective + '</b></h1>'+
                '<h2>('+count+' occurences)</h2>'+
                '<button type="button" class="btn btn-primary btn-sm" '+
                    'data-toggle="modal" data-target="#myModal"'+
                    'data-recipients="'+short_profile_list +
                    '">Message Profiles with '+adjective+'</button></div>';
        }else{

            html =
                '<div id="content">'+
                '<h1>There are <b>' + population + '</b> profiles in ' + location + '</h1>'+
                '<h2>matching your search</h2>'+
                '<button type="button" class="btn btn-primary btn-sm" disabled>'+
                    'Login to Message Profiles in ' + location + '</button>' +
                '<h1>The most commonly used adjective is <b>' + adjective + '</b></h1>'+
                '<h2>('+count+' occurences)</h2>'+
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
        marker = new MarkerWithLabel({
        position: {lat: latitude, lng: longitude},
        labelContent: adjective,
        map: map,
        labelClass: "labels",
        labelInBackground: false
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
            circles.push(createCircle(latitude,longitude, count));
            marker = createMarker(latitude, longitude, adjective);
            markers.push(marker);

            bindInfoWindow(marker, map, infoWindow, html);
        }

        $('#loading').hide();
    }


    var map;
    function initialize() {
        var lebanon = { lat: 39.8282, lng: -98.5795 };
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 4,
            center: lebanon
        });
        // .setOptions({styles, styles})
        return map;
    }


    google.maps.event.addDomListener(window, 'load', initialize);
        

    $('#orientation-hover').tooltip();

    function plotInputs(){
        var inputs = {
            "orientation": ($('input[name="orientation"]:checked').serialize()),
            "gender": ($('input[name="gender"]:checked').serialize()),
            "age": $("#age").val()
        };

        $.get("/map-checked.json", inputs, addMarkers);

    }

    // slider
    $(function() {
        $( "#slider-range" ).slider({
            range: true,
            min: 18,
            max: 98,
            values: [ 20, 30 ],
            slide: function( event, ui ) {
                $( "#age" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
                }
            });
        $( "#age" ).val( $( "#slider-range" ).slider( "values", 0 ) +
          " - " + $( "#slider-range" ).slider( "values", 1 ) );
    });


    $('#map-choices-form').on('change slidechange', function (event) {
        event.stopPropagation();
        $('#loading').show();
        plotInputs();
    });

     

    $('#myModal').on('shown.bs.modal', function (evt) {
        var recipients = $(evt.relatedTarget).data('recipients');
        recipients = recipients.replace(/,/g,", ");
        $("#add-recipients").html(recipients);
    });

    function messageSubmission(evt){
        evt.preventDefault();

        var recipients = $("#add-recipients").html();
        var message = $("#message").val();

        var sendInputs = {
            "recipients": recipients,
            "message": message
        };

        $.post("/send-message.json", sendInputs, function(data){
            console.log("finished short sub");});
    }

    $("#message-form").on('submit', messageSubmission);


    $(document).ready(function() {
        $('#pageModal').modal();
        plotInputs();

    });

})();

