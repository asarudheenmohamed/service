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
    r'customer_orders',
    views.SalesOrderViewSet,
    base_name='SalesOrderViewSet')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'update_address', views.UpdateAddressApi.as_view()),
    url(r'search_customer', views.SearchCustomerApi.as_view()),
    url(r'freshdesk_tickets', views.FreshDeskTicketApi.as_view()),
    url(r'sale_order_location', views.SaleOrderLocationAPI.as_view())
]
