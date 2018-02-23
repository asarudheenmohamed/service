"""tendercuts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
# Uncomment the next two lines to enable the admin:

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'core/', include('app.core.urls')),
    url(r'driver/', include('app.driver.urls')),
    url(r'user/', include('app.login.urls')),
    url(r'sale_order/', include('app.sale_order.urls')),
    url(r'inventory/', include('app.inventory.urls')),
    url(r'payment/', include('app.payment.urls')),
    url(r'tcash/', include('app.tcash.urls')),
    url(r'otp/', include('app.otp.urls')),
    url(r'store_manager/', include('app.store_manager.urls'))
]
