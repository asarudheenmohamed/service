from . import views
from django.conf.urls import url, include

urlpatterns = [
   url(r'simpl', views.SimplClaimTxnApi.as_view())
]
