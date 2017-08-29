"""URLS for driver app."""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(
    r'assign',
    views.DriverOrdersViewSet,
    base_name='DriverOrderViewSet')
router.register(
    r'unassign',
    views.UnassignOrdersViewSet,
    base_name='UnassignOrderViewSet')
router.register(
    r'orders',
    views.OrderFetchViewSet,
    base_name='DriverOrderViewSet')
router.register(
    r'fetch_related_order',
    views.FetchRelatedOrder,
    base_name='FetchRelatedViewSet')
router.register(
    r'driver_position',
    views.DriverPositionViewSet,
    base_name='DriverPositiontViewSet')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'login', views.DriverLoginApi.as_view())
]
