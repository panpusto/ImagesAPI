from rest_framework import serializers
from .models import Image


class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = [
            'image'
        ]


class ImageListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = [
            "images"
        ]
    
    def get_images(self, obj):
        request = self.context.get("request")
        return obj.get_links(request)
