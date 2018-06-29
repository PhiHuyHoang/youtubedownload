$(function(){
var games = ["Baseball","Tennis","Golf","Cricket","Football","Hockey","Badminton","Volleyball","Boxing","Kabaddi","Chess","Long Jump","High Jump","Racing","Handball","Swimming","Wrestling"];

$("#autocomplete").autocomplete({
source: games
});

});