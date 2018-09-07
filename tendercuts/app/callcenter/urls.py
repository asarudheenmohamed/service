"""URLS for driver app."""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(
    r'sale_detail',
    views.SalesOrderDetailSet,
    base_name='SalesOrderDetailSet')

router.register(
    r'update_address',
    views.UpdateAddressApi,
    base_name='UpdateAddressApi')

urlpatterns = [
    url(r'', include(router.urls)),
]
