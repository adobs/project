
function resetSelfSummaryCharts(){

    // clear out comments
    $("#self-summary-gender-comment-info").empty();
    $("#self-summary-orientation-comment-info").empty();

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
    $("#message-me-if-gender-comment-info").empty();
    $("#message-me-if-orientation-comment-info").empty();

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
    var chartSectionHeight = chartSectionWidth*0.5;
    $("#self-summary-gender-chart").width(chartSectionWidth);
    $("#self-summary-gender-chart").height(chartSectionHeight);
    $("#self-summary-orientation-chart").width(chartSectionWidth);
    $("#self-summary-orientation-chart").height(chartSectionHeight);
    $("#self-summary-age-chart").width(chartSectionWidth);
    $("#self-summary-age-chart").height(chartSectionHeight);

    $("#message-me-if-gender-chart").width(chartSectionWidth);
    $("#message-me-if-gender-chart").height(chartSectionHeight);
    $("#message-me-if-orientation-chart").width(chartSectionWidth);
    $("#message-me-if-orientation-chart").height(chartSectionHeight);
    $("#message-me-if-age-chart").width(chartSectionWidth);
    $("#message-me-if-age-chart").height(chartSectionHeight);
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
    for (var i = 0; i < options.gender.commentInfo; i++){
         genderSum += options.gender.commentInfo[i].value;

        document.getElementById(genderElementCommentId).append(options.gender.commentInfo[i].label + ": " + options.gender.commentInfo[i].value + "%");
    }
    document.getElementById(genderElementCommentId).prepend("<b>'Other' Category: " + genderSum + "%</b>");

    var orientationSum = 0;
    for (var j=0; j < options.orientation.commentInfo; j++){
        orientationSum += options.orientation.commentInfo[j].value;

        document.getElementById(orientationElementCommentId).append(options.orientation.commentInfo[j].label + ": " + options.orientation.comemntInfo[j].value + "%");
    }
    doument.getElementById(orientationElementCommentId).prepend("<b>'Other' Category: " + orientationSum + "%</b>");


    var genderContext = document.getElementById(genderElementId).getContext('2d');
    var genderChart = new Chart(genderContext).Doughnut(genderDataPoints,{maintainAspectRatio: true, responsive: true});

    var orientationContext = document.getElementById(orientationElementId).getContext('2d');
    var orientationChart = new Chart(orientationContext).Doughnut(orientationDataPoints,{maintainAspectRatio: true, responsive: true});

    var ageContext = document.getElementById(ageElementId).getContext('2d');
    var ageChart = new Chart(ageContext).Doughnut(ageDataPoints,{maintainAspectRatio: true, responsive: true});

}