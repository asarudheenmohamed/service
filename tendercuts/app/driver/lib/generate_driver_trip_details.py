
import logging
import logging

from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
from datetime import date, timedelta
from ..models import OrderEvents
import csv
from app.core.lib.communication import Mail

logger = logging.getLogger(__name__)

from app.core.models.entity import EavAttribute
from app.core.models.customer import address
from app.driver.lib.end_of_day_driver_status import DriverStatusController
from datetime import datetime
logger = logging.getLogger(__name__)


class TripDetailsController(object):
    """Driver controller."""

    def __init__(self):
        """Constructor."""
        pass

    def generate_csv(self):
        """Generate a csv file."""

        open_file = open('end_of_day_driver_trip_details.csv', 'wb')
        csv_writer = csv.writer(open_file)

        logger.debug('csv file generated')

        return csv_writer, open_file

    def generate_trip_details(self):
        """Update customer current location."""
        driver_trip_objects = DriverTrip.objects.filter(
            trip_created_time__start_with=datetime.now.date(),
            trip_ending_time=datetime.now())
        # csv_writer, open_csv_file = self.generate_csv()
        # add header row for csv file
        csv_writer.writerow(
            ['driver name', 'trip id', 'Trip created time', 'Trip ending Time', 'km travelled', 'Trip status'])
        for trip in driver_trip_objects:

            trip_orders = trip.driver_order.values_list(
                'driver_id', 'increment_id')
            order_ids = [order[1] for order in trip_orders]

            driver_basic_info = CustomerSearchController.load_cache_basic_info(
                trip_orders.last()[0])

            sale_order_objects = SalesFlatOrder.objects.filter(
                increment_id__in=order_ids)
            [[order.increment_id, order.created_at, order.updated_at, order.status]
                for order in sale_order_objects]

            csv_writer.writerow(
                [driver_basic_info['name'], trip.id, trip.trip_created_time, trip.trip_ending_time, trip.km_traveled, trip.status])

        df = pd.DataFrame(self.csvdict)
        writer = pandas.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='trip_details')
        writer.save()
