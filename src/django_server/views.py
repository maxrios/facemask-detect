from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import base64
from urllib.parse import unquote
from .third_party.get_mask_predict import get_prediction
import re

DATA_URL_PATTERN = re.compile("data=data:image/(png|jpeg);base64,(.*)$")
MODEL_ID = "ICN3966723492690264064"
PROJECT_ID = "767032446048"


@csrf_exempt
def test(request):
    if request.method == "POST":
        if request.is_ajax():
            image_data = unquote(request.body.decode())
            # image_data = DATAURLPATTERN.match().group(2)
            image_data_trim = image_data[27:].encode()
            image_data_trim = base64.b64decode(image_data_trim)
            preds = get_prediction(image_data_trim, PROJECT_ID, MODEL_ID)
            print(preds)

    return render(request, "camera.html", {})
