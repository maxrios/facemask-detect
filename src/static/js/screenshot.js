var screenshotButton = document.querySelector('#screenshot-button');
var img = document.querySelector('#screenshot-img');
var canvas = document.createElement('canvas');

function start() {

    setTimeout(function () {
        snap();

        // Again

        // start();
        console.log("make this run more than once plssssszzzzz")
        // Every 3 sec
    }, 1000);
}

function snap() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    // Other browsers will fall back to image/png
    var pic = canvas.toDataURL('image/jpg');
    img.src = pic;
    // pic = pic.replace(/^data:image\/(png|jpg);base64,/, "");

    $.ajax({
        type: "POST",
        url: window.location.toString(),
        data: pic
    })
        .done(function (msg) {
            if (msg = "no_mask") {
                document.body.style.backgroundColor = "red"
            } else if (msg = "mask") {
                document.body.style.backgroundColor = "green"
            } else {
                document.body.style.backgroundColor = "yellow"
            }
            console.log(typeof msg)
            console.log(msg);
        });
};
