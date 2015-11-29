 $("#add-btn").hide();

    // slider
    $(function() {
        $( "#slider-range" ).slider({
            range: true,
            min: 18,
            max: 98,
            values: [ 18, 30 ],
            slide: function( event, ui ) {
                $( "#age" ).val( ui.values[ 0 ] + " - " + ui.values[ 1 ] );
                }
            });
        $( "#age" ).val( $( "#slider-range" ).slider( "values", 0 ) +
          " - " + $( "#slider-range" ).slider( "values", 1 ) );
    });

    //location autofill
    $(function() {
        var availableTags = [];
            {% for location in locations %}
            availableTags.push("{{location.location}}");
            {% endfor %}
    $( "#location" ).autocomplete({
      source: availableTags
    });
  });

    function status(data){
        $("#markov-status").html("Updated!")
    }

    function addToProfile(evt){
        var text= {
            "text": $("#markov").html()
        }
        $.post("/add-to-profile.json", text, status);
    }

    $("#add-btn").on("click", addToProfile)
    
    function showAdjectives(data){
        var options = $.parseJSON(data);
        console.log("options is "+options);
        $('.adjective').empty();
        if (options != ""){
            console.log("in full adjectives list");
            $.each(options, function(i, p) {
            $('.adjective').append($('<option></option>').val(p).html(p));
            });
        }else{
            console.log("empty adjective list")
            $('.adjective').append($('<option></option>').val("None available").html("None available"));
        }
    }

    $('.input').on('change slidechange keypress', function (event) {
        if ($("#orientation").val() && $("#gender").val()){
            console.log("change observed")        
            var adjectiveInputs = {
                "orientation": $("#orientation").val(),
                "gender": $("#gender").val(),
                "age": $("#age").val(),
                "location": $("#location").val(),
            }
            $.get("/markov-adjectives.json", adjectiveInputs, showAdjectives);
        }
    });



    function displayMarkov(data){
        $("#markov").html(data);
        if(data!='invalid search results'){
            $("#add-btn").show();
            $("#markov").removeClass("alert alert-danger").removeAttr('role', 'alert');
        }
        else{
            $("#markov").addClass("alert alert-danger").attr('role', 'alert');
        }

    }

    function execute(evt){
        evt.preventDefault();
        var inputs = {
            "orientation": $("#orientation").val(),
            "gender": $("#gender").val(),
            "age": $("#age").val(),
            "location": $("#location").val(),
            // "radius": $("#radius").val(),
            "randomness": $("#randomness").val(),
            "adjective1": $("#adjective1").val(),
            "adjective2": $("#adjective2").val(),
            "adjective3": $("#adjective3").val()

        }

        $.get("/markov.json", inputs, displayMarkov)
    }
    $("#markov-form").on("submit", execute)