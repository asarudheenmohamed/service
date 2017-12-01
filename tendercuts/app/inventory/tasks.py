"""Sending updated inventory's status sms to the customers."""
import logging

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

    for notify_customer in notify_customers:
        #convert unicode into string and get user id from user name
        user_id = notify_customer.encode('ascii', 'ignore').split(":")

        if len(user_id) < 1:
            user_id = None
        else:
            user_id = user_id[1]

        customer = CustomerSearchController.load_basic_info(user_id)

        msg = str(notify_customers[notify_customer])
        SMS().send(int(customer[2]), msg)

    logger.info("Notified customers are receives the updated inventory SMS")

    update_notify=controller.update_isnotified(notify_obj, notify_customers)

    status = True
 
    return status


