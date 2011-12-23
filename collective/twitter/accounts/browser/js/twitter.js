function removeAuthAccount(name){
    $("#auth-account-"+name).remove();
    jQuery.get('@@remove-auth-account',
                {'account_name':name},
                function(results){});
}

function requestTwitterToken() {
    
    var consumer = $('#form\\.consumer').val();
    var consumer_key = $('#form\\.consumer_key').val();        
    var consumer_secret = $('#form\\.consumer_secret').val();
    
    $.ajax({
        url:'@@request-token',
        data:{
            'consumer':consumer,
            'consumer_key':consumer_key,
            'consumer_secret':consumer_secret
        },
        success: function(results){
            var div = $('#token_url_placeholder');
            div.html('');

            if (results){
                var split = results.split("&");
                var a = $('<a/>').attr({
                    'href': split[0],
                    'target': '_blank'
                    }).html('Allow permission to your account');

                div.append(a);
                $("#form\\.oauth_token").val(split[1]);
                $("#form\\.oauth_token_secret").val(split[2]);
            }
            else{
                var p = $('<p/>');
                p.html('Invalid "consumer key" and "consumer secret" provided');

                div.append(p);
                $("#form\\.oauth_token").val("");
                $("#form\\.oauth_token_secret").val("");
            } 
        }
    });
}
