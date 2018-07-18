"""Test cases for Address models."""

import pytest
from app.core.models.customer.address import CustomerAddressEntityVarchar


@pytest.mark.django_db
class TestAddress(object):
    """Test cases for Address related api's."""

    def test_designated_store(self, auth_rest):
        """Test to the customer designated store api..

        params:
            auth_rest (fixture): Auth rest endpoint

        Asserts:
            Checks the mock designated store
            Checks the mock address id

        """
        address_obj = CustomerAddressEntityVarchar.objects.all().last()
        address_obj.value = 'tambaram'
        address_obj.save()

        response = auth_rest.get(
            "/core/designated_store/",
            {"address_id": address_obj.entity_id},
            format='json')

        assert (response) is not None
        assert response.data['results'][0]['entity'] == address_obj.entity_id
        assert response.data['results'][0]['value'] == address_obj.value
