
var focusCheck = false;
var input = document.getElementById("search-info");
var oUl = document.getElementById("search-ul");
input.onkeyup = function () {
    var value = this.value;
    var oScript = document.createElement('script');
    oScript.src = 'https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=' + value + '&cb=send'
    // 核心在这里，
    // 1.实时获取参数 value
    // 2.cb=返回值的处理函数（aa）
    document.body.appendChild(oScript)
}
function send(data) {
    oUl.style.display = 'block';
    var list = data.s;
    var str = '';
    if (list.length > 0) {
        focusCheck = true;
        var i = 0;
        list.forEach(function (ele, index) {
            str += '<a href="https://www.baidu.com/s?wd=' + ele + '" id="list' + i + '"' + '>' + ele;
            i++;
        });
        
        hideLabel();
        oUl.innerHTML = str;
        document.getElementById("s-table").style.opacity = 1;
        document.getElementById("s-table").style.visibility = "visible";
        document.getElementById("s-table").style.maxHeight = "400px";


    } else {
        focusCheck = false;
        showLabel();
        document.getElementById("s-table").style.opacity = 0;
        document.getElementById("s-table").style.visibility = "hidden";
        document.getElementById("s-table").style.maxHeight = "0";
    }
}

function lostFocus() {
    document.getElementById("s-table").style.opacity = 0;
    document.getElementById("s-table").style.visibility = "hidden";
    document.getElementById("s-table").style.maxHeight = "0";
    if ($("#search-info").val() != "") showLabel();
}

function getFocus() {
    if (focusCheck == false) return;
    document.getElementById("s-table").style.opacity = 1;
    document.getElementById("s-table").style.visibility = "visible";
    document.getElementById("s-table").style.maxHeight = "400px";
    hideLabel();
}

var cur = -1;

function checkKeyCode(e) {
    
    var as = document.getElementById("search-ul").getElementsByTagName("a");
    switch (e.keyCode) {
        case 38: //up
            if (cur == -1) cur = as.length - 1;
            else {
                as[cur].className = '';
                cur -= 1;
            }
            if (cur < 0) cur = -1;
            if (cur != -1) as[cur].className = 'on';
            break;
        case 40: //down
            if (cur == -1) cur = 0;
            else {
                as[cur].className = '';
                cur++;
            }
            if (cur >= as.length) cur = -1;
            if (cur != -1) as[cur].className = 'on';
            break;
        case 13:
            if (cur != -1) window.location.href = "https://www.baidu.com/s?wd=" + as[cur].innerHTML;
            else if (cur == -1) window.location.href = "https://www.baidu.com/s?wd=" + $("#search-info").val();
            break;
    }
}


var inputFlag = false;

//监听 搜索 按钮
$(function () {
    $("#go-btn").click(function() {
        window.location.href = "https://www.baidu.com/s?wd=" + $("#search-info").val();
    });
});

//监听文本输入框 
$("#search-info").on("input propertychange", function() {
    checkInput();
});

//监听输入文本框 
$("#search-info").focus(function () {
    checkInput();
    zoomIn();
});

$("#search-info").blur(function () {
    zoomOut();
});

function checkInput() {
    var str = $("#search-info").val();
    // console.log(str);
    if (str != "") {
        $("#search-info").css("animation", "search-info-lengthen 0.2s forwards");
        showBtn();
        inputFlag = true;
    }
    else if (str == "") {
        if (inputFlag == true) {
            hideBtn();
            setTimeout("shortenInput()", 100);
        }
        inputFlag = false;
    }
}


function showBtn() {
    $("#go-btn").css("display", "block");
    $("#go-btn").css("opacity", "1");
}

function hideBtn() {
    $("#go-btn").css("opacity", "0");
    setTimeout(function () {
        $("#go-btn").css("display", "none");
    }, 200);
}

function shortenInput() {
    $("#search-info").css("animation", "search-info-shorten 0.2s forwards");
}



//bg图片缩放
function zoomIn() {
    // $("#bg").css("left", "-2%");
    // $("#bg").css("top", "-4%");
    // $("#bg").css("width", "104%");
    // $("#bg").css("height", "108%");
    $("#bg").css("filter", "blur(20px)");
    $("#title").css("text-shadow", "3px 3px 3px rgba(40, 40, 40, .2)");
}

function zoomOut() {
    $("#bg").css("left", "0");
    $("#bg").css("top", "0");
    // $("#bg").css("width", "100%");
    // $("#bg").css("height", "100%");
    $("#bg").css("filter", "blur(0)");
}


var arrWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
var arrMinute = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09"];

function countTime() {
    var date = new Date();
    var hour = date.getHours();
    var minute = date.getMinutes();
    var second = date.getSeconds();
    // console.log(hour + " " + minute + " " + second);
    if (hour == 0 && minute == 0) {
        countDate();
    }
    if (minute < 10) minute = arrMinute[minute];
    $("#time-label").text(hour + ":" + minute);
}

function countDate() {
    var date = new Date();
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var week = date.getDay();
    // console.log(week);
    
    $("#date-label").text(year + "/" + month + "/" + day + " - " + arrWeek[week]);
}

function hideLabel() {
    $("#time-label").css("animation", "label-disable 0.3s forwards");
    $("#date-label").css("animation", "label-disable 0.3s forwards");
}

function showLabel() {
    $("#time-label").css("animation", "label-enable 0.3s forwards");
    $("#date-label").css("animation", "label-enable 0.3s forwards");
}

// init-------------------------->>>>>>>>>
$(function () {
    var date = new Date();
    hour = date.getHours();
    minute = date.getMinutes();
    if (minute < 10) minute = arrMinute[minute];
    $("#time-label").text(hour + ":" + minute);
    countDate();
    // selectBg();
    setInterval("countTime()", 1000);
});

var bgCount = 6;
function selectBg() {
    var base = "../homepage/image/bg/wallpaper";
    var rand = Math.floor(Math.random() * 10) % (bgCount + 1);
    var path = base + rand + ".jpg";
    $(".bg").css("background", "url(" + path + ") center 0 no-repeat");
    $(".bg").css("background-size", "cover-auto");
}

$("#airdrop").click(function () {
    window.location.href = "/radar/";
});

$("#recorder").click(function () {
    window.location.href = "/recorder/";
});