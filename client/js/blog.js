blogAppId = 0;
var server = 'http://oluwafemi.pythonanywhere.com/api/v1/';
$(document).ready(function(){    
    while(fetchBlogPosts()){
        console.log("fetching blog posts");
    }
    
    
});

var fetchBlogPosts = function(){
    var response = $.get(server+'posts').done(
            function(data){
                var markup = ''
                for(var i=0; i < data.length; i++){
                    if(data.length > 1){
                        markup = '<hr>';
                    }
                    markup += '<article><h3><a href="#">'+ data[i].title +'</a></h3>';
                    markup += '<p>'+data[i].body+'</p>';
                    markup += '</article>';
                }
                $('#blog-entries').append(markup);
                return false;
            }
        );
} 