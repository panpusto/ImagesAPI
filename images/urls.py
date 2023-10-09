from django.urls import path
from .views import ImageListCreateAPIVIew


urlpatterns = [
    path('', ImageListCreateAPIVIew.as_view(), name="images"),
]
