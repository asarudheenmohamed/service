"""Send an email that includes driver details."""
import sys
import xlrd
import os
import csv


# import gen_py.lib
import logging

from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
import csv
from app.core.lib.communication import Mail


from app.driver.models.driver_order import *

from datetime import date, timedelta
import itertools
from django.conf import settings
import googlemaps


logger = logging.getLogger(__name__)


class DriverTripController(object):
    """Generates a csv file that includes driver details worked on current date."""

    def __init__(self):
        """Constructor."""
        self.log = logging.getLogger()
        self.api = googlemaps.Client(
            key=settings.GOOGLE_MAP_DISTANCE_API['KEY'])

    def generate_csv(self):
        """Generate a csv file."""

        open_file = open('end_of_day_driver_trip.csv', 'wb')
        csv_writer = csv.writer(open_file)

        logger.debug('csv file generated')

        return csv_writer, open_file

    def fetch_order_status(self, increment_ids):
        """Fetch the sale order object using order id's and apply filter to identify the store name where id belongs.

        Params:
         increment_ids(list): order increment id's

        Returns:
           list of order status

        """
        sale_objects = SalesFlatOrder.objects.filter(
            increment_id__in=increment_ids)

        logger.debug(
            "Fetched the sale order objects for that list of order id's")

        order_status = {}
        complete_orders = []
        canceled_orders = []
        closed_orders = []
        for order_obj in sale_objects:
            if order_obj.status == 'complete':
                complete_orders.append(order_obj.increment_id)
            elif order_obj.status == 'canceled':
                canceled_orders.append(order_obj.increment_id)
            elif order_obj.status == 'closed':
                closed_orders.append(order_obj.increment_id)

        order_status['complete_orders'] = ', '.join(complete_orders)
        order_status['canceled_orders'] = ', '.join(canceled_orders)
        order_status['closed_orders'] = ', '.join(closed_orders)

        return order_status

    def calculate_trip_distance(self, driver_id):
        """calculate trip distance."""
        start_date = date.today()
        end_date = date.today() + timedelta(days=1)

        driver_orders = DriverOrder.objects.filter(
            driver_id=driver_id, created_at__range=(
                start_date, end_date))

        trip_objects = DriverTrip.objects.filter(
            driver_order__in=driver_orders)
        trip_objects = set(trip_objects)
        csv_writer, open_csv_file = self.generate_csv()

        # add header row for csv file
        csv_writer.writerow(['Driver name',
                             'Phone',
                             'Order ids',
                             'km_traveled',
                             'Completed Orders',
                             'Canceled Orders',
                             'Closed Orders'])
        driver_basic_info = CustomerSearchController.load_cache_basic_info(
            driver_id)

        for trip in trip_objects:

            trip_orders_status = self.fetch_order_status(
                [order.increment_id for order in trip.driver_order.all()])

            events = OrderEvents.objects.filter(driver__in=trip.driver_order.all(
            )).prefetch_related('driver_position').order_by('updated_time')

            # starting and ending destination point
            starting_point = events.first().driver_position
            destination_point = events.last().driver_position

            # trip starting point
            trip_starting_time = events.first().updated_time

            # sort completed order only because we get a order completed
            # location and completed time
            event_complete_objects = events.filter(status='completed')
            way_points = []

            for complete_object in event_complete_objects:

                # fetch driver position
                position_objects = DriverPosition.objects.filter(
                    driver_id=driver_id, recorded_time__range=(
                        trip_starting_time, complete_object.updated_time))

                mid_index = len(position_objects) / 2
                mid_position = position_objects[mid_index]
                way_points.append(str(mid_position))
                way_points.append(str(complete_object.driver_position))

                trip_starting_time = complete_object.updated_time

            try:
                compute_km = self.api.directions(starting_point, destination_point,
                                                 waypoints=way_points)
                self.log.info(
                    'Measured the km taken for the trip by the driver using google api with way points travlled from starting point :{} to ending point :{} for a trip '.format(
                        starting_point, destination_point))

                # update trip kmc
                km_traveled = 0
                for leg in compute_km[0]['legs']:
                    km_traveled += int(leg['distance']['value'])

            except Exception as msg:
                self.log.error('{}, trip_id:{}'.format(repr(msg), trip.id))

            csv_writer.writerow([
                driver_basic_info['name'],
                driver_basic_info['phone'],
                trip.id,
                km_traveled,
                trip_orders_status['completed_orders'],
                trip_orders_status['canceled_orders'],
                trip_orders_status['closed_orders']])

        open_csv_file.close()
        Mail().send(
            "reports@tendercuts.in",
            ["asarudheen@tendercuts.in"],
            'Driver details',
            "Here the attachement includes driver details at end of day",
            ["end_of_day_driver_trip.csv"])

        self.log.info(
            "The driver details csv file has been sent to the following mail id asarudheen@tendercuts.in")
