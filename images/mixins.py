import uuid
import time
from django.core import signing
from django.urls import reverse
from rest_framework.exceptions import NotFound
from .models import ExpiringLink

class ExpiringLinkMixin:
    def generate_expiring_link(self, image, expiration_time):
        """
        Generates expiring link with expiration time
        for uploaded image.
        """
        pk = uuid.uuid4()
        signed_link = signing.dumps(str(pk))

        full_url = self.request.build_absolute_uri(reverse("expiring_link_detail", kwargs={'signed_link': signed_link}))

        current_time = int(time.time())
        exp_time = current_time + int(expiration_time)

        ExpiringLink.objects.create(
            id=pk,
            link=full_url,
            image=image,
            expiration_time=exp_time
        )

        return {"link": full_url}
    
    @staticmethod
    def decode_signed_value(value):
        """Decodes signed link."""
        try:
            return signing.loads(value)
        except signing.BadSignature:
            raise NotFound("Invalid signed link.")
