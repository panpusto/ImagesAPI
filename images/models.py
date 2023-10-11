import os
import uuid
import time
from pathlib import Path
from django.db import models
from django.conf import settings
from django.core.files.storage import default_storage
from .utils import path_to_uploaded_img
from .validators import validate_expiration_time


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=path_to_uploaded_img, max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)

    def get_filename(self):
        return Path(f'{self.image}').stem
    
    def __str__(self):
        return f"{self.get_filename()}"
    
    def get_links(self, request):
        user_tier = self.user.account_tier
        base_file = os.path.dirname(self.image.name)
        thumbnails = default_storage.listdir(base_file)[1]
        base_url = request.build_absolute_uri("/").rstrip("/")

        thumbs_for_user = []
        for thumbnail in thumbnails:
            if 'thumb' in thumbnail:
                thumbnails_path = os.path.join(base_file, thumbnail)
                thumbs_for_user.append(base_url + settings.MEDIA_URL + thumbnails_path)
        
        if user_tier.is_expiration_link and hasattr(self, "expiring_link"):
            thumbs_for_user.append(self.expiring_link.link)
        
        if user_tier.is_original_file:
            thumbs_for_user.append(base_url + self.image.url)
            
        return thumbs_for_user


class ThumbnailSize(models.Model):
    height = models.IntegerField()

    def __str__(self):
        return f"{self.width}x{self.height}"


class ExpiringLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, unique=True, related_name="expiring_link")
    link = models.CharField(max_length=255)
    expiration_time = models.IntegerField(validators=[validate_expiration_time])

    def __str__(self):
        return f"{self.id}"

    def is_expired(self):
        current_time = time.time()
        return current_time > self.expiration_time
