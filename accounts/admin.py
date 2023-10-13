from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AccountTier


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "account_tier"
    )

    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Account Tier", {"fields": ("account_tier",)}),
        ("Additional Stats", {"fields": ("last_login", "date_joined")})
    )
    add_fields = (
        (None, {"fields": ("email", "password")}),
        ("Account Tier", {"fields": ("account_tier",)})
    )


@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "thumbnail_size_for_admin_site",
        "is_expiration_link",
        "is_original_file"
    )