from django.contrib import admin
from .models import Image, ThumbnailSize, ExpiringLink


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "upload_date"
    )
    ordering = ("-upload_date",)


@admin.register(ThumbnailSize)
class ThumbnailSizeAdmin(admin.ModelAdmin):
    ordering = ("height",)


@admin.register(ExpiringLink)
class ExpiringLinkAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "image"
    )
    fieldsets = (
        (None, 
            {"fields": ("image", "expiration_time"),
        }),
    )
