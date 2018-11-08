from datetime import datetime

import pytest
from app.core.lib.controller import ProductsPriceController
from app.core.models.product import CatalogProductFlat1


@pytest.mark.django_db
class TestProductPriceController:
    """Testcases for Product price controller."""

    def test_get_products_price(self):
        """Fetch product prices for selected store.

        Asserts:
            1.Check fetched products are vissible and active
            2.Check updated special price will reflected

        """
        store_id = 1

        controller = ProductsPriceController()
        products_prices = controller.get_products_price(store_id)

        obj = CatalogProductFlat1.objects.get(
            entity=products_prices[0]['entity_id'])

        obj.special_price = 100
        obj.special_to_date=datetime.now()
        obj.save()

        controller = ProductsPriceController()
        products_prices = controller.get_products_price(store_id)
        product=(products_price for products_price in products_prices if products_price["entity_id"] == obj.entity_id).next()

        assert obj.special_price == product['special_price']
