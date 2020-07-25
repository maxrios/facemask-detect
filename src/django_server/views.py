from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import base64
from urllib.parse import unquote
import re
DATAURLPATTERN = re.compile('data=data:image/(png|jpeg);base64,(.*)$')
@csrf_exempt
def test(request):
    if request.method == "POST":
        # print(request.body.decode('utf-8')) 
        if request.is_ajax():
            # image = request.body    
            # print(image)
            image_data = unquote(request.body.decode())
            # image_data = DATAURLPATTERN.match().group(2)
            image_data = image_data[27:].encode()
            image_data = base64.b64decode(image_data)
            filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
            with open(filename, 'wb') as f:
                f.write(image_data)
            exit(1)
            # uploaded_image = photo(img = image)
            # uploaded_image.save()
            # photo=photo.objects.first()  
        # g = open("out.jpg", "w")
        # g.write(base64.decodestring(bytes(request.body.decode('utf-8')[5:], 'utf-8')))
        # g.close()
        # exit()
    return render(request, 'camera.html', {})