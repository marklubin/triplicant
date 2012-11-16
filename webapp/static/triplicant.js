/*
*triplicant.js
*jquery functions used in triplicant web app
*Mark Lubin
*/

var inputs;

function test(){
    inputs = $('input')
}


$(document).ready(function(){
    $('a').click(function(event){
        event.preventDefault();
        console.log("they want a trip");
    });
});
