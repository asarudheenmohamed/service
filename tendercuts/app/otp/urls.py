from django.conf.urls import url, include

from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views
router = DefaultRouter()
# only viewset have to be registered!!

# Unified OTP API
router.register(r'generate', views.OtpGenerateApi, base_name='otp_geneate')
router.register(r'verify', views.OtpVerifyApi, base_name='otp_verify')
router.register(r'retry', views.OtpRetryApi, base_name='otp_retry')

urlpatterns = [
    url(r'', include(router.urls)),
]
