var width = $("#about-text").width();

function showText(evt){
    evt.preventDefault();
    $("#about-text").show();
    $("#about").hide();
}
$("#about").on("click", showText);