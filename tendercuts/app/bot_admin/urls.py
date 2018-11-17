# Create your views here.
from django.conf.urls import include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'flock_callback', views.FlockAppApi.as_view()),
    url(r'dialogflow_callback', views.DialogFlowAppApi.as_view())
]
