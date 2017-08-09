"""
Test endpoint "store"
"""

import pytest


@pytest.mark.django_db
class TestApiInventoryFetch(object):
    """Test cases for inventory fetch."""

    def test_fetch_inventory(self, auth_rest):
        """Test case to fetch the inventory.

        params:
            auth_rest (fixture): Auth rest endpoint

        Asserts:
            1. For a valid response.
        """
        response = auth_rest.get(
            "/inventory/store/",
            {"store_id": 1,
             "website_id": 2},
            format='json')

        assert len(response.json()) > 20

    def test_fetch_inventory_product(self, auth_rest):
        """Test case for fetching inventory with product filter.

        params:
            auth_rest (fixture): Auth rest endpoint

        Asserts:
            1. For a valid response.

        """
        data = {
            "store_id": 1,
            "website_id": 2,
            "product_ids": ",".join(["193", "194"])
        }

        response = auth_rest.get(
            "/inventory/store/",
            data,
            format='json')

        assert len(response.json()) == 2
