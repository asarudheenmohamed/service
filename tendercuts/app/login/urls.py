from django.conf.urls import url, include

from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views

router = DefaultRouter()
# only viewset have to be registered!!
router.register(r'otp', views.OtpApiViewSet)

urlpatterns = [
   url(r'', include(router.urls)),
   url(r'login', views.UserLoginApi.as_view()),
   url(r'signup', views.UserSignUpApi.as_view()),
]