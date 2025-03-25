from django.urls import path
from . import views

urlpatterns = [ 
    path('v1/', views.v1, name='v1'),
    path('upload/', views.upload_image, name='upload_image'),
    path('', views.image_list, name='image_list'),  # Ensure this line exists
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
    path('details/<int:image_id>/', views.image_details, name='image_details'),

]

 