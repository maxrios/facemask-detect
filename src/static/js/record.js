var audioTag = document.querySelector("#audioElement");

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function (stream) {
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();

      const audioChunks = [];

      mediaRecorder.addEventListener('dataavailable', event => {
          audioChunks.push(event.data);
      });

      mediaRecorder.addEventListener("stop", () => {
        const audioBlob = new Blob(audioChunks);
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audioTag.src = audioUrl;
        const play = () => {
            audioTag.load();
            audioTag.play();
        };
        $.ajax({
            type: "POST",
            url: window.location.toString(),
            // csrfmiddlewaretoken: '{{ csrf_token }}',
            data: { data: audio}
            })
                .done(function( msg ) {
                // alert( "Data Saved: " + msg );
            });
              
      });

      setTimeout(() => {
        mediaRecorder.stop();
      }, 5000);

    //   audio.srcObject = stream;
    }).catch(function (err0r) {
        console.log(err0r);
      console.log("Something went wrong!");
    });
}