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

    customer_location_obj = tasks.customer_current_location.delay(
        generate_mock_order.customer_id, 11.342, 80.542)

    customer_address_obj = address.CustomerAddressEntity.objects.filter(
        parent__entity_id=generate_mock_order.customer_id).last()

    eav_obj = EavAttribute.objects.filter(attribute_code='latitude').last()

    customer_addressentity_obj = address.CustomerAddressEntityText.objects.filter(
        attribute=eav_obj, entity=customer_address_obj)

    assert customer_addressentity_obj[0].value == '11.342'

    eav_obj = EavAttribute.objects.filter(attribute_code='longitude').last()

    customer_addressentity_obj = address.CustomerAddressEntityText.objects.filter(
        attribute=eav_obj, entity=customer_address_obj).last()

    assert customer_addressentity_obj.value == '80.542'
