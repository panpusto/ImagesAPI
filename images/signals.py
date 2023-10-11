from django.dispatch import receiver
from django.db.models.signals import post_save
from django_cleanup.signals import cleanup_pre_delete
from .models import Image
from .tasks import generate_thumbnails, cleanup_image_folder


@receiver(post_save, sender=Image)
def create_thumbnails(sender, instance: Image, **kwargs):
    """
    Creates thumbanails for uploaded images 
    after saving image to db.
    """
    generate_thumbnails.delay(instance.id)


@receiver(cleanup_pre_delete, sender=Image)
def cleanup_pre_delete_image_folder(sender, instance, **kwargs):
    cleanup_image_folder.delay(instance.image.name)
