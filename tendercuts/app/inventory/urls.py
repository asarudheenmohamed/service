from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(
    r'notify_me',
    views.CustomerNotificationViewSet,
    base_name='CustomerNotificationViewSet')

urlpatterns = [
   url(r'', include(router.urls)),
   url(r'store', views.InventoryViewSet.as_view()),
   url(r'^upload/(?P<filename>[^/]+)$', views.InventoryUploadView.as_view())
]
