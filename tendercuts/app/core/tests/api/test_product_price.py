"""Test endpoint product price."""

import pytest

from app.core.models.product import CatalogProductFlat1


@pytest.mark.django_db
class TestApiProductsPriceFetch(object):
    """Test cases for product price fetch."""

    def test_fetch_products_price(self, auth_rest):
        """Test case to fetch the products price
        params:
            auth_rest (fixture): Auth rest endpoint

        Asserts:
            1. For a valid response.
            2. Check updated special price is reflected in response
        """
        response = auth_rest.get(
            "/core/price/",
            {"store_id": 1})

        print response.data[0]

        obj = CatalogProductFlat1.objects.get(
            entity=response.data[0]['entity_id'])
        obj.special_price = 100
        obj.save()

        response = auth_rest.get(
            "/core/price/",
            {"store_id": 1},
            format='json')

        assert response.status_code == 200

        assert response.data[0]['special_price'] == 100
