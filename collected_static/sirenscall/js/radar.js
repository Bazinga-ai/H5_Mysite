$("#upload").click(function () {
    mainUp();
    boxEnable();
});

$("#download").click(function () {
    mainUp();
    boxEnable();
});

$("#close").click(function () {
    boxDisable();
    mainDown();
});

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
    $("#show-box").css("display", "block");
    $("#show-box").css("animation", "show-box-enable 0.6s ease forwards");
}

function boxDisable() {
    $("#show-box").css("animation", "show-box-disable 0.3s ease forwards");
    setTimeout(function () {
        $("#show-box").css("display", "none");
    }, 200);
}
