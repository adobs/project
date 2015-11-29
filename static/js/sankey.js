
// (function(){
    
    function addSource(data){
        var options = $.parseJSON(data);

        var container = $("#self_summary_words_container");
        var container_expanded = $('#self_summary_words_container_expanded');
        container.empty();
        container_expanded.empty();


        
        // container.append($('<li></li>').val(options.unique[i]).html(options.unique[i]));
        for (var i = 0; i < options.unique.length; i++){
            container.append($('<div class="word-div"></div>').val(options.unique[i]).html(options.unique[i]));
        }
    }

    function addTarget(data){
        
            var options = $.parseJSON(data);

            var container = $("#message_me_if_words_container");
            container.empty();
            
            for (var i = 0; i < options.unique.length; i++){
                container.append($('<div class="word-div"></div>').val(options.unique[i]).html(options.unique[i]));
            }
        }


    function showWords(source, target){
        $.get("/source.json", {"source": source}, addSource);
        $.get("/source-chart.json", {"source": source, "genderElement":
            "self-summary-gender-chart", "orientationElement":
            "self-summary-orientation-chart", "ageElement":
            "self-summary-age-chart", "genderCommentElement":
            "self-summary-gender-comment-info", "orientationCommentElement":
            "self-summary-orientation-comment-info", "ageCommentElement":
            "self-summary-age-comment-info"}, makeDoughnutChart);

        $.get("/target.json", {"target": target}, addTarget);
        $.get("/target-chart.json", {"target": target, "genderElement":
            "message-me-if-gender-chart", "orientationElement":
            "message-me-if-orientation-chart", "ageElement":
            "message-me-if-age-chart", "genderCommentElement":
            "message-me-if-gender-comment-info", "orientationCommentElement":
            "message-me-if-orientation-comment-info", "ageCommentElement":
            "message-me-if-age-comment-info"}, makeDoughnutChart);
    }

    function resetSelfSummaryCharts(){

        // clear out comments
        $("#self-summary-gender-comment-info").html("<ul></ul>");
        $("#self-summary-orientation-comment-info").html("<ul></ul>");

        // remove old charts
        $("#self-summary-gender-chart").remove();
        $("#self-summary-orientation-chart").remove();
        $("#self-summary-age-chart").remove();

        // add gender canvas
        $("#self-summary-gender").text("Gender").append('<canvas id="self-summary-gender-chart" class="chart" ></canvas>');
        
        // add orientation canvas
        $("#self-summary-orientation").text("Orientation").append('<canvas id="self-summary-orientation-chart" class="chart" ></canvas>');
        
        // add age canvas
        $("#self-summary-age").text("Age").append('<canvas id="self-summary-age-chart" class="chart" ></canvas>');

    }

    function resetMessageMeIfCharts(){
        // clear out comments
        $("#message-me-if-gender-comment-info").html("<ul></ul>");
        $("#message-me-if-orientation-comment-info").html("<ul></ul>");

        // remove old charts
        $("#message-me-if-gender-chart").remove();
        $("#message-me-if-orientation-chart").remove();
        $("#message-me-if-age-chart").remove();

        // add gender canvas
        $("#message-me-if-gender").text("Gender").append('<canvas id="message-me-if-gender-chart" class="chart" ></canvas>');

        // add orientation canvas    
        $("#message-me-if-orientation").text("Orientation").append('<canvas id="message-me-if-orientation-chart" class="chart" ></canvas>');
        
        // add age canvas
        $("#message-me-if-age").text("Age").append('<canvas id="message-me-if-age-chart" class="chart" ></canvas>');


    }


    function setHeightWidth(){
        // set height and widths of charts
        var chartSectionWidth = $('#self-summary').width()/3;
        var wordSectionWidth = $('#self-summary').width();
        var chartSectionHeight = chartSectionWidth*0.5;
        $("#self_summary_words_container").width(wordSectionWidth);
        $("#message_me_if_words_container").width(wordSectionWidth);

        $("#self-summary-gender-chart").width(chartSectionWidth);
        $("#self-summary-gender-chart").height(chartSectionHeight);
        $("#self-summary-orientation-chart").width(chartSectionWidth);
        $("#self-summary-orientation-chart").height(chartSectionHeight);
        $("#self-summary-age-chart").width(chartSectionWidth);
        $("#self-summary-age-chart").height(chartSectionHeight);
        $("#self-summary-gender-comment-info").width(chartSectionWidth);
        $("#self-summary-orientation-comment-info").width(chartSectionWidth);

        $("#message-me-if-gender-chart").width(chartSectionWidth);
        $("#message-me-if-gender-chart").height(chartSectionHeight);
        $("#message-me-if-orientation-chart").width(chartSectionWidth);
        $("#message-me-if-orientation-chart").height(chartSectionHeight);
        $("#message-me-if-age-chart").width(chartSectionWidth);
        $("#message-me-if-age-chart").height(chartSectionHeight);
        $("#message-me-if-gender-comment-info").width(chartSectionWidth);
        $("#message-me-if-orientation-comment-info").width(chartSectionWidth);
    }


    function makeDoughnutChart(data){

        var options = $.parseJSON(data);
        var genderElementId = options.gender.identifier;
        var genderElementCommentId = options.gender.commentElement;
        var genderDataPoints = options.gender.dataPoints;
        console.log(options.orientation.commentInfo[0].value);
        console.log(options.orientation.commentInfo[0].label);
        var orientationElementId = options.orientation.identifier;
        var orientationElementCommentId = options.orientation.commentElement;
        var orientationDataPoints = options.orientation.dataPoints;
        var ageElementId = options.age.identifier;
        var ageElementCommentId = options.age.commentElement;
        var ageDataPoints = options.age.dataPoints;


        if ((genderElementId).includes('self-summary')){
            resetSelfSummaryCharts();

        }else{
            resetMessageMeIfCharts();
        }

        setHeightWidth();
        
        var genderSum= 0;
        var manSum;
        for (var i = 0; i < options.gender.commentInfo.length; i++){

            if (parseFloat(options.gender.commentInfo[i].value)>0.0 && options.gender.commentInfo[i].label!='Man'){
                genderSum += parseFloat(options.gender.commentInfo[i].value);
                $("#"+genderElementCommentId+" ul").append("<li>"+options.gender.commentInfo[i].label + ": " + options.gender.commentInfo[i].value + "%</li>");
            }

            if (options.gender.commentInfo[i].label=='Man'){
                manSum = parseFloat(options.gender.commentInfo[i].value).toFixed(1);
            }
        }
        
        if (manSum!=100){
            $("#"+genderElementCommentId).prepend('<i>"Other" Category: ' + (100 - manSum).toFixed(1) + "%</i>");
        }

        if ((100 - manSum) > genderSum){
            $("#"+genderElementCommentId+" ul").append("<li>Everything else: " + (100 - manSum - genderSum).toFixed(1) + "%</li>");

        }


        var orientationSum = 0.0;
        var straightSum;
        for (var j=0; j < options.orientation.commentInfo.length; j++){

            if (parseFloat(options.orientation.commentInfo[j].value)>0.0 && options.orientation.commentInfo[j].label!='Straight'){
                orientationSum += parseFloat(options.orientation.commentInfo[j].value);
                $("#"+orientationElementCommentId+" ul").append("<li>"+options.orientation.commentInfo[j].label + ": " + options.orientation.commentInfo[j].value + "%</li>");
            }

            if (options.orientation.commentInfo[j].label=='Straight'){
                straightSum = parseFloat(options.orientation.commentInfo[j].value).toFixed(1);
            }
        }
        if (straightSum!=100){
            $("#"+orientationElementCommentId).prepend('<i>"Other" Category: ' + (100 - straightSum).toFixed(1) + "%</i>");
        }

        if ((100 - straightSum) > orientationSum){
            $("#"+orientationElementCommentId+" ul").append("<li>Everything else: " + (100 - straightSum - orientationSum).toFixed(1) + "%</li>");
        }

        var genderContext = document.getElementById(genderElementId).getContext('2d');
        var genderChart = new Chart(genderContext).Doughnut(genderDataPoints,{maintainAspectRatio: true, responsive: true});

        var orientationContext = document.getElementById(orientationElementId).getContext('2d');
        var orientationChart = new Chart(orientationContext).Doughnut(orientationDataPoints,{maintainAspectRatio: true, responsive: true});

        var ageContext = document.getElementById(ageElementId).getContext('2d');
        var ageChart = new Chart(ageContext).Doughnut(ageDataPoints,{maintainAspectRatio: true, responsive: true});

    }

// })();