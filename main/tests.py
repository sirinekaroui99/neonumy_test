from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UploadedImage
import tempfile

class ImageViewsTest(TestCase):
     
    def test_image_upload_invalid(self):
        """Test invalid image upload"""
        # Simulate uploading invalid data (e.g., no image uploaded)
        response = self.client.post(reverse('upload_image'), {})

        # Ensure the form is rendered again with validation errors
        self.assertEqual(response.status_code, 200)  # Expect the form to be re-rendered
        self.assertContains(response, 'This field is required.')  # Check if error is in the response


    def test_image_list(self):
        """Test the image list view"""
        # Add some images to the database
        UploadedImage.objects.create(image='images/test_image1.jpg')
        UploadedImage.objects.create(image='images/test_image2.jpg')

        # Access the image list view
        response = self.client.get(reverse('image_list'))

        # Ensure the response is successful and the images are displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_image1.jpg')
        self.assertContains(response, 'test_image2.jpg')

    def test_delete_image_success(self):
        """Test successful image deletion"""
        image = UploadedImage.objects.create(image='images/test_image.jpg')

        # Delete the image
        response = self.client.get(reverse('delete_image', args=[image.id]))

        # Ensure the image is deleted, and we are redirected to the image list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('image_list'))
        self.assertFalse(UploadedImage.objects.filter(id=image.id).exists())

    def test_delete_image_not_found(self):
        """Test deleting an image that doesn't exist"""
        # Try to delete a non-existent image
        response = self.client.get(reverse('delete_image', args=[999]))

        # Ensure a 404 error occurs since the image does not exist
        self.assertEqual(response.status_code, 404)

    def test_image_details_success(self):
        """Test image details view for an existing image"""
        image = UploadedImage.objects.create(image='images/test_image.jpg')

        # Access the image details view
        response = self.client.get(reverse('image_details', args=[image.id]))

        # Ensure the response is successful and the image details are displayed
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_image.jpg')

    def test_image_details_not_found(self):
        """Test image details view for a non-existent image"""
        # Try to access details for a non-existent image
        response = self.client.get(reverse('image_details', args=[999]))

        # Ensure the user is redirected to the image list page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('image_list'))
