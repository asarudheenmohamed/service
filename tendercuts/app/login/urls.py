from django.conf.urls import url, include

from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as rest_framework_views
router = DefaultRouter()
# only viewset have to be registered!!
router.register(r'otp', views.OtpApiViewSet)
router.register(r'reward', views.RewardPointsTransaction, base_name='reward')
router.register(r'mcredit', views.CreditBalance, base_name='mcredit')
router.register(r'forgot_password_otp', views.OtpForgotPasswordApiViewSet)

# Unified OTP API
router.register(r'otp_view', views.OtpApi, base_name='otp_view')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'login', views.UserLoginApi.as_view()),
    url(r'signup', views.UserSignUpApi.as_view()),
    url(r'fetch', views.UserDataFetch.as_view()),
    url(r'exists', views.UserExistsApi.as_view()),
    url(r'change_password', views.UserChangePassword.as_view()),
    url(r'edit_profile', views.EditPrifile.as_view()),
    url(r'otp_validation/(?P<mobile>\d+)',
        views.OtpValidation.as_view(),
        name='otp_validation'),
]
