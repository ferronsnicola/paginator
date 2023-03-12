from django.urls import path
from .views import file_loader

urlpatterns = [
    path('', file_loader, name='file_loader')
]