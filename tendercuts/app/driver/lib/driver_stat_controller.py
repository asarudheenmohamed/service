"""All driver status controller related actions."""
from app.driver.models import DriverOrder, DriverStat


class DriverStatController(object):
    """Driver controller."""

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
            driver = DriverOrder.objects.filter(increment_id=order_id)
            driver_stats = DriverStat.objects.get_or_create(
                    driver_id=driver[0].driver_id)
            driver_stats[0].no_of_orders += 1
            driver_stats[0].save()
        except ValueError:
            print "This order was not placed"

        return driver_stats[0].no_of_orders
