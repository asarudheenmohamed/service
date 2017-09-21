"""Endpoint for  driver Delay SMS."""

from rest_framework import viewsets
from rest_framework.response import Response

from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_user_id
from app.driver.lib.driver_controller import DriverController

from ..auth import DriverAuthentication


class DriverSmsViewSet(viewsets.ModelViewSet):
    """Endpoint that driver sends delay SMS to customer.

    EndPoint:
        API: driver/delay_sms/

    """

    authentication_classes = (DriverAuthentication,)

    def create(self, request, *args, **kwargs):
        """Send the information via SMS if the driver delays the order.

        Input:
            order_id

        returns:
            Response({status: bool})

        """
        order_id = self.request.data['order_id']
        driver_id = get_user_id(self.request)
        driver = DriverController.driver_obj(driver_id)
        controller = DriverController(driver)
        status = controller.driver_delay_sms(order_id)

        return Response({'status': status})
