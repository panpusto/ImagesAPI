from django.urls import path
from .views import (
    ImageListCreateAPIVIew,
    ExpiringLinkListCreateAPIView,
    ExpiringLinkDetailAPIView,
)


urlpatterns = [
    path("", ImageListCreateAPIVIew.as_view(), name="images"),
    path(
        "expiring-link/",
        ExpiringLinkListCreateAPIView.as_view(),
        name="expiring_link"),
    path(
        "expiring-link/<str:signed_link>/",
        ExpiringLinkDetailAPIView.as_view(),
        name="expiring_link_detail"
    ),
]
