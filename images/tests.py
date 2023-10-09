import pytest 
from django.contrib.auth import get_user_model
from accounts.models import AccountTier
from .models import Image, ThumbnailSize


@pytest.fixture
def user():
    tier = AccountTier.objects.get(name="Enterprise")
    user = get_user_model().objects.create_user(
        username="test_user",
        email="test_user@email.com",
        password="testpass123",
        account_tier=tier
    )
    return user

@pytest.fixture
def image(user):
    image_file = "../test_images/furia_lp.jpg"
    image = Image.objects.create(
        image=image_file,
        user=user
    )
    return image


@pytest.mark.django_db
class TestImageModel:
    def test_image_owner(self, image):
        assert image.user.username == "test_user"
        assert image.user.email != "noname@email.com"

    def test_get_filename(self, image):
        assert image.get_filename() == "furia_lp"
        assert image.get_filename() != "furia"
    
    def test_str_method(self, image):
        assert image.__str__() == "furia_lp"
        assert image.__str__() != "furia"


@pytest.mark.django_db
class TestThumbnailSizeModel:
    def test_create_thumbnail_size(self):
        thumb_size = ThumbnailSize.objects.create(height=100)
        assert thumb_size.height == 100
        assert thumb_size.height != 300
        assert ThumbnailSize.objects.count() == 3


# add tests for ExpiringLink and api later
