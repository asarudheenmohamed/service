from django.conf.urls import url
from . import views

urlpatterns = [
   url(r'store', views.InventoryViewSet.as_view()),
   url(r'^upload/(?P<filename>[^/]+)$', views.InventoryUploadView.as_view())
]
