from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^my-own-view/$', views.RestApi.as_view()),
]