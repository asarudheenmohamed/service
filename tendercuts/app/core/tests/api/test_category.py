"""Test endpoint "product."""

import pytest


@pytest.mark.django_db
class TestApiInventoryFetch(object):
    """Test cases for products fetch."""

    def test_fetch_product(self, auth_rest):
        """Test case to fetch the products.

        params:
            auth_rest (fixture): Auth rest endpoint

        Asserts:
            1. For a valid response.
            2. If the first category is what;s new
        """
        response = auth_rest.get(
            "/core/product/",
            {"store_id": 1},
            format='json')

        assert (response) is not None
        assert len(response.data) >= 6
