from app.core.models.sales_order import *
from app.core.models.ddate import *

def test_orders(auth_rest):
    order_id = 76106
    orders = SalesFlatOrder.objects.filter(entity_id=order_id)
    assert "9:00-11:00" == orders[0].schedule.ddate.dtimetext
    assert orders[0].promised_delivery_time() == "Feb 02, Thu 11:00 AM"
