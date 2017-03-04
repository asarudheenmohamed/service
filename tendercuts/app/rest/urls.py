from django.conf.urls import url, include

from . import views

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
   url(r'^', include(router.urls)),
    url(r'^get_route/$', views.RestApi.as_view()),
]