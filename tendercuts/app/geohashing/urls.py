"""URLS for geohashing."""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'store_details', views.StoreDetailView.as_view()),
    url(r'store', views.GeohashToStore.as_view()),
]
