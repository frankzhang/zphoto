import os
from django.http import HttpResponse,JsonResponse,HttpResponseNotAllowed
from django import forms
from django.core.files.storage import default_storage
from django.core.files import File
from django.conf import settings
from pgmagick import Image, Blob, Geometry, FilterTypes, Color

from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def upload(request):
    ret = {}
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)

        files = request.FILES.getlist('fileList')
        
        initalPreview = []
        initialPreviewConfig = []
        
        for f in files:
            print(f)
            if 'img_op' in request.POST:
                fname = processing(f,request.POST)
                
                initalPreview.append("<img src='http://debian-workstation.local:8000/media/"+fname+"' class='file-preview-image' style='width:auto;height:60px;max-width:100%;max-height:100%;' alt='image' title='" + os.path.splitext(fname)[0]+"'>")

                initialPreviewConfig.append(
                    { 'caption': os.path.splitext(f.name)[0]+os.path.splitext(fname)[-1],
                       'size': os.path.getsize(settings.MEDIA_ROOT + "/"+ fname),
                       'downloadUrl': 'http://debian-workstation.local:8000/media/'+fname,
                    })
                print(initialPreviewConfig)

        return JsonResponse({
            'msg':'SUCESS',
            'initialPreview': initalPreview ,
            'initialPreviewConfig': initialPreviewConfig,
            })

    return HttpResponseNotAllowed(permitted_methods=['POST'])

def processing(f, params):
    operation = params['img_op']
    blob = Blob(f.read())
    img = Image(blob)
    name = f.name

    if operation == 'compress':
        compress_level = params['compress_level']
        quality = 75
        colorIndex = params['colorIndex']
        
        if compress_level == 'tiny':
            if img.magick() == 'PNG':
                    quality = 95
            else:
                    quality = 50
        elif compress_level == 'quality':
            if img.magick == 'PNG':
                    quality = 75
            else:
                    quality = 90
        else:
            quality = 75

        print(img.magick())
            
        if img.magick() == 'PNG' and (colorIndex == 'True' or colorIndex) == 'true':
            img.quantizeColors(256)
            img.quantize()
            print(colorIndex)

        img.quality(quality)
        name = default_storage.get_available_name(f.name)
        img.write(settings.MEDIA_ROOT + "/"+ name)
        return name

    elif operation == 'resize':
        width = params['width']
        height = params['height']
        ignoreAspectRatio = params['ignoreAspectRatio']
        
        img.filterType(FilterTypes.SincFilter)
        geo = Geometry( int(width), int(height) )
        geo.aspect(ignoreAspectRatio=='True' or ignoreAspectRatio=='true')
        img.resize(geo)
        name = default_storage.get_available_name(f.name)
        img.write(settings.MEDIA_ROOT + "/"+ name)
        return name

    elif operation == 'convert':
        img_type = params['img_type'];
        name = os.path.splitext(f.name)[0] + '.' + img_type
        name = default_storage.get_available_name(name)
        img.write(settings.MEDIA_ROOT + "/"+ name)
        return name
         
    elif operation == 'transparent':
        transparentColor = params['transparentColor']
        fuzz =  params['colorFuzz']
        img.transparent(Color(transparentColor))
        img.colorFuzz(float(fuzz)/100)
        name = os.path.splitext(f.name)[0] + '.png'
        name = default_storage.get_available_name(name)
        img.write(settings.MEDIA_ROOT + "/"+ name)
        return name
    
    elif operation == 'watermark':
        watermarkText = params['ignoreAspectRatio']
        opacity = params['opacity']
        
    elif operation == 'Animate':
        interval = params['delay']
        
        # img.animate
    else:
        pass
            
        # blob = Blob(f.read())
        # img = Image(blob,Geometry(100,100))
        # img .write(f.name)
        
    return f.name
