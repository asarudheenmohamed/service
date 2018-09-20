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
        inv = Graminventory.objects.get(
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
            self.inv.qty = request.qty
            type = "qty"
        else:
            old_qty = self.inv.forecastqty
            self.inv.forecastqty = request.qty
            type = "forecastqty"

        # inventory log
        self.inv.save()

        return Inventorylog.objects.create(
            sku=request.sku,
            createdat=datetime.datetime.now(),
            message=message,
            stockupdatedfrom=old_qty,
            stockupdatedto=request.qty,
            store_id=request.store_id,
            type_of_qty=type
        )


class InventoryRequestController:
    def __init__(self, request):
        self.request = request

    def approve(self, message=""):

        # double check if no orders are pending
        if self.request.status == InventoryRequest.Status.CREATED.value:
            return

        inv_controller = InventoryController.get_controller_from_request(self.request)
        inv_controller.process_inventory_request(self.request, message)

        # update status
        self.request.status = InventoryRequest.Status.APPROVED.value
        self.request.save()

    def reject(self):
        # update status
        self.request.status = InventoryRequest.Status.REJECTED.value
        self.request.save()

