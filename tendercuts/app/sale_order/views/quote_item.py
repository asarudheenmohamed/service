"""ViewSet for the customer last quote items."""

from app.core.models.sale_quote import SalesFlatQuote
from app.sale_order.serializers import QuoteSerializer
from rest_framework import viewsets


class QuoteItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuoteSerializer

    def get_queryset(self):
        """Returns the customer last quote item queryset.

        Params:
          store_id (str): store id
          customer_id (str): megento customer id

        """
        store_id = self.request.query_params['store_id']
        customer_id = self.request.query_params['customer_id']

        return SalesFlatQuote.objects.filter(
            customer_id=customer_id, store=store_id).order_by('-entity_id')[:1]
