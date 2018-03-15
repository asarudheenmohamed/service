"""Returns custom objects to the Driver order admin."""
from django.contrib import admin

from app.driver.models import DriverTrip


class DriverTripAdmin(admin.ModelAdmin):
    list_display = [f.name for f in DriverTrip._meta.fields]


admin.site.register(DriverTrip, DriverTripAdmin)
