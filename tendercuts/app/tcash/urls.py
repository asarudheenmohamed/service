from django.conf.urls import include
from django.conf.urls import url

from . import views
from rest_framework.authtoken import views as rest_framework_views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'referral', views.RewardPointAmountApi.as_view()),
    url(r'code', views.GetReferralCodeApi.as_view())
]
