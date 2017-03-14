from django.conf.urls import url, include

from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
   url(r'login', views.UserLoginApi.as_view()),
   url(r'signup', views.UserSignUpApi.as_view()),
]
