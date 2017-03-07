from django.conf.urls import url, include

from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# only viewset have to be registered!!
router.register(r'store', views.StoreViewSet)

urlpatterns = [
   url(r'', include(router.urls)),
]
