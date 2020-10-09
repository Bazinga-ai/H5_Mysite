var status = 0;
var real_size = -1;
var ready_to_upload = false;
/*
    status 1: OK
    status 2: size overloaded

*/

$("#upload").click(function() {
    mainUp();
    boxEnable();
    $("#submit_upload").css("pointer-events", "auto");
    $("#submit_upload").css("background-color", "rgba(255, 255, 255, 0.8)");
});

$("#download").click(function() {
    mainUp();
    boxEnable2();
    $("#submit_download").css("pointer-events", "auto");
    $("#submit_download").css("background-color", "rgba(255, 255, 255, 0.8)");
});

$("#close-upload").click(function() {
    boxDisable();
    mainDown();
    erase();
});

$("#close-download").click(function() {
    boxDisable2();
    mainDown();
    erase();
});

$("#back").click(function() {
    location.href = "../";
});

function erase() {
    $("#id_id").val("");
    $("#id_key_download").val("");
    $("#id_keycode_upload").val("");
    $("#file-input").val("");
    $("#file-name").html("");
    $("#f-size").html("");
    $("#warning").html("");
    $("#warning-download").html("");
    ready_to_upload = false;
}

function mainUp() {
    $("#main").css("animation", "move-up 0.5s ease forwards");
    $("#upload").attr("disabled", "true");
    $("#download").attr("disabled", "true");
}

function mainDown() {
    $("#main").css("animation", "move-down 0.5s ease forwards");
    $("#upload").removeAttr("disabled", "true");
    $("#download").removeAttr("disabled", "true");
}

function boxEnable() {
    $("#show-box-upload").css("display", "block");
    $("#show-box-upload").css("animation", "show-box-enable 0.6s ease forwards");
}

function boxDisable() {
    $("#show-box-upload").css("animation", "show-box-disable 0.3s ease forwards");
    setTimeout(function () {
        $("#show-box-upload").css("display", "none");
    }, 200);
}


function boxEnable2() {
    $("#show-box-download").css("display", "block");
    $("#show-box-download").css("animation", "show-box-enable 0.6s ease forwards");
}

function boxDisable2() {
    $("#show-box-download").css("animation", "show-box-disable 0.3s ease forwards");
    setTimeout(function () {
        $("#show-box-download").css("display", "none");
    }, 200);
}



$("#submit_upload").click(function(e) {
    if (ready_to_upload) {
        $("#submit_upload").css("pointer-events", "none");
        $("#submit_upload").css("background-color", "grey");    
    }
    if (real_size == -1) return false;
    var form_data = new FormData();
    var password = $("#id_keycode_upload").val();
    var file_obj = $('[name=n_file_upload]')[0].files[0];
    var front_status = status;

    if (password == '' || password == null) {
        password = '0';
    }

    if (file_obj == null) {
        $("#warning").html("Please select a file.");
        $("#warning").css("color", "crimson");
    }

    form_data.append('password', password);
    form_data.append('file_obj', file_obj);
    form_data.append('front_status', front_status);
    form_data.append('front_real_size', real_size);
    form_data.append('csrfmiddlewaretoken', str_csrf_token);

    // alert("???");

    $.ajax({
        url: url1,
        type: "POST",
        data: form_data,
        processData: false, //告诉jQuery不要去处理发送的数据
        contentType: false, // 告诉jQuery不要去设置Content-Type请求头
        success: function(data) {
            var obj = JSON.parse(data);
            if (obj.status == 1) {
                // $("#warning").html(obj.msg);
                // $("#warning").css("color", "rgb(83, 164, 84)");
                

                upload_successful(obj);

                // alert(obj.msg);
                // location.reload();
            }
            else {
                $("#warning").html(obj.msg);
                $("#warning").css("color", "crimson");
            }
        },
        xhr: function() {
            var xhr = new XMLHttpRequest();
            //使用XMLHttpRequest.upload监听上传过程，注册progress事件，打印回调函数中的event事件
            xhr.upload.addEventListener('progress', function (e) {
                console.log(e);
                //loaded代表上传了多少
                //total代表总数为多少
                var progressRate = e.loaded / e.total;
                var progressStr = (progressRate * 100).toFixed(1) + '%';

                //通过设置进度条的宽度达到效果
                console.log(progressRate);
                // $("#warning-download").html(obj.msg);
                r = 83 * progressRate;
                g = 164 * progressRate;
                b = 84 * progressRate;
                rgb = "rgb(" + r + ", " + g + ", " + b + ")";
                $("#warning").css("color", rgb);
                $("#warning").html(progressStr);
            })

            return xhr;
        }
    });
    e.preventDefault();
}); 

$("#submit_download").click(function(e) {
    // alert("download...");
    var id = $("#id_id").val();
    var password = $("#id_key_download").val();

    if (id == '' || id == null) {
        id = -1;
    }
    
    if (password == '' || password == null) {
        password = '0';
    }

    $.ajax({
        url: url2,
        type: "POST",
        data: {
            'id': id,
            'password': password,
            csrfmiddlewaretoken: str_csrf_token
        },
        success: function(data) {
            var obj = JSON.parse(data);
            if (obj.status == 1) {
                $("#submit_download").css("pointer-events", "none");
                $("#submit_download").css("background-color", "grey");
                $("#warning-download").html(obj.msg);
                $("#warning-download").css("color", "rgb(83, 164, 84)");
                // alert(obj.path + '\n                        ' + obj.name + '\n');
                location.href = url3 + '/' + id + 'radar' + password + '/';
            }
            else if (obj.status > 1) {
                $("#warning-download").html(obj.msg);
                $("#warning-download").css("color", "crimson");
            }
            // console.log("OK");
            // location.href =
            
        }
    });

    e.preventDefault();
});

$("#choose-file-btn").click(function() {
    console.log("clicked");
    $("#file-input").click();
});

function file_check(e) {
    var file_name = $("#file-input").val();
    real_size = (e.files[0].size / 1024 / 1000.0).toFixed(3);
    if (real_size > 20) {
        // real_size += " MB";
        $("#warning").html("File size cannot be more than 20 MB.");
        $("#warning").css("color", "crimson");
        status = 2;
        real_size = -1;
        ready_to_upload = false;
        return false;
    }
    else if (real_size >= 1 && real_size <= 20) {
        real_size += " MB";
        status = 1;
        $("#warning").html("");
    }
    else if (real_size <= 0.001) {
        real_size = -1;
        real_size = "smaller than 1 KB";
        status = 1;
        $("#warning").html("");
    }
    else if (real_size < 1) {
        status = 1;
        real_size *= 1000;
        real_size += " KB";
        $("#warning").html("");
    }
    
    console.log(real_size);
    $("#file-name").html = '';
    var pos = file_name.lastIndexOf("\\");
    $("#file-name").html(file_name.substring(pos + 1));
    $("#f-size").html("Size: " + real_size);

    ready_to_upload = true;

    // $("#warning").html("文件合格");
}

function upload_successful(obj) {
    boxDisable();
    $("#show-box-after").css("display", "block");
    $("#show-box-after").css("opacity", "1");
    $("#show-box-after").css("animation", "move-down 0.5s ease forwards");

    $("#show-box-after-text").html(obj.msg);
    // $("#show-box-after-text").css("color", "crimson");
}


$("#close-after").click(function () {
    $("#show-box-after").css("display", "none");
    $("#show-box-after").css("opacity", "0");
    $("#show-box-after").css("animation", "move-up 0.5s ease forwards");
    mainDown();
    erase();
});