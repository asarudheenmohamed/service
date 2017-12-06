"""Sending order's status sms to the customer related celry tasks."""

import logging

from celery.utils.log import get_task_logger

from app.core.lib.celery import TenderCutsTask
from app.core.lib.communication import SMS
from app.core.lib.user_controller import CustomerSearchController
from app.core.models import SalesFlatOrder
from app.core.models.entity import EavAttribute
from app.core.models.customer import address
from app.driver.lib.driver_stat_controller import DriverStatController
from config.celery import app

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask, ignore_result=True)
def driver_stat(order_id):
    """Celery task to add the driver completed order."""
    try:
        logger.info('driver stat order id {}'.format(order_id))
        order_obj = SalesFlatOrder.objects.filter(increment_id=order_id)
    except ValueError:
        print "This order id is invalid"
    stat_controller = DriverStatController(order_id)
    orders = stat_controller.generate_stat(
        order_obj[0].increment_id, order_obj[0].status)

    # logger.info("No of order is added to driver : {}".format(
    # order_obj[0].))


@app.task(base=TenderCutsTask, ignore_result=True)
def customer_current_location(customer_id, lat, lon):
    """Update customer current location.

    Params:
     customer_id(int):user entity_id
     lat(int):custoner location latitude
     lon(int):customer location longitude

    """
    customer_address_obj = address.CustomerAddressEntity.objects.filter(
        parent__entity_id=customer_id)
    for loc_value in ['latitude', 'longitude']:
        eav_obj = EavAttribute.objects.filter(
            attribute_code=loc_value)
        customer_addressentity_obj = address.CustomerAddressEntityText.objects.filter(
            attribute=eav_obj[0], entity=customer_address_obj[0])
        if customer_addressentity_obj:
            customer_addressentity_obj[
                0].value = lat if loc_value == 'latitude' else lon
        else:
            customer_addressentity_obj = address.CustomerAddressEntityText.objects.create(
                attribute=eav_obj[0],
                entity_type_id=1,
                entity=customer_address_obj[0],
                value=lat if loc_value == 'latitude' else lon)


@app.task(base=TenderCutsTask, ignore_result=True)
def send_sms(order_id):
    """Celery task to send the order's status to the customer."""

    order_obj = SalesFlatOrder.objects.filter(increment_id=order_id)
    logger.info('order_obj:{}'.format(order_obj))
    if not order_obj:
        raise ValueError('Order object Does not exist')

    customer = CustomerSearchController.load_basic_info(
        order_obj[0].customer_id)

    msg = {'out_delivery': "Your order #{}, is now out for delivery.Have a great meal Wish to serve you again!",
           'processing': "We have started to process Your #{},we will notify you,when we start to deliver.Tendercut.in-Farm Fresh Meats.",
           'complete': "Thanks for choosing Tendercuts.Your order has been successfully delivered!.please give a missed call to rate our quality of the product.Like it-9543486488 Disliked it-9025821254"}

    logger.info("Send status as {} to the customer : {}".format(
        order_obj[0].status, customer[0]))

    SMS().send(int(customer[2]), msg[order_obj[0].status].format(order_id))
