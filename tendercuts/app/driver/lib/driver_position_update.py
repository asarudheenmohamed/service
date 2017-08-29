"""Driver  Locations related actions."""
from app.driver.lib.geo_locations import GeoLocations

from .driver_controller import DriverController


class DriverLocations(object):
    """Driver Locations controller."""

    def __init__(self, driver):
        """Initialize the driver objects."""
        self.driver = driver

    def update_driver_position(self, order_id, lat, lon):
        """Update driver locations.

        Params:
         order_id(int): Sales flat order id
         lat(int): locations latitude
         longitude(int): locations longitude

        Retuns:
         Returns a Order Events object

        """
        controller = DriverController(self.driver)
        controller.driver_position(lat, lon)

        location = GeoLocations()
        location = location.get_location(lat, lon)

        sales_obj = controller.get_order_obj(order_id)
        obj = controller.order_events(
            location, sales_obj.status)

        return obj
