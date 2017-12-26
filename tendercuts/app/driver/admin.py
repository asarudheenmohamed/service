"""Returns custom objects to the Driver order admin."""
from django.contrib import admin

from app.core.models.store import CoreStore
from app.driver.lib.store_order_controller import StoreOrderController
from app.driver.models import DriverOrder, DriverTrip


class DriverOrderAdmin(admin.ModelAdmin):
    """Driver order change view list."""
    def changelist_view(self, request):
        """Fetch driver object associated with the corresponding store.

        Args:
          store_id: store id

        Returns:
         driver obj

        """

        data = {}
        if request.method == 'POST':

            controller = StoreOrderController()
            data = controller.get_store_driver_order(request.POST['store_id'])

        data['store_obj'] = CoreStore.objects.all()
        response = super(DriverOrderAdmin, self).changelist_view(
            request,
            extra_context=data
        )

        return response

admin.site.register(DriverOrder, DriverOrderAdmin)

class DriverTripAdmin(admin.ModelAdmin):
    list_display  = [f.name for f in DriverTrip._meta.fields]


admin.site.register(DriverTrip, DriverTripAdmin)
