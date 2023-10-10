from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Image
from .tasks import generate_thumbnails


@receiver(post_save, sender=Image)
def create_thumbnails(sender, instance: Image, **kwargs):
    """
    Creates thumbanails for uploaded images 
    after saving image to db.
    """
    generate_thumbnails.delay(instance.id)
