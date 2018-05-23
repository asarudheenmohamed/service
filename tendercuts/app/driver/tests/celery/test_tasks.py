"""Test the update customer current location task."""

import pytest

from app.core.models.customer import address
from app.core.models.entity import EavAttribute
from app.driver import tasks


@pytest.mark.django_db
def test_customer_current_location_task(generate_mock_order):
    """Test the customer current location task.

        Asserts:
         Checks the mock latitude and longitude

    """

    customer_location_obj = tasks.customer_current_location.apply(
        generate_mock_order.customer_id, 11.342, 80.542).get()

    customer_address_obj = address.CustomerAddressEntity.objects.filter(
        parent__entity_id=generate_mock_order.customer_id)

    eav_obj = EavAttribute.objects.filter(attribute_code='latitude')
    customer_addressentity_obj = address.CustomerAddressEntityText.objects.filter(
        attribute=eav_obj[0], entity=customer_address_obj[0]).values_list('value')

    # latitude = customer_addressentity_obj[0].value
    assert str(customer_addressentity_obj[0][0]) == '11.342'

    eav_obj = EavAttribute.objects.filter(attribute_code='longitude')

    customer_addressentity_obj = address.CustomerAddressEntityText.objects.filter(
        attribute=eav_obj[0], entity=customer_address_obj[0]).values_list('value')

    # longitude = customer_addressentity_obj[0].value
    assert str(customer_addressentity_obj[0][0]) == '80.542'
