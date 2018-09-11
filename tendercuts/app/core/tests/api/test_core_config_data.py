"""Test the store address Api."""

import pytest

from app.core.models.product import CatalogProductFlat1


@pytest.mark.django_db
class TestApiCoreConfigDataViewSet(object):
    """Test the CoreConfigData Api."""

    def test_store_address(self, rest):
        """Test the Store address api
        params:
            rest (fixture): rest endpoint

        Asserts:
            1. For a valid response.
        """
        response = rest.get(
            "/core/store_address/",
            format='json')

        assert response.status_code == 200
        assert (response) is not None
