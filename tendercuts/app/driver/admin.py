"""Returns custom objects to the Driver order admin."""
from django.contrib import admin

from app.driver.models import DriverTrip, DriverLoginLogout


class DriverTripAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DriverTrip._meta.fields]


class DriverLoginLogoutAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DriverLoginLogout._meta.fields]


admin.site.register(DriverTrip, DriverTripAdmin)
admin.site.register(DriverLoginLogout, DriverLoginLogoutAdmin)
