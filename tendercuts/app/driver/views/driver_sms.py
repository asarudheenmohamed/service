from rest_framework import viewsets
from rest_framework.response import Response

from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_user_id
from app.driver.lib.driver_controller import DriverController

from ..auth import DriverAuthentication

class DelaySmsViewSet(viewsets.ModelViewSet):

    authentication_classes = (DriverAuthentication,)

    def get_driver(self):
        """Extract DriverId from request.
        Returns:
            Returns Driver object
        """

        driver_id = get_user_id(self.request)
        driver = CustomerSearchController.load_by_id(driver_id)

        return driver

    def create(self, request, *args, **kwargs): 
        """Send the information via SMS if the driver delays the order.

        Input:
            order_id

        returns:
            Response({status: bool})
        """

        order_id = self.request.data['order_id']
        driver = self.get_driver()
        controller = DriverController(driver)
        status = controller.driver_delay_sms(order_id)

        return Response({'status':status})
        







