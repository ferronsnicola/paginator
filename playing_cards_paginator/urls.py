from django.urls import path
from .views import file_loader
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', file_loader, name='file_loader')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
