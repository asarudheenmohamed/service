import datetime

from app.core.models import Graminventory
from app.inventory.models import Inventorylog, InventoryRequest


class InventoryController:
    """A wrapper on top of inventory controller"""

    @classmethod
    def get_controller(cls, store_id, product_id, date):
        """Get the inventory record

        :param store_id (int):
        :param product_id(int):
        :param date (date):
        :return:
        """
        inv, _ = Graminventory.objects.get_or_create(
            product_id=product_id,
            store_id=store_id,
            date=date
        )

        if not inv:
            return

        return cls(inv)

    @classmethod
    def get_controller_from_request(cls, request):
        """Get the inventory record from inventory request

        :param request (InventoryRequest):
        :return:
        """
        return cls.get_controller(
            store_id=request.store_id,
            product_id=request.product_id,
            date=request.created_time.date()
        )

    def __init__(self, inv):
        """

        :type inv: Graminventory
        """
        self.inv = inv

    def process_inventory_request(self, request, message=""):
        """Updates scheduled inventory
        :action OptimizeImports

        :type request: InventoryRequest
        """
        if request.type == InventoryRequest.INV_TYPE.TODAY.value:
            old_qty = self.inv.qty
            new_qty = round((request.qty * request.gpu) / 1000.0, 2)
            self.inv.qty = new_qty
            type = "qty"
        else:
            old_qty = self.inv.forecastqty
            new_qty = round((request.qty * request.gpu) / 1000.0, 2)
            self.inv.forecastqty = new_qty
            type = "forecastqty"

        # inventory log
        self.inv.save()

        return Inventorylog.objects.create(
            sku=request.sku,
            createdat=datetime.datetime.now(),
            message=message,
            stockupdatedfrom=old_qty,
            stockupdatedto=new_qty,
            store_id=request.store_id,
            type_of_qty=type
        )


class InventoryRequestController:

    @classmethod
    def auto_approve_expired_request(cls, test_mode=False):
        start = datetime.date.today()
        end = datetime.datetime.now() - datetime.timedelta(minutes=15)
        if test_mode:
            end = datetime.datetime.now()

        requests = InventoryRequest.objects.filter(
            created_time__gt=start,
            created_time__lte=end,
            status=InventoryRequest.Status.CREATED.value
        )

        for request in requests:  # type: InventoryRequest
            message = "Marked done automatically for request raised by {}".format(
                request.triggered_by.email
            )
            req_controller = cls(request)
            req_controller.approve(message)

        return requests

    def __init__(self, request):
        self.request = request

    def approve(self, message):
        self.request.status = InventoryRequest.Status.APPROVED.value;
        self.request.save()

        self._process_inventory(message)

    def reject(self):
        self.request.status = InventoryRequest.Status.REJECTED.value;
        self.request.save()

    def _process_inventory(self, message):
        """Core method to process the inventory."""
        # double check if no orders are pending
        if self.request.status == InventoryRequest.Status.CREATED.value:
            return

        inv_controller = InventoryController.get_controller_from_request(self.request)
        log = inv_controller.process_inventory_request(self.request, message)

    def process_request(self, message=""):
        """Called from the view, the values are already updated, so we only
        process the inventory"""
        if self.request.status == InventoryRequest.Status.APPROVED.value:
            self._process_inventory(message)
