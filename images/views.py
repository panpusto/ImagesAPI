from rest_framework import generics
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import ImageCreateSerializer, ImageListSerializer
from .models import Image

@method_decorator(login_required(login_url="/api-auth/login"), name="dispatch")
class ImageListCreateAPIVIew(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ImageCreateSerializer
        return ImageListSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)
