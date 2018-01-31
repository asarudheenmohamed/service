"""Sending updated inventory's status sms to the customers."""
import logging

from django.contrib.auth.models import User

from app.core.lib.celery import TenderCutsTask
from app.core.lib.communication import SMS, Flock
from app.core.lib.user_controller import CustomerSearchController
from app.core.models.product import CatalogProductFlat1
from app.core.models.store import CoreStore
from app.inventory.lib.low_stock_notification_controller import \
    LowStockNotificationController
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


@app.task(base=TenderCutsTask, ignore_result=True)
def low_stock_notification():
    """Celery task to notify the low stock information through flock."""
    controller = LowStockNotificationController()
    low_stocks = controller.get_low_stocks()

    #  Inorder to get store name filter the object from CoreStore
    store_objs = CoreStore.objects.filter(store_id__in=low_stocks.keys())
    store_dict = {store.store_id: store.name for store in store_objs}

    logger.debug("To send Flock message to filtered store groups: {}".format(
        store_dict.values()))
    #  Inorder to get product name filter the object from CatalogProductFlat1
    product_obj = CatalogProductFlat1.objects.select_related('entity').all()
    product_name = {product.sku: product.name for product in product_obj}

    for store_id, products in low_stocks.items():
        store_name = store_dict.get(store_id)
        #  To prepare the flockml text for flockml attachment
        product_detail = ["{}: <b>{} - {}(qty)</b>".format(
            index, product_name.get(product['product__sku']), product['qty'])
            for index, product in enumerate(products, 1)]
        product_detail = "<br/>".join(product_detail)

        title = "Out of stock Alerts"
        description = "These products are going to be out of stock"

        Flock().send_flockml(store_name, product_detail, title, description)

    logger.info("Store groups: {} are received low stock message Successfully".format(
        store_dict.values()))

    return {'status': True}

