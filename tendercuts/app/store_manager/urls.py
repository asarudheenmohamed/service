"""URLS for driver app."""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(
    r'store_data',
    views.StoreOrderViewSet,
    base_name='StoreOrderViewSet')

router.register(
    r'trips',
    views.StoreTripViewSet,
    base_name='StoreTripViewSet')


router.register(
    r'driver_lat_lon',
    views.DriverLocationViewSet,
    base_name='DriverLocationViewcSet')

router.register(
    r'inv_request',
    views.StoreInventoryRequestApi,
    base_name='StoreInventoryRequestApi')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'login', views.StoreManagerLoginApi.as_view()),
    url(r'drivers', views.StoreDriverView.as_view()),
    url(r'routing', views.StoreRoutingView.as_view()),
    url(r'processing', views.OrderProcessingView.as_view()),
    url(r'flock_auth', views.StoreManagerFlockApi.as_view()),
    url(r'flock_app', views.FlockAppApi.as_view()),
]
