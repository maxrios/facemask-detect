console.log("Video Loaded");
var video = document.querySelector("#videoElement");

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
      start();
      video.srcObject = stream;
    }).catch(function (err0r) {
      console.log("Something went wrong!");
    });
}
