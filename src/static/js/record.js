var audioTag = document.querySelector("#audioElement");

function run_audio_capture() {


    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(function (stream) {
                const mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();

                const audioChunks = [];

                mediaRecorder.addEventListener('dataavailable', event => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }

                });

                mediaRecorder.addEventListener("stop", () => {
                    const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                    var reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = function () {
                        var base64data = reader.result;
                        console.log(base64data);
                        $.ajax({
                            type: "POST",
                            url: window.location.toString(),
                            data: base64data
                        })
                            .done(function (msg) {
                                console.log(msg)
                            });
                    }

                });

                setTimeout(() => {
                    mediaRecorder.stop();
                    run_audio_capture();

                }, 5000);

                //   audio.srcObject = stream;
            }).catch(function (err0r) {
                console.log(err0r);
                console.log("Something went wrong!");
            });
    }
}
run_audio_capture();