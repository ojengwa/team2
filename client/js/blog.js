$(document).ready(function(){
    var server = 'http://oluwafemi.pythonanywhere.com/api/v1/';

    var response = $.get(server+'posts');

    console.log(response);
    
});