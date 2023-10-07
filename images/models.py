import uuid
from django.db import models
from django.conf import settings
from .utils import path_to_uploaded_img
from .validators import validate_expiration_time


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=path_to_uploaded_img, max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)


class ThumbnailSize(models.Model):
    height = models.IntegerField()


class ExpiringLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.OneToOneField(Image, on_delete=models.CASCADE, unique=True, related_name='expiring_link')
    link = models.CharField(max_length=255)
    expiration_time = models.IntegerField(validators=[validate_expiration_time])
