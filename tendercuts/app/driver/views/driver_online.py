"""Endpoints to provide driver online updates and status."""

import logging

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from app.driver.lib.driver_online_controller import DriverOnlineController

logger = logging.getLogger(__name__)


class DriverCheckIn(APIView):
    """Create Driver check_in object.

    EndPoint:
        API: driver/check_in

    """

    def get(self, request):
        """To create driver check in object.

        Input:
            user_id

        returns:
            Response({'status':status})

        """
        store_id = self.request.GET.get('store_id', None)
        logger.info("To Create Check In record for the driver :{}".format(
            self.request.user))

        controller = DriverOnlineController(self.request.user)
        status = controller.driver_checkin(store_id)

        return Response({'status': status})


class DriverCheckOut(APIView):
    """Update the Driver check out time.

    EndPoint:
        API: driver/check_out

    """

    def get(self, request):
        """To update driver check_out time.

        Input:
            user_id

        returns:
            Response({'status':status})

        """

        logger.info("To Update Check Out record for the driver :{}".format(
            self.request.user))

        controller = DriverOnlineController(self.request.user)
        status = controller.driver_checkout()

        return Response({'status': status})


class CheckStatus(APIView):
    """Check current driver status.

    EndPoint:
        API: driver/check_status

    """

    def get(self, request):
        """To Check the status of the driver.

        Input:
            user_id

        returns:
            Response({'status':status})

        """
        logger.info("To Check online status for the driver :{}".format(
            self.request.user))

        controller = DriverOnlineController(self.request.user)
        status, store_id = controller.driver_status()

        return Response({'status': status, 'store_id': store_id})
