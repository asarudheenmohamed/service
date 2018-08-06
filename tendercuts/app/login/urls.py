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


urlpatterns = [
    url(r'', include(router.urls)),
    url(r'login', views.UserLoginApi.as_view()),
    url(r'signup', views.UserSignUpApi.as_view()),
    url(r'fetch', views.UserDataFetch.as_view()),
    url(r'exists', views.UserExistsApi.as_view()),
    url(r'change_password', views.UserChangePassword.as_view()),
    url(r'edit_profile', views.EditProfile.as_view()),
    url(r'version_control', views.VersionControl.as_view()),
]
