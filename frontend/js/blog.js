var server = 'http://oluwafemi.pythonanywhere.com/api/v1/';
$(document).ready(function(){
    setEnv();    
    while(fetchBlogPosts()){
        console.log("fetching blog posts");
    }
    $('#signin-btn').click(function(e){
        e.preventDefault();
        signIn();
    });

    $('#signup-btn').click(function(e){
        e.preventDefault();
        signUp();
    });

    $('.logout-btn').click(function(e){
        e.preventDefault();
        localStorage.clear();
        setEnv();
    });
    $('.create-post-btn').click(function(e) {
        e.preventDefault();
        createPost();
    });
    
});

var fetchBlogPosts = function(){
    var response = $.get(server+'posts').done(
            function(data){
                var markup = '';
                datag = data;
                for(var i=0; i < data.length; i++){
                    if(i > 0){
                        markup += '<hr>';
                    }
                    markup += '<article><h3 onmouseout="removeModifiers('+data[i].id+');" onmouseover="generateModifiers('+data[i].id+');" data-id="'+data[i].id+'"><a href="#">'+ data[i].title +'</a></h3>';
                    markup += '<p>'+data[i].body+'</p>';
                    var d = new Date(data[i].created_at);
                    var created_at = d.yyyymmdd();
                    markup += 'Published: <time>'+created_at+'</time>'
                    markup += '</article>';
                }
                $('#blog-entries').append(markup);
                return false;
            }
        );
}

var signIn = function(){
    var email = $("#signin-email").val();
    var password = $("#signin-pwd").val();
    $.post(server+'sessions',{email:email, password:password}).done(function(data){
    console.log(data);
      localStorage.setItem('BLOGAPPID',data.id);
       var success = '<div id="signin-success" class="alert-box success">Login successful</div>';
        $('#signinModal div').hide();
        $('#signinModal h2').after(success).slideDown();
        $('#signin-success').fadeOut(6000, function(){$(this).remove();});
        $('#signinModal').foundation('reveal', 'close');
        setAdminEnv();
    }).error(function(){
        var error = '<div id="signin-error" class="alert-box alert">Login failed. Check email/password</div>';
        $('#signinModal h2').after(error).slideDown();
        $('#signin-error').fadeOut(6000, function(){$(this).remove();});
    });
}; 

var signUp = function(){
    var email = $("#signup-email").val();
    var password = $("#signup-pwd").val();
    $.post(server+'users',{email:email, password:password}).done(function(data){
        //console.log(data);
      localStorage.setItem('BLOGAPPID',data.id);
       var success = '<div id="signup-success" class="alert-box success">Login successful</div>';
        $('#signupModal div').hide();
        $('#signupModal h2').after(success).slideDown();
        $('#signup-success').fadeOut(6000, function(){$(this).remove();});
        $('#signupModal').foundation('reveal', 'close');
        setAdminEnv();
    }).error(function(){
        var error = '<div id="signin-error" class="alert-box alert">Login failed. Check email/password</div>';
        $('#signupModal h2').after(error).slideDown();
        $('#signup-error').fadeOut(6000, function(){$(this).remove();});
    });
};

var setAdminEnv = function(){
    $('.show-signin, .show-signup').hide();
    $('.create-post').show();
    $('.logout-btn').show();
};

var setEnv = function(){
    if(localStorage.hasOwnProperty('BLOGAPPID')){
        setAdminEnv();
    }
    else{
        setGuestEnv();
    }

}

var setGuestEnv = function(){
    $('.create-post').hide();
    $('.logout-btn').hide();
    $('.show-signin, .show-signup').show();
}

var createPost = function(){
    var title = $('#blog-entry-title').val();
    var body = $('#blog-entry-text').val();
    var user_id = localStorage.getItem('BLOGAPPID');
    $.post(server+'posts',{title:title, body:body, id:user_id}).done(function(){
    $('#createModal').foundation('reveal', 'close');   
    var success = '<div id="create-success" class="alert-box success">Post created successfully.</div>';
    $('#blog-entries').before(success).slideUp();
    $('#create-success').fadeOut(6000, function(){$(this).remove();});
    fetchBlogPosts();
    });
    
}
// Adds menu for Update and delete
function generateModifiers(postId) {
    if(localStorage.hasOwnProperty('BLOGAPPID')){
        $('h3[data-id='+postId+'] a').append('<span style="padding-left: 5px" class="p-menu"><i class="fa fa-pencil-square-o"></i><a href="#" onclick="deletePost('+postId+')"><i class="fa fa-trash-o"></i></a></span>');   
        }
};

function removeModifiers(postId){
    $('.p-menu').remove();
};
// Sends request that deletes post from db
function deletePost(postId){
    $.ajax({
        url: server+'posts/'+postId,
        type: 'DELETE',
        dataType: 'json',
    })
    .done(function() {
        alert("Post successfully deleted.");
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        console.log("complete");
    });
    
}

Date.prototype.yyyymmdd = function() {         
                                
        var yyyy = this.getFullYear().toString();                                    
        var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based         
        var dd  = this.getDate().toString();             
                            
        return yyyy + '-' + (mm[1]?mm:"0"+mm[0]) + '-' + (dd[1]?dd:"0"+dd[0]);
   };  
