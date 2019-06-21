var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

var getToken = function (){
    var g_auth = localStorage.getItem("auth");
    if(g_auth == null) {
        g_auth = sessionStorage.getItem("auth");
    }

    if(g_auth) {
        try {
            g_auth = JSON.parse(g_auth);
        } catch(error) {
            g_auth = null; 
        }
    }
    return g_auth;
};

var Ajaxlogout = function(url) {

    console.log("Trying to logout");
    console.log("AuthToken: "+ token.key);
    console.log("csrf middleware token: " +g_csrftoken);

    $.ajax({
        url: url, 
        method: "POST", 
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", "Token " + token.key);
        },
        data: {
            csrfmiddlewaretoken: g_csrftoken
        }
    }).done(function(data) {
        console.log("DONE: ", data);
        token = null;
        localStorage.removeItem("auth");
        sessionStorage.removeItem("auth");
        checkIfLoggedIn();
    }).fail(function(data) {
        console.log("FAIL: ", data);
    });
};


var Ajaxlogin = function (username, password, remember_me, url){
    if(username && password) {
        console.log("Will try to login with ", username, password);
        $('#id_login_modal_error').addClass('d-invisible');
        $.ajax({
            url: url, 
            method: "POST", 
            data: {
                username: username,
                password: password,
                csrfmiddlewaretoken: g_csrftoken
            }
        }).done(function(data) {
            console.log("DONE: ", username, data.key);
            token = {
                username: username,
                key: data.key,
                remember_me: remember_me
            };
            $('#id_login_modal').removeClass('active');

            if(remember_me) {
                localStorage.setItem("auth", JSON.stringify(token));
            } else {
                sessionStorage.setItem("auth", JSON.stringify(token));
            }

            checkIfLoggedIn();

            // CAREFUL! csrf token is rotated after login: https://docs.djangoproject.com/en/1.7/releases/1.5.2/#bugfixes
            g_csrftoken = getCookie('csrftoken');
        }).fail(function(data) {
            console.log("FAIL", data);
            $('#id_login_modal_error').removeClass('d-invisible').text(data.responseText);
        });
    } else {
        $('#id_login_modal_error').removeClass('d-invisible');
    }
};


var Ajaxsignup = function (email, password, name, url){
    if(email && password && name) {
        console.log("Will try to create an account with credentials: "+email +" "+password +" "+name);
        $('#id_sign_up_modal_error').addClass('d-invisible');
        $.ajax({
            url: url, 
            method: "POST", 
            data: {
                email: email,
                password: password,
                name: name,
                csrfmiddlewaretoken: g_csrftoken
            }
        }).done(function(data) {
            console.log("DONE: ", data);
            $('#id_sign_up_modal').removeClass('active');
        }).fail(function(data) {
            console.log("FAIL", data);
            $('#id_sign_up_modal_error').removeClass('d-invisible').text(data.responseText);
        });
    } else {
        $('#id_sign_up_modal_error').removeClass('d-invisible');
    }
};


function base64Encode(str) {
    var CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    var out = "", i = 0, len = str.length, c1, c2, c3;
    while (i < len) {
        c1 = str.charCodeAt(i++) & 0xff;
        if (i == len) {
            out += CHARS.charAt(c1 >> 2);
            out += CHARS.charAt((c1 & 0x3) << 4);
            out += "==";
            break;
        }
        c2 = str.charCodeAt(i++);
        if (i == len) {
            out += CHARS.charAt(c1 >> 2);
            out += CHARS.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
            out += CHARS.charAt((c2 & 0xF) << 2);
            out += "=";
            break;
        }
        c3 = str.charCodeAt(i++);
        out += CHARS.charAt(c1 >> 2);
        out += CHARS.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
        out += CHARS.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
        out += CHARS.charAt(c3 & 0x3F);
    }
    return out;
}