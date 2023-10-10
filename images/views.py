from rest_framework import generics
from .serializers import ImageCreateSerializer, ImageListSerializer
from .models import Image


class ImageListCreateAPIVIew(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ImageCreateSerializer
        return ImageListSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)
