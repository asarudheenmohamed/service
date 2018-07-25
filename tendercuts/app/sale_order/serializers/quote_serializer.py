"""Serializer for the  SalesFlatQuote,SalesFlatQuoteItem models."""

from app.core.models.sale_quote import SalesFlatQuote, SalesFlatQuoteItem
from rest_framework import serializers


class QuoteItemSerializer(serializers.ModelSerializer):
    """Serializer for the SalesFlatQuoteItem model."""
    class Meta:
        model = SalesFlatQuoteItem
        fields = ('product', 'qty')


class QuoteSerializer(serializers.ModelSerializer):
    """Serializer for the SalesFlatQuote model."""
    quote_item = QuoteItemSerializer(many=True)

    class Meta:
        model = SalesFlatQuote
        fields = ('quote_item', 'store', 'customer_id')
