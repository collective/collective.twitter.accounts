function removeAuthAccount(name){
    $("#auth-account-"+name).remove();
    jQuery.get('@@remove-auth-account',
                {'account_name':name},
                function(results){
                    document.getElementById("zc.page.browser_form").reset();
                    var url = '@@twitter-controlpanel';
                    window.location = url;
                });
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

                a.click( function() {
                                     openInPopUp(this);
                                     return false;
                                     })
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

function openInPopUp(mylink){
    href=mylink.href;
    window.open(href, 'popup', 'width=400,height=200,scrollbars=yes');
}