"""Send an email that includes driver details."""

import logging

from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
from datetime import date, timedelta
from ..models import OrderEvents
import csv
from app.core.lib.communication import Mail

logger = logging.getLogger(__name__)


class DriverStatusController(object):
    """Generates a csv file that includes driver details worked on current date."""

    def __init__(self):
        """Constructor."""
        pass

    def generate_csv(self):
        """Generate a csv file."""
        open_file = open('end_of_day_driver_details.csv', 'wb')
        csv_writer = csv.writer(open_file)
        logger.debug('csv file generated')

        return csv_writer, open_file

    def fetch_driver_completed_order_store_names(self, increment_ids):
        """Fetch the sale order object using order id's and apply filter to identify the store name where id belongs.

        Params:
         increment_ids(list): order increment id's

        Returns:
           Returns a store name for that order's,it's returns to dict object

        """
        sale_objects = SalesFlatOrder.objects.filter(
            increment_id__in=increment_ids).prefetch_related('store')

        logger.debug(
            "Fetched the sale order objects for that list of order id's")

        order_stores = {}
        for order_objs in sale_objects:
            order_stores[order_objs.increment_id] = order_objs.store.name

        return order_stores

    def generate_driver_completed_order_status(self):
        """Generates a csv file that includes driver details worked on current date and send the email for Accounts team."""
        # curent date
        start_date = date.today()

        end_date = date.today() + timedelta(days=1)
        # fetch current date driver order Events who completed order's
        logger.info(
            "Fetch the current date:{} driver order events,who completed order's" .format(start_date))
        driver_objects = OrderEvents.objects.filter(
            status='completed', updated_time__range=(start_date, end_date)).prefetch_related('driver')
        # list the order-id's who completed orders
        increment_id = [
            driver_obj.driver.increment_id for driver_obj in driver_objects]
        # fetch sale order objects
        logger.info(
            "To fetch the store names based on orders completed by driver")
        sale_objects = self.fetch_driver_completed_order_store_names(
            increment_id)
        # generate a csv file
        logger.info(
            "To generate a end_of_day_driver_details.csv file")
        csv_writer, open_csv_file = self.generate_csv()
        # add header row for csv file
        csv_writer.writerow(['Driver name', 'Phone', 'Order id', 'Store Name'])
        for driver_obj in driver_objects:
            # fetch driver basic info
            driver_basic_info = CustomerSearchController.load_cache_basic_info(
                driver_obj.driver.driver_id)
            # include a row for driver details in csv file
            logger.info(
                'pushing the driver:{} details along with order id:{} and store name to the csv file.'.format(driver_basic_info['entity_id'], driver_obj.driver.increment_id))
            csv_writer.writerow([
                driver_basic_info['name'],
                driver_basic_info['phone'],
                driver_obj.driver.increment_id,
                sale_objects.get(
                    driver_obj.driver.increment_id)])

        open_csv_file.close()
        # send email the driver end of day csv file
        Mail().send(
            "reports@tendercuts.in",
            ["varun@tendercuts.in", "asarudheen@tendercuts.in"],
            'Driver details',
            "Here the attachement includes the driver details at end of day",
            ["end_of_day_driver_details.csv"])
