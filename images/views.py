from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import ImageCreateSerializer, ImageListSerializer
from .models import Image


class ImageListCreateAPIVIew(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ImageCreateSerializer
        return ImageListSerializer

    def get_queryset(self):
            return Image.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)

            success_message = "Image uploaded successfully."
            response_data = {
                 "message": success_message
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
