function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');




$(document).ready(function(){
$.Dialog({
	shadow: true,
	overlay: false,
	draggable: true,
	icon: '<span class="icon-windows"></span>',
	title: 'Draggable window',
	width: 600,
	height: 250,
	padding: 10,
	content: 'This Window is draggable by caption.',
	onShow: function(){
		var content = '<div id=result></div>' + 
		        '<form id=Loginform action="/auth/" method="POST">' +
				'<label>Login</label>' +
				'<div class="input-control text"><input type="text" name="username" id="username"><button class="btn-clear"></button></div>' +
				'<label>Password</label>'+
				'<div class="input-control password"><input type="password" name="password" id="password"><button class="btn-reveal"></button></div>' +
				'<div class="form-actions">' +
				'<input type="submit" value="Login" class="button primary">&nbsp;'+
				'<button class="button" type="button" onclick="$.Dialog.close()">Cancel</button> '+
				'<input type="hidden" name="csrfmiddlewaretoken" value="' + csrftoken + '"/>'+
				'</div>'+
				'</form>';

		$.Dialog.title("User login");
		$.Dialog.content(content);
	}
	

});

$('#result').html('');

$('#Loginform').submit(function() { // catch the form's submit event
	var withToken = ($(this).serialize());
    $.ajax({ // create an AJAX call...
        data: withToken, // get the form data
		async: false,
        type: $(this).attr('method'), // GET or POST
        url: $(this).attr('action'), // the file to call
        success: function(response) { // on success..
			if (response == "True")
			{
				window.location.replace("/");
			}
			else
			{
				$('#result').html(response); // update the DIV
			}
			
        }
    });
    return false; // cancel original event to prevent form submitting
});
});