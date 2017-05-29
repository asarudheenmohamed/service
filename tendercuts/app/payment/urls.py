"""
Sub urls of "payment"
"""
from . import views
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
# only viewset have to be registered!!
router.register(r'modes',
                views.PaymentMethodViewSet,
                base_name="PaymentMethodViewSet")

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'verify', views.VerifyTransaction.as_view()),
    url(r'juspay', views.JusPayApprovalCallBack.as_view()),
    url(r'done', views.juspay_done, name="juspay_done"),
]
