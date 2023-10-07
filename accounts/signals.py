from django.dispatch import receiver
from django.db.models.signals import post_migrate
from .models import AccountTier
from images.models import ThumbnailSize
from .default_tiers import DEFAULT_TIERS as dflt_trs


@receiver(post_migrate)
def create_default_tiers(sender, **kwargs):
    """
    Creates default tiers after db migration.
    """
    if sender.name == "accounts":
        if AccountTier.objects.filter(name="Basic").exists():
            return
        
        # basic tier
        basic = AccountTier.objects.create(
            name="Basic",
            is_expiration_link=dflt_trs["Basic"]["is_expiration_link"],
            is_original_file=dflt_trs["Basic"]["is_original_file"]
        )
        basic_thumbs = ThumbnailSize.objects.create(
            height=dflt_trs["Basic"]["thumbnail_size"]["height"]
        )
        basic.thumbnail_size.add(basic_thumbs)
        basic.save()


        # premium tier
        premium = AccountTier.objects.create(
            name="Premium",
            is_expiration_link=dflt_trs["Premium"]["is_expiration_link"],
            is_original_file=dflt_trs["Premium"]["is_original_file"]
        )
        premium_thumbs = ThumbnailSize.objects.create(
            height=dflt_trs["Premium"]["thumbnail_size"]["height"]
        )
        premium.thumbnail_size.set([
            basic_thumbs,
            premium_thumbs
        ])
        premium.save()


        # enterprise tier
        enterprise = AccountTier.objects.create(
            name="Enterprise",
            is_expiration_link=dflt_trs["Enterprise"]["is_expiration_link"],
            is_original_file=dflt_trs["Enterprise"]["is_original_file"]
        )
        enterprise.thumbnail_size.set([
            basic_thumbs,
            premium_thumbs
        ])
        enterprise.save()
