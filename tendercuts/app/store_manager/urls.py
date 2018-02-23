"""URLS for driver app."""

from django.conf.urls import url, include
from . import views



urlpatterns = [
    url(r'login', views.StoreManagerLoginApi.as_view()),
]
