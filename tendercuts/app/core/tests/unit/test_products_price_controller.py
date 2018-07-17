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
        obj.save()

        controller = ProductsPriceController()
        products_prices = controller.get_products_price(store_id)

        assert obj.visibility == 4
        assert obj.status == 1
        assert obj.special_price == 100
