import pytest
from django.contrib.auth import get_user_model
from .models import AccountTier
from images.models import ThumbnailSize

@pytest.mark.django_db
class TestClassAccounts:
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username="test_user",
            email="test_user@email.com",
            password="testpass123"
        )
        assert get_user_model().objects.count() == 1
        assert user.username == "test_user"
        assert user.email == "test_user@email.com"
        assert user.is_staff == False
        assert user.is_superuser == False
    
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@email.com",
            password="testpass123"
        )
        assert get_user_model().objects.count() == 1
        assert user.username == "admin"
        assert user.email == "admin@email.com"
        assert user.is_staff == True
        assert user.is_superuser == True

    @pytest.fixture
    def basic_user(self):
        user = get_user_model().objects.create_user(
            username="basic_user",
            email="basic_user@email.com",
            password="testpass123"
        )
        basic_tier = AccountTier.objects.get(name="Basic")
        user.account_tier = basic_tier

        return user
    
    @pytest.fixture
    def premium_user(self):
        user = get_user_model().objects.create_user(
            username="premium_user",
            email="premium_user@email.com",
            password="testpass123"
        )
        premium_tier = AccountTier.objects.get(name="Premium")
        user.account_tier = premium_tier

        return user
    
    @pytest.fixture
    def enterprise_user(self):
        user = get_user_model().objects.create_user(
            username="enterprise_user",
            email="enterprise_user@email.com",
            password="testpass123"
        )
        enterprise_tier = AccountTier.objects.get(name="Enterprise")
        user.account_tier = enterprise_tier

        return user
    
    def test_user_account_tier(self, basic_user, premium_user, enterprise_user):
        assert basic_user.account_tier.name == "Basic"
        assert premium_user.account_tier.name == "Premium"
        assert enterprise_user.account_tier.name == "Enterprise"


@pytest.mark.django_db
class TestClassAccountTier:
    @pytest.fixture
    def basic_tier(self):
        tier = AccountTier.objects.get(name="Basic")
        return tier
    
    @pytest.fixture
    def premium_tier(self):
        tier = AccountTier.objects.get(name="Premium")
        return tier
    
    @pytest.fixture
    def enterprise_tier(self):
        tier = AccountTier.objects.get(name="Enterprise")
        return tier
    
    def test_user_tier_has_expiration_link(self, basic_tier, premium_tier, enterprise_tier):
        assert basic_tier.is_expiration_link == False
        assert premium_tier.is_expiration_link == False
        assert enterprise_tier.is_expiration_link == True
    
    def test_user_tier_has_original_file(self, basic_tier, premium_tier, enterprise_tier):
        assert basic_tier.is_original_file == False
        assert premium_tier.is_original_file == True
        assert enterprise_tier.is_original_file == True

    def test_user_tier_thumbs_size(self, basic_tier, premium_tier, enterprise_tier):
        basic_thumbs = basic_tier.thumbnail_size.all()
        premium_thumbs = premium_tier.thumbnail_size.all()
        enterprise_thumbs = enterprise_tier.thumbnail_size.all()
        assert len(basic_thumbs) == 1
        assert len(premium_thumbs) == 2
        assert len(enterprise_thumbs) == 2
        assert basic_thumbs[0].height == 200
        assert premium_thumbs[0].height == 200
        assert premium_thumbs[1].height == 400
        assert enterprise_thumbs[0].height == 200
        assert enterprise_thumbs[1].height == 400

    def test_create_custom_tier(self):
        thumb = ThumbnailSize.objects.create(height=200)
        custom_tier = AccountTier.objects.create(
            name="Custom",
            is_expiration_link=True,
            is_original_file=True
        )
        custom_tier.thumbnail_size.set([thumb])
        custom_tier.save()
        thumbnail_instance = custom_tier.thumbnail_size.first()
        assert custom_tier.name == "Custom"
        assert custom_tier.is_expiration_link == True
        assert custom_tier.is_original_file == True
        assert thumbnail_instance.height == 200
