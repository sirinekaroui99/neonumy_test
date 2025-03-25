from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .forms import ImageUploadForm
from .models import UploadedImage

def index(response):
    return HttpResponse("Hello, world. You're at the main index.")

def v1(response):
    return HttpResponse("Hello, the second view.")
# Create your views here.

import logging

logger = logging.getLogger(__name__)

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            logger.info("Image successfully uploaded.")  # Log successful upload
            return redirect('image_list')  # Redirect to the gallery after upload
        else:
            logger.error("Form is not valid. Errors: %s", form.errors)  # Log form errors if invalid
    else:
        form = ImageUploadForm()

    return render(request, 'main/upload_image.html', {'form': form})
def image_list(request):
    images = UploadedImage.objects.all()
    return render(request, 'main/image_list.html', {'images': images})

def delete_image(request, image_id):
    # Retrieve the image to delete by its ID, and handle the case where the image doesn't exist
    try:
        image = UploadedImage.objects.get(id=image_id)
        # Delete the image file from the filesystem
        image.image.delete()  # This will remove the image from the media folder
        # Delete the image record from the database
        image.delete()
    except UploadedImage.DoesNotExist:
        raise Http404("Image not found")  # Raise a 404 error if the image does not exist

    # Redirect back to the image list after deletion
    return redirect('image_list')

def image_details(request, image_id):
    try:
        image = UploadedImage.objects.get(id=image_id)
    except UploadedImage.DoesNotExist:
        # Handle the case when the image does not exist
        return redirect('image_list')  # Or show an error page

    return render(request, 'main/image_details.html', {'image': image})