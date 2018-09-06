"""URLS for driver app."""

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(
    r'sale_order',
    views.SalesOrderDetailSet,
    base_name='SalesOrderDetailSet')

urlpatterns = [
    url(r'', include(router.urls)),
]
