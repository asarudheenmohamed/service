from django.conf.urls import url, include
from django.conf import settings
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# only viewset have to be registered!!
router.register(r'store', views.StoreViewSet)
router.register(
    r'destinated_store',
    views.CustomerAddressVarcharViewSet,
    base_name='CustomerAddressVarcharViewSet')

# router.register(r'product', views.ProductViewSet)#,
# base_name='CatalogProductEntity')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'product', views.ProductViewSet.as_view()),
    url(r'cart/add/', views.CartAddApi.as_view()),
    url(r'customer/', views.CustomerDataApi.as_view()),
    url(r'price/', views.ProductPriceViewSet.as_view())
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
