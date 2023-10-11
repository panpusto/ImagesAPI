import os
from io import BytesIO
from celery import shared_task
from PIL import Image as pilImg
from PIL.Image import Resampling
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from .models import Image


@shared_task()
def generate_thumbnails(pk):
    """
    Generates thumbnails for uploaded images
    according to user's account tier.
    """
    instance = Image.objects.get(id=pk)
    user_tier = instance.user.account_tier
    tier_thumbs = user_tier.get_thumbnail_size
    filename, extension = os.path.splitext(os.path.basename(instance.image.name))
    image_name = filename.split("/")[-1]

    for thumb_size in tier_thumbs:
        height = int(thumb_size.height)

        img_file = BytesIO(instance.image.read())
        with pilImg.open(img_file) as image:
            original_width, original_height = image.size
            aspect_ratio = original_width / original_height
            new_width = int(height * aspect_ratio)

            image = image.resize((new_width, height), resample=Resampling.LANCZOS)
            thumbnail_io = BytesIO()
            image.save(
                thumbnail_io,
                format="JPEG" if extension.lower() == "jpg" else "PNG",
                quality=100)  
        
        thumbnail_name = f"{image_name}_thumb{height}px{extension.lower()}"
        thumb_file = SimpleUploadedFile(
            thumbnail_name,
            thumbnail_io.getvalue(),
            content_type="image/jpeg" if extension.lower() == "jpg" else "image/png")
        instance.image.save(thumbnail_name, thumb_file, save=False)
