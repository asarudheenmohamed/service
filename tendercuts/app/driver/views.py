import app.core.core.magento_api as magento

from . import models as models
from . import serializers as serializers
from .lib import ShadowFaxDriverController
from .lib import driver_controller as driver_lib

from app.core.lib.order_controller import OrderController

import datetime
import json

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status


class DriverViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.

    Acts an authentication endpoint and to get the driver detail
    """
    queryset = models.DriverManagement.objects.all()
    serializer_class = serializers.DriverSerializer
    lookup_field = "phone"


class DriverSalesOrderViewSet(generics.ListAPIView):
    """
    Endpoint that acts provides all the active order for the current driver.
    """
    serializer_class = serializers.SalesOrderSerializer

    def get_queryset(self):
        user = self.request.user

        driver = models.DriverManagement.objects.filter(phone=user.username)

        driver = driver[0]

        controller = driver_lib.DriverController(driver)

        try:
            status = self.request.query_params['status']
            queryset = controller.get_completed_orders()
        except KeyError:
            queryset = controller.get_active_orders()

        return queryset


class OrderCompleteApi(APIView):
    """
    Enpoint that uses magento API to mark an order as comple
    """
    def post(self, request, format=None):
        user = self.request.user

        increment_id = self.request.data['increment_id']

        order = models.SalesFlatOrder.filter(increment_id=increment_id)
        controller = OrderController(order)
        response_data = controller.complete_order()

        data = {"status": response_data}
        return Response(data, status=status.HTTP_201_CREATED)



class DriverLocationViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.

    Get all the location udpates of the current driver.
    """
    serializer_class = serializers.DriverLocationSerializer
    # Since queryset is not defined, we will specify the model in the uRL

    def get_queryset(self):
        user = self.request.user

        queryset = models.DriverLocation.objects \
            .filter(driver=user)
            # .filter(updated_at=str(datetime.datetime.today()))

        return queryset


from datetime import date
from datetime import timedelta
from django.db.models import Q
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):

        store_id = self.request.GET.get('store')
        context = super(HomePageView, self).get_context_data(**kwargs)

        drivers = driver_models.DriverLocation.objects.filter(
            updated__range=(date.today(),
                            date.today() + timedelta(days=1)))

        stores = models.CoreStore.objects.filter(~Q(store_id=0) & ~Q(store_id=9))

        context["selected_store"] = 0
        context['stores'] = stores

        if store_id:
            drivers = [user for user in drivers if user.driver.store == store_id ]
            store = [dp for dp in stores if dp.store_id == int(store_id)]
            context["selected_store"] = store[0]

        context['locations'] = drivers


        return context


class ShadowFaxUpdate(APIView):
    def post(self, request, format=None):
        try:
            controller = ShadowFaxDriverController().update_order(self.request.data)
        except Exception as e:
            return Response(
                {"status": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        return Response(self.request.data, status=status.HTTP_201_CREATED)

