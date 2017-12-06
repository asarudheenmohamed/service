"""Sending updated inventory's status sms to the customers."""
import logging

from django.contrib.auth.models import User

from app.core.lib.celery import TenderCutsTask
from app.core.lib.communication import SMS
from app.core.lib.user_controller import CustomerSearchController
from app.inventory.lib.notify_customer_controller import \
    NotifyCustomerController
from app.inventory.models import NotifyCustomer
from config.celery import app

logger = logging.getLogger(__name__)


@app.task(base=TenderCutsTask, ignore_result=True)
def notification_sms():
    """Celery task to send the updated inventory sms to the customer."""
    controller = NotifyCustomerController()
    notify_obj = controller.get_customer_notify_obj()
    notify_customers = controller.get_avalible_notifies(notify_obj)

    logger.debug("To get the User object for notify_customers:{}".format(
        notify_customers.keys()))

    user_objs = User.objects.filter(id__in=notify_customers.keys())
    user_dict = {user.id: user.username for user in user_objs}
    for customer_id, products in notify_customers.items():
        # To get user name from user_dict and change it into user_id
        user_id = user_dict.get(customer_id).split(":")

        if len(user_id) < 1:
            user_id = None
        else:
            user_id = user_id[1]

        customer = CustomerSearchController.load_cache_basic_info(user_id)
        msg = str(products)
        SMS().send(int(customer['phone']), msg)

    logger.info("Notified customers are receives the updated inventory SMS")

    status = True

    return status
