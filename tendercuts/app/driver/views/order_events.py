"""Endpoints to provide password reset."""

# Create your views here.magent
# import the logging library
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from app.core.lib.utils import get_user_id
from app.driver.models.driver_order import DriverOrder, DriverPosition, OrderEvents
from app.driver.serializer.serializers import OrderEventsSerializer
from app.driver.lib.geo_locations import GeoLocations
from app.core.models import SalesFlatOrder
from app.driver.lib.driver_controller import DriverController
from ..auth import DriverAuthentication
# Get an instance of a logger
logger = logging.getLogger(__name__)


class OrderEventsViewSet(APIView):
    """OTP for resetting password."""
    authentication_classes = (DriverAuthentication,)
    serializer_class = OrderEventsSerializer

    def get(self, request):
        print 'gffffffffffffffffffffffffffffffffffffffffffffffff'
        """Fetch the OTP from redis DB and validate the OTP.

        1.Then go ahead and reset the password!

        """
        order_id = request.GET.get("order_id")

        # user_id = get_user_id(self.request)
        user_id = 2150

        a = OrderEvents.objects.filter(driver__driver_id=user_id)
        print a, 'ggggggggggggggggggggggggggggg'
        serializer = self.get_serializer(driver_position)
        return Response(serializer.data)
        # return Response(
        #     {'status': True, 'message': 'driver location updated successfully'})
