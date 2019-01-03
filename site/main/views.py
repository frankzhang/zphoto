from django.http import HttpResponse,JsonResponse,HttpResponseNotAllowed
from django import forms
from django.core.files.storage import default_storage
from django.core.files import File
from pgmagick import Image, Blob, Geometry, FilterTypes

# Create your views here.

def upload(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)

        files = request.FILES.getlist('fileList')
        
        for f in files:
            print(f)
            if 'img_op' in request.POST:
                processing(f,request.POST)
            else:
                default_storage.save(None,f)

        return JsonResponse({'msg':'SUCESS'})

    return HttpResponseNotAllowed(permitted_methods=['POST'])

def processing(f, params):
    operation = params['img_op']
    blob = Blob(f.read())
    img = Image(blob)

    if operation == 'compress':
        compress_level = params['compress_level']
        depth = params['depth']
        img.write(f.name)
        
        
    elif operation == 'resize':
        width = params['width']
        height = params['height']
        ignoreAspectRatio = params['ignoreAspectRatio']
        
        img.filterType(FilterTypes.SincFilter)
        # img.resize(width+'x'+height)
        img.scale(width+'x'+height)
        img.write(f.name)
        
    elif operation == 'convert':
        img_type = params['img_type'];
        
    elif operation == 'transparent':
        pass
    
    elif operation == 'watermark':
        watermarkText = params['ignoreAspectRatio']
        opacity = params['opacity']
        
    elif operation == 'Animate':
        
        interval = params['interval']
    else:
        pass
            
        # blob = Blob(f.read())
        # img = Image(blob,Geometry(100,100))
        # img .write(f.name)
        
    return
