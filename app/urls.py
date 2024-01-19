from django.urls import path
from .views import upload_resume, suggestions

urlpatterns = [
    path('upload/', upload_resume, name='upload_resume'),
    path('suggestions/', suggestions, name='suggestions'),
]