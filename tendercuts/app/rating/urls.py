"""URLS for rating app."""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(
    r'rating_create',
    views.ProductratingViewSet,
    base_name='OrderratingViewSet')
router.register(
    r'rating_tags',
    views.ProductRatingTagViewSet,
    base_name='ProductRatingTagsViewSet')


urlpatterns = [
    url(r'', include(router.urls)),
]
