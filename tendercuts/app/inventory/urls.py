from django.conf.urls import url, include
from django.conf import settings
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views


urlpatterns = [
   url(r'store', views.InventoryViewSet.as_view()),
]
