import os
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
            print('set img colors to 256')
            # img.depth(8)
        img.quality(quality)
        img.write(default_storage.location + "/"+ f.name)
        
    elif operation == 'resize':
        width = params['width']
        height = params['height']
        ignoreAspectRatio = params['ignoreAspectRatio']
        
        img.filterType(FilterTypes.SincFilter)
        # geometry = Geometry( int(width), int(height) ).aspect(ignoreAspectRatio=='True')
        # img.resize(Geometry( int(width), int(height) ).aspect(ignoreAspectRatio=='True'))
        geo = Geometry( int(width), int(height) )
        geo.aspect(ignoreAspectRatio=='True' or ignoreAspectRatio=='true')
        img.resize(geo)
        # img.resize(Geometry( int(width), int(height) ))
        img.write(default_storage.location + "/"+ f.name)

    elif operation == 'convert':
        img_type = params['img_type'];
        img.write(default_storage.location + "/"+ os.path.splitext(f.name)[0] + '.' + img_type)
         
    elif operation == 'transparent':
        transparentColor = params['transparentColor']
        pass
    
    elif operation == 'watermark':
        watermarkText = params['ignoreAspectRatio']
        opacity = params['opacity']
        
    elif operation == 'Animate':
        interval = params['delay']
    else:
        pass
            
        # blob = Blob(f.read())
        # img = Image(blob,Geometry(100,100))
        # img .write(f.name)
        
    return
