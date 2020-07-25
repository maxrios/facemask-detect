from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import base64
from urllib.parse import unquote
from .third_party.get_mask_predict import get_prediction
import re

# from google.cloud import speech

# DATA_URL_PATTERN = re.compile("data=data:image/(png|jpeg);base64,(.*)$")
# MODEL_ID = "ICN3966723492690264064"
# PROJECT_ID = "767032446048"

# # Audio recording parameters
# STREAMING_LIMIT = 240000 * 5  # 20 minutes
# SAMPLE_RATE = 16000
# CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

# RED = "\033[0;31m"
# GREEN = "\033[0;32m"
# YELLOW = "\033[0;33m"

# client = speech.SpeechClient()
# config = speech.types.RecognitionConfig(
#     encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz=SAMPLE_RATE,
#     language_code="en-US",
#     max_alternatives=1,
# )
# streaming_config = speech.types.StreamingRecognitionConfig(
#     config=config, interim_results=True
# )


# def something_request(request):
#     audio_generator = []
#     requests = (
#         speech.types.StreamingRecognizeRequest(audio_content=content)
#         for content in audio_generator
#     )

#     responses = client.streaming_recognize(streaming_config, requests)
#     for response in responses:
#         if not response.results:
#             continue

#         result = response.results[0]

#         if not result.alternatives:
#             continue

#         transcript = result.alternatives[0].transcript


@csrf_exempt
def camera_validate_view(request):
    if request.method == "POST":
        if request.is_ajax():
            image_data = unquote(request.body.decode())
            # image_data = DATAURLPATTERN.match().group(2)
            image_data_trim = image_data[27:].encode()
            image_data_trim = base64.b64decode(image_data_trim)
            preds = get_prediction(image_data_trim, PROJECT_ID, MODEL_ID)
            print(preds)

    return render(request, 'camera.html', {})

@csrf_exempt
def transcribe_view(request):
    if request.method == "POST":
        if request.is_ajax():
            audio_data = request.body.decode()
    return render(request, 'microphone.html', {})
