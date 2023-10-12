import pytest 
import shutil
from io import BytesIO
from PIL import Image as pilImg
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import AccountTier
from .models import Image, ThumbnailSize, ExpiringLink


@pytest.mark.django_db
class TestImageModel:

    @pytest.fixture
    def user(self):
        tier = AccountTier.objects.get(name="Premium")
        user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@email.com",
            password="testpass123",
            account_tier=tier
        )
        return user

    @pytest.fixture
    def image(self, user):
        image_file = "../test_images/furia_lp.jpg"
        image = Image.objects.create(
            image=image_file,
            user=user
        )
        return image
    
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


@pytest.fixture
def enterprise_user():
    enterprise_account = AccountTier.objects.get(name="Enterprise")
    user = get_user_model().objects.create_user(
        username="enterprise_testuser",
        email="enterprise_testuser@email.com",
        password="testpass123",
        account_tier=enterprise_account
    )
    return user

@pytest.fixture
def basic_user():
    basic_account = AccountTier.objects.get(name="Basic")
    user = get_user_model().objects.create_user(
        username="basic_testuser",
        email="basic_testuser@email.com",
        password="testpass123",
        account_tier=basic_account
    )
    return user

@pytest.fixture
def client(enterprise_user):
    client = APIClient()
    client.login(username="enterprise_testuser", password="testpass123")
    return client

@pytest.fixture
def image_file():
    file = BytesIO()
    image = pilImg.new("RGB", size=(500, 500), color=(155, 0, 0))
    image.save(file, "jpeg")
    file.name = "test.jpeg"
    file.seek(0)
    return SimpleUploadedFile("test.jpeg", file.read())

@pytest.fixture
def image(client, enterprise_user, image_file):
    return Image.objects.create(image=image_file, user=enterprise_user)

@pytest.fixture
def expiring_link(client, image):
    url = reverse("expiring_link")
    data = {"image": image.id, "expiration_time": 500}
    response = client.post(url, data, format="json")
    return response.data.get("link")


# temporary directory for tests
TEST_DIR = "test_data"

@pytest.mark.django_db
class TestImageAPI:
    @override_settings(MEDIA_ROOT=(TEST_DIR + "/media"))
    def test_upload_image(self, client, image_file):
        url = reverse("images")
        data = {"image": image_file}
        response = client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_201_CREATED
        assert Image.objects.count() == 1

    def test_image_list_for_logged_in_user(self, client):
        url = reverse("images")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_image_list_for_logged_out_user(self, client):
        client.logout()
        url = reverse("images")
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_image_create_for_logged_out_user(self, client, image_file):
        client.logout()
        url = reverse("images")
        data = {"image": image_file}
        response = client.post(url, data, format="multipart")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Image.objects.count() != 1


@pytest.mark.django_db
class TestExpiringLinkAPI:
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_create_expiring_link(self, client, image, enterprise_user):
        url = reverse("expiring_link")
        data = {"image": image.id, "expiration_time": 300}
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert ExpiringLink.objects.count() == 1
        assert Image.objects.first().user == enterprise_user

    def test_list_exp_link_for_authorized_user(self, client, expiring_link):
        url = reverse("expiring_link")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_list_exp_link_for_unauthorized_user(self, client, basic_user):
        client.login(username="basic_testuser", password="testpass123")
        url = reverse("expiring_link")
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    @override_settings(MEDIA_ROOT=(TEST_DIR + "/media"))
    def test_exp_link_detail_for_authorized_user(self, client, image_file, enterprise_user):
        image = Image.objects.create(
            image=image_file,
            user=enterprise_user
        )
        url = reverse("expiring_link")
        data = {"image": image.id, "expiration_time": 300}
        response = client.post(url, data, format="json")
        link = response.data.get("link").split("/")[-2]
        url = reverse("expiring_link_detail", kwargs={"signed_link": link})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @override_settings(MEDIA_ROOT=(TEST_DIR + "/media"))
    def test_exp_link_detail_for_unauthorized_user(self, client, image_file, enterprise_user):
        image = Image.objects.create(
            image=image_file,
            user=enterprise_user
        )
        url = reverse("expiring_link")
        data = {"image": image.id, "expiration_time": 300}
        response = client.post(url, data, format="json")
        link = response.data.get("link").split("/")[-2]
        url = reverse("expiring_link_detail", kwargs={"signed_link": link})
        client.logout()
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_teardown(self):
        print('\nDeleting temporary files...\n')
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
