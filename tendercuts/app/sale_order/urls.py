from django.conf.urls import url, include
from django.conf import settings
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# only viewset have to be registered!!
router.register(r'orders', views.SalesOrderViewSet)
# router.register(r'product', views.ProductViewSet)#, base_name='CatalogProductEntity')

urlpatterns = [
   url(r'', include(router.urls)),
]

