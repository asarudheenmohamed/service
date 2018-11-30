"""User object map in all driver models."""
from app.driver.models.driver_order import DriverOrder, DriverTrip, DriverPosition
from django.contrib.auth.models import User


class DrivermapController(object):

    def username_format(self, driver_id):
        return "u:{}".format(driver_id)

    def user_map_driver_order(self):
        """User Object map in all driver order models."""
        driver_orders = DriverOrder.objects.all()
        for driver_order in driver_orders:
            username = self.username_format(driver_order.driver_id)
            user = User.objects.filter(username=username)[0]
            driver_order.driver_user = user
            driver_order.save()

    def user_map_driver_position(self):
        """User object map in all DriverPosition."""
        driver_positions = DriverPosition.objects.all()
        for driver_position in driver_positions:
            username = self.username_format(driver_position.driver_id)
            user = User.objects.filter(username=username)[0]
            driver_position.driver_user = user
            driver_position.save()

    def user_map_driver_trip(self):
        """User onject map in all DriverTrip objects."""
        driver_trip_objects = DriverTrip.objects.all()
        for driver_trip in driver_trip_objects:
            username = self.username_format(
                driver_trip.driverorder.all().first().driver_id)
            user = User.objects.filter(username=username)[0]
            driver_trip.driver_user = user
            driver_trip.save()

    def user_map_driver_stat(self):
        """User onject map in all DriverTrip objects."""
        driver_stat_objects = DriverStat.objects.all()
        for driver_stat in driver_stat_objects:
            username = self.username_format(
                driver_stat.driver_id)
            user = User.objects.filter(username=username)[0]
            driver_stat.driver_user = user
            driver_stat.save()
