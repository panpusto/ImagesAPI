import mimetypes
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from django.http import FileResponse
from .models import Image, ExpiringLink
from .mixins import ExpiringLinkMixin
from .permissions import IsAdminOrEnterprise
from .serializers import (
    ImageCreateSerializer,
    ImageListSerializer,
    ExpiringLinkCreateSerializer,
    ExpiringLinkListSerializer
)


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


class ExpiringLinkListCreateAPIView(generics.ListCreateAPIView, ExpiringLinkMixin):
    permission_classes = [IsAdminOrEnterprise]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ExpiringLinkCreateSerializer
        return ExpiringLinkListSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = self.link 
        return response

    def perform_create(self, serializer):
        expiration_time = self.request.data.get("expiration_time")
        self.link = self.generate_expiring_link(serializer.validated_data.get("image"), expiration_time)
    
    def get_queryset(self):
        return ExpiringLink.objects.filter(image__user=self.request.user)
    
    

class ExpiringLinkDetailAPIView(generics.RetrieveAPIView, ExpiringLinkMixin):
    queryset = ExpiringLink.objects.all()
    permission_classes = [AllowAny]
    
    def get_object(self):
        signed_link = self.kwargs.get("signed_link")
        expiring_link_id = self.decode_signed_value(signed_link)
        expiring_link = generics.get_object_or_404(self.queryset, pk=expiring_link_id)
        if expiring_link.is_expired():
            expiring_link.delete()
            raise NotFound("Link has expired.")
        
        return expiring_link.image
    
    def retrieve(self, request, *args, **kwargs):
        image = self.get_object().image
        content_type, encoding = mimetypes.guess_type(image.name)
        response = FileResponse(
            image,
            content_type=content_type,
            as_attachment=False,
            filename=image.name.split('/')[-1])
        
        return response
