// set height and widths of charts
var chartSectionWidth = $('#self-summary-chart-container').width()/3;
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

function makeDoughnutChart(data){
    var options = $.parseJSON(data);
    console.log("options is "+options);
    var genderElementId = options.gender.identifier;
    var genderDataPoints = options.gender.dataPoints;
    var orientationElementId = options.orientation.identifier;
    var orientationDataPoints = options.orientation.dataPoints;
    var ageElementId = options.age.identifier;
    var ageDataPoints = options.age.dataPoints;


    var genderContext = document.getElementById(genderElementId).getContext('2d');
    var genderChart = new Chart(genderContext).Doughnut(genderDataPoints,{maintainAspectRatio: true, responsive: true});

    var orientationContext = document.getElementById(orientationElementId).getContext('2d');
    var orientationChart = new Chart(orientationContext).Doughnut(orientationDataPoints,{maintainAspectRatio: true, responsive: true});

    var ageContext = document.getElementById(ageElementId).getContext('2d');
    var ageChart = new Chart(ageContext).Doughnut(ageDataPoints,{maintainAspectRatio: true, responsive: true});
}