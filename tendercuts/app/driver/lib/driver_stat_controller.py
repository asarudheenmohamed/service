"""All driver status controller related actions."""
from app.driver.models import DriverOrder, DriverStat


class DriverStatController(object):
    """Driver stat controller."""

    def __init__(self, order):
        """Constructor."""
        self.order = order

    def generate_stat(self, order_id, status):
        """Driver status controller.

        Add the completed order to the driver.

        Params:
            order_id: increment_id

        Returns:
            no of orders in DriverStat obj


        """
        if status != "complete":
            raise ValueError("Order:{} is not completed yet".format(order_id))

        try:
            driver = DriverOrder.objects.filter(increment_id=order_id).last()
        except ValueError:
            print "This order was not placed"

        driver_stat = DriverStat.objects.get_or_create(
            driver_user=driver.driver_user)
        driver_stat[0].no_of_orders += 1
        driver_stat[0].save()

        return driver_stat[0].no_of_orders
