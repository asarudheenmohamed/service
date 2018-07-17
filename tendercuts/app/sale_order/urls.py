from django.conf.urls import url, include
from django.conf import settings
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# only viewset have to be registered!!
router.register(r'orders',
                views.SalesOrderViewSet,
                base_name="SalesOrderViewSet")
# router.register(r'product', views.ProductViewSet)#,
# base_name='CatalogProductEntity')
router.register(
    r'quote_items',
    views.QuoteItemViewSet,
    base_name='QuoteItemViewSet')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'delivery_slots', views.DeliveryViewSet.as_view()),
    url(r'order_data', views.OrderDataViewSet.as_view()),
    url(r'store_order', views.StoreDataViewSet.as_view()),
    url(r'item_weight', views.OrderItemWeightUpdateViewSet.as_view()),

]
