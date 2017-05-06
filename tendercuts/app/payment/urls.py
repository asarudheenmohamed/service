from . import views
from django.conf.urls import url, include

urlpatterns = [
    url(r'verify', views.VerifyTransaction.as_view()),
    url(r'juspay', views.JusPayApprovalCallBack.as_view())
]
