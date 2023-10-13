from rest_framework import serializers
from .models import Image, ExpiringLink
from rest_framework.exceptions import ValidationError



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
    
    def get_images(self, obj) -> str:
        request = self.context.get("request")
        return obj.get_links(request)


class ExpiringLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = [
            "link"
        ]


class ExpiringLinkImageField(serializers.PrimaryKeyRelatedField):
    """Filters images uploaded by authenticated user."""
    def get_queryset(self):
        user = self.context['request'].user
        return Image.objects.filter(user=user)
    

class ExpiringLinkCreateSerializer(serializers.ModelSerializer):
    image = ExpiringLinkImageField(queryset=Image.objects.all())
    class Meta:
        model = ExpiringLink
        fields = [
            "image",
            "expiration_time"
        ]
