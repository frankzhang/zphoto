from django.http import HttpResponse,JsonResponse,HttpResponseNotAllowed
from django import forms
from django.core.files.storage import default_storage
from django.core.files import File
from pgmagick import Image, Blob, Geometry

# Create your views here.

def upload(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)

        files = request.FILES.getlist('fileList[]')

        for f in files:
            # default_storage.save(None,f)
            blob = Blob(f.read())
            img = Image(blob,Geometry(100,100))
            img .write(f.name)
            print(f)

        return JsonResponse({'msg':'SUCESS'})

    return HttpResponseNotAllowed(permitted_methods=['POST'])
