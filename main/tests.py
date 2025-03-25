from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UploadedImage
import tempfile

class ImageViewsTest(TestCase):
     
    def test_image_upload_invalid(self):
        """Test invalid image upload"""
        response = self.client.post(reverse('upload_image'), {})
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'This field is required.') 


    def test_image_list(self):
        """Test the image list view"""
        UploadedImage.objects.create(image='images/test_image1.jpg')
        UploadedImage.objects.create(image='images/test_image2.jpg')

        response = self.client.get(reverse('image_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_image1.jpg')
        self.assertContains(response, 'test_image2.jpg')

    def test_delete_image_success(self):
        """Test successful image deletion"""
        image = UploadedImage.objects.create(image='images/test_image.jpg')

        response = self.client.get(reverse('delete_image', args=[image.id]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('image_list'))
        self.assertFalse(UploadedImage.objects.filter(id=image.id).exists())

    def test_delete_image_not_found(self):
        """Test deleting an image that doesn't exist"""

        response = self.client.get(reverse('delete_image', args=[999]))

        self.assertEqual(response.status_code, 404)

    def test_image_details_success(self):
        """Test image details view for an existing image"""
        image = UploadedImage.objects.create(image='images/test_image.jpg')

        response = self.client.get(reverse('image_details', args=[image.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_image.jpg')

    def test_image_details_not_found(self):
        """Test image details view for a non-existent image"""

        response = self.client.get(reverse('image_details', args=[999]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('image_list'))
