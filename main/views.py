from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .forms import ImageUploadForm
from .models import UploadedImage


import logging

logger = logging.getLogger(__name__)

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.info("Image successfully uploaded.") 
            return redirect('image_list')  
        else:
            logger.error("Form is not valid. Errors: %s", form.errors)  
    else:
        form = ImageUploadForm()

    return render(request, 'main/upload_image.html', {'form': form})
def image_list(request):
    images = UploadedImage.objects.all()
    return render(request, 'main/image_list.html', {'images': images})

def delete_image(request, image_id):
    try:
        image = UploadedImage.objects.get(id=image_id)
        image.image.delete() 
        image.delete()
    except UploadedImage.DoesNotExist:
        raise Http404("Image not found") 

    return redirect('image_list')

def image_details(request, image_id):
    try:
        image = UploadedImage.objects.get(id=image_id)
    except UploadedImage.DoesNotExist:
        return redirect('image_list') 

    return render(request, 'main/image_details.html', {'image': image})