from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from urllib.parse import unquote
from .third_party.get_mask_predict import get_prediction
import re

from google.cloud import speech

IMG_DATA_URL_PATTERN = re.compile("data:image/(png|jpeg);base64,(.*)$")
AUDIO_DATA_URL_PATTERN = re.compile("data:audio/(wav|mp3);base64,(.*)$")
MODEL_ID = "ICN3966723492690264064"
PROJECT_ID = "767032446048"

# Audio recording parameters
STREAMING_LIMIT = 240000 * 5  # 20 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"

client = speech.SpeechClient()
config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=SAMPLE_RATE,
    language_code="en-US",
    max_alternatives=1,
)
streaming_config = speech.types.StreamingRecognitionConfig(
    config=config, interim_results=True
)


# def something_request(request):
#     audio_generator = []

import json


@csrf_exempt
def camera_validate_view(request):
    if request.method == "POST":
        if request.is_ajax():
            image_data = unquote(request.body.decode())
            # image_data = DATAURLPATTERN.match().group(2)
            image_data_trim = IMG_DATA_URL_PATTERN.match(image_data).group(2)
            image_data_trim = base64.b64decode(image_data_trim)
            preds = get_prediction(image_data_trim, PROJECT_ID, MODEL_ID)
            print(str(preds))
            preds = str(preds)
            if '"mask"' in preds:
                return HttpResponse('mask')
            elif '"no_mask"' in preds:
                return HttpResponse('no_mask')
            # try:   
            #     return HttpResponse(preds.payload._values[0].display_name)
            # except:
            #     return HttpResponse('Failed')
    return render(request, "camera.html", {})


@csrf_exempt
def transcribe_view(request):
    if request.method == "POST":
        if request.is_ajax():
            audio_data = request.body.decode()
            audio_data_trim = AUDIO_DATA_URL_PATTERN.match(audio_data).group(2)
            audio_data_trim = base64.b64decode(audio_data_trim)
            requests = [
                speech.types.StreamingRecognizeRequest(audio_content=audio_data_trim)
            ]
            with open("test.wav", "wb") as file:
                file.write(audio_data_trim)
            print("Getting text")
            responses = client.streaming_recognize(streaming_config, requests)
            print("Got text")
            transcripts = {"data": []}
            for response in responses:
                if not response.results:
                    continue

                result = response.results[0]

                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript

                print(transcript)
                transcripts["data"].append(transcript)
            return HttpResponse(transcripts)
    return render(request, "microphone.html", {})
