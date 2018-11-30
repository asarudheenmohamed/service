"""All driver controller related actions."""
import logging

from app.core.models import SalesFlatOrder
from config.celery import app
from config.messaging import ORDER_STATE
from app.driver.models.driver_order import DriverOrder, DriverPosition, OrderEvents


from ..models import DriverOrder

logger = logging.getLogger(__name__)


class DriverController(object):
    """Driver controller."""

    def __init__(self, driver):
        """Constructor."""
        super(DriverController, self).__init__()
        self.driver = driver
