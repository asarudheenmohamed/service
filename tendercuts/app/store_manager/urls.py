"""URLS for driver app."""

from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(
    r'store_data',
    views.StoreOrderViewSet,
    base_name='StoreOrderViewSet')

router.register(
    r'driver_lat_lon',
    views.DriverLocationViewSet,
    base_name='DriverLocationViewSet')

urlpatterns = [
	url(r'', include(router.urls)),
    url(r'login', views.StoreManagerLoginApi.as_view()),
]
