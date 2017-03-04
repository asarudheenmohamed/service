import app.tcuts.core.magento_api as magento
from app.tcuts import models as models
from app.tcuts import serializers as serializers
from rest_framework.views import APIView
from rest_framework import viewsets, generics
import json
import datetime
from rest_framework.response import Response

from rest_framework import status


class DriverViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.DriverManagement.objects.all()
    serializer_class = serializers.DriverSerializer
    lookup_field = "phone"


class SalesOrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.SalesFlatOrder.objects.all()
    serializer_class = serializers.SalesOrderSerializer


class DriverSalesOrderViewSet(generics.ListAPIView):
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        user = self.request.user

        driver = models.DriverManagement.objects.filter(phone=user.username)

        driver = driver[0]

        try:
            status = self.request.query_params['status']
        except KeyError:
            status = 'out_delivery'

        queryset = models.SalesFlatOrder.objects \
            .filter(driver=driver) \
            .filter(status=status)
            # .filter(updated_at=str(datetime.datetime.today()))

        return queryset


class OrderCompleteApi(APIView):

   def post(self, request, format=None):
        user = self.request.user

        increment_id = self.request.data['increment_id']
        mage = magento.Connector()

        response_data = mage.api.tendercuts_apis.completeOrders(
                [{"increment_id": increment_id}])

        data = {"status": response_data}
        return Response(data, status=status.HTTP_201_CREATED)

