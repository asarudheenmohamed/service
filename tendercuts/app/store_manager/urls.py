"""URLS for driver app."""

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'login', views.StoreManagerLoginApi.as_view()),
    url(r'store_data', views.store_orders, name="store_data"),
    url(r'driver_lat_lon', views.driver_lat_lon, name="driver_lat_lon"),
]
