from django.urls import path

from core.views import process_file

urlpatterns = [
    path('files/', process_file, name='process_file'),
]
