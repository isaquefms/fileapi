from rest_framework import routers
from django.urls import path, include
from .views import FileViewSet


router = routers.DefaultRouter()
router.register(r'files', FileViewSet, basename='files')

urlpatterns = [
    path('', include(router.urls)),
]
