"""Sending order's status sms to the customer related celery tasks."""

from datetime import datetime, timedelta
import logging

from app.core.lib.celery import TenderCutsTask
from app.core.lib.communication import SMS
from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
from app.driver.models import DriverLoginLogout
from config.celery import app
from django.conf import settings
from app.core.lib.communication import Mail
from app.core.models.customer.address import CustomerAddressEntityInt

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask)
def driver_stat(order_id):
    """Celery task to add the driver completed order."""
    from app.driver.lib.driver_stat_controller import DriverStatController

    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id).last()
    if not order_obj:
        raise ValueError('Order object Does not exist')

    stat_controller = DriverStatController(order_id)
    orders = stat_controller.generate_stat(
        order_obj.increment_id, order_obj.status)


@app.task(base=TenderCutsTask)
def address_verified(order_id):
    """Celery task to add the driver completed order."""
    from django.conf import settings

    order = SalesFlatOrder.objects.filter(increment_id=order_id).last()
    if not order:
        raise ValueError('Order object Does not exist')

    is_verified_attr = settings.MAGE_ATTRS['IS_VERIFIED']
    shipping_address = order.shipping_address.filter(
        address_type="shipping").last()

    is_verified_obj, _ = CustomerAddressEntityInt.objects.get_or_create(
        attribute_id=is_verified_attr,
        entity_type_id=2,
        value=0,
        entity_id=shipping_address.customer_address_id)

    is_verified_obj.value = 1
    is_verified_obj.save()


@app.task(base=TenderCutsTask)
def send_force_complete_order_alert(order_id, force_complete_lat, force_complete_lng):
    """Celery task to alert the driver force completed order."""
    order = SalesFlatOrder.objects.filter(increment_id=order_id).last()
    if not order:
        raise ValueError('Order object Does not exist')
    shipping_address = order.shipping_address.filter(
        address_type="shipping").last()
    if shipping_address.geohash:
        # return True

        message = "The Order:{} complete the force customer location lat:{},lng:{} and dest location:{},{}".format(
            order_id, force_complete_lat, force_complete_lng, shipping_address.o_latitude, shipping_address.o_longitude)

        Mail().send(
            "reports@tendercuts.in",
            ["jira@tendercuts.atlassian.net", "tech@tendercuts.in"],
            "[INFO] Order:{} force complete Alert".format(order_id),
            message)


@app.task(base=TenderCutsTask)
def generate_end_of_day_driver_stat(order_id):
    """Celery task to generate end of day driver status."""
    from app.driver.lib.end_of_day_driver_status import DriverStatusController
    controller = DriverStatusController()
    controller.generate_driver_completed_order_status()


@app.task(base=TenderCutsTask)
def customer_current_location(customer_id, lat, lon):
    """Update customer current location.

    Params:
     customer_id(int):user entity_id
     lat(int):customer location latitude
     lon(int):customer location longitude

    """

    from app.driver.lib.customer_location import CustomerLocationController
    customer_location_controller = CustomerLocationController()
    customer_loc_obj = customer_location_controller.update_customer_location(
        customer_id, lat, lon)


@app.task(base=TenderCutsTask)
def send_sms(order_id, template_key, scheduled_time=None):
    """Celery task to send the order's status to the customer."""

    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id)

    if not order_obj:
        raise ValueError('Order object Does not exist for {}'.format(order_id))

    order_obj = order_obj.last()

    try:
        data = CustomerSearchController.load_basic_info(
            order_obj.customer_id)
        userid, email, phone, name = data
    except Exception as e:
        raise ValueError('Extract basic info failed for CID: {}'.format(
            order_obj.customer_id))

    logger.info("Send status as {} to the customer : {}".format(
        order_obj.status, phone))

    message = settings.SMS_TEMPLATES[template_key].format(order_id)

    if scheduled_time:
        SMS().send(phone, message, scheduled_time)
    else:
        SMS().send(phone, message)

    logger.info(
        "Send order:{} {} state message for this customer:{}".format(
            order_id, order_obj.status, name))


@app.task(base=TenderCutsTask)
def set_checkout():
    """Celery task to set Check Out time for the driver."""
    objs = DriverLoginLogout.objects.filter(
        date=datetime.today().date(), check_out__isnull=True)

    logger.info(
        "To Update the check_out time for the drivers who forgot to check_out")

    if objs:
        objs.select_related('driver').update(
            check_out=datetime.now().time().replace(
                hour=23, minute=59, second=0, microsecond=0))


@app.task(base=TenderCutsTask)
def compute_order_eta(increment_id):
    """Update the order ETA."""
    from app.driver.lib.google_api_controller import GoogleApiController
    order = SalesFlatOrder.objects.filter(increment_id=increment_id).last()
    controller = GoogleApiController(order)
    controller.compute_eta()
