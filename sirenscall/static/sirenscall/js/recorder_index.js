$(".submit-button").click(function(e) {
    var password = $("#id_password").val();
    if ($("#input-ck-box").prop("checked")) {
        if (password == null || password == undefined || password == "") {
            password = '0';
        }
        else {
            password = $("#id_password").val();
        }    
    }
    else {
        password = '0';
    }
    // alert(password);

    $.ajax({
        url: url1,
        type: "POST",
        data: {
            'n_main_text': $("#id_main_text").val(),
            'n_title': $("#id_title").val(),
            'n_author': $("#id_author").val(),
            'n_password': password,

            csrfmiddlewaretoken: str_csrf_token
        },
        success: function(data) {
            var obj = JSON.parse(data);
            if (obj.status == 1) {
                $("#warning").css("color", "rgb(83, 164, 84)");
                $("#warning").html("<br>Record successful.");
                location.reload();
            }
            else if (obj.status >= 2) {
                $("#warning").css("color", "crimson");
                $("#warning").html(obj.data_error);
            }
        }
    });
    e.preventDefault();
});

$(".back-btn").click(function() {
    window.location.href = "../";
});

$(function() {
    $("#password-input").hide();
    $("#input-ck-box").click(function() {
        if ($(this).prop("checked")) {
            $("#password-input").show();
        }
        else {
            $("#password-input").hide();
        }
    });
});


$(".locked-btn").click(function(e) {
    var idFull = $(this).attr("id");
    var unlock_id = idFull.match(/\d+/g)[0];
    console.log(unlock_id);
    console.log("Type: " + typeof(unlock_id));
    console.log($("#id_unlock-" + unlock_id).val());

    $.ajax({
        url: url2,
        type: "POST",
        data: {
            'n_unlock': $("#id_unlock-" + unlock_id).val(),
            'unlock_id': unlock_id,

            csrfmiddlewaretoken: str_csrf_token
        },
        success: function(data) {
            var obj = JSON.parse(data);
            console.log("Data received.");
            if (obj.status == 1) {
                // console.log("OK. Data received.");
                $("#unlock-form-" + unlock_id).hide();
                $("#locked-pre-" + unlock_id).append("<pre class='pre-scrollable'>" + obj.main_text + "</pre>");
            }
            else if (obj.status == 2) {
                id = "#locked-warning-" + unlock_id;
                $(id).css("color", "crimson");
                $(id).html(obj.data_error);
            }
        }
    });
    e.preventDefault();
});