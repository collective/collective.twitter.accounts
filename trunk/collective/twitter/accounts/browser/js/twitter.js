function removeAuthAccount(name){
    $("#auth-account-"+name).remove();
    jQuery.get('@@remove-auth-account',
                {'account_name':name},
                function(results){});
}

function requestTwitterToken() {
    
    var consumer = document.getElementById('form.consumer').value;
    var consumer_key = document.getElementById('form.consumer_key').value;        
    var consumer_secret = document.getElementById('form.consumer_secret').value;
    
    jQuery.get('@@request-token',
                {'consumer':consumer,
                 'consumer_key':consumer_key,
                 'consumer_secret':consumer_secret},
                function(results){

                    var div = $('#token_url_placeholder');
                    div.html('');
                    if (results){
                        var split = results.split("&");
                        var a = $('<a></a>');
                        a.attr('href', split[0]);
                        a.attr('target', '_blank');
                        a.html('Allow permission to your account');
    
                        div.append(a);
                        document.getElementById("form.oauth_token").value = split[1];
                        document.getElementById("form.oauth_token_secret").value = split[2];
                    }
                    else{
                        var p = $('<p></p>');
                        p.html('Invalid "consumer key" and "consumer secret" provided');
    
                        div.append(p);
                        document.getElementById("form.oauth_token").value = "";
                        document.getElementById("form.oauth_token_secret").value = "";
                    }
                    
                });

}
