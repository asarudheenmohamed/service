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
router.register(
    r'delay_sms',
    views.DriverSmsViewSet,
    base_name='DriverSmsViewSet')
router.register(
    r'driver_stat',
    views.DriverStatViewSet,
    base_name='DriverStatViewSet')
router.register(
    r'driver_trip',
    views.DriverTripViewSet,
    base_name='DriverTripViewSet')


urlpatterns = [
    url(r'', include(router.urls)),
    url(r'login', views.DriverLoginApi.as_view()),
    url(r'product_weight/update/(?P<pk>\d+)/$',
        views.ProductWeightUpdateView.as_view())
]
