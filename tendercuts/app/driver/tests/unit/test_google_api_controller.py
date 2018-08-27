"""Test cases for controller."""

import mock
import pytest
from app.core.models.customer.address import CustomerAddressEntityVarchar
from app.core.models.entity import EavAttribute
from app.core.models.sales_order import SalesFlatOrder, SalesFlatOrderAddress
from app.driver.lib.google_api_controller import GoogleApiController


@pytest.mark.django_db
class TestGoogleApiController:
    """Test cases for Driver controller."""

    def mock_objects(self):
        """Mock the customer Address details."""
        eav_attribute = EavAttribute.objects.get_or_create(
            attribute_code='geohash',
            entity_type_id=2,
            is_user_defined=1,
            is_required=0,
            is_unique=0)

        shipping_address = SalesFlatOrderAddress.objects.filter(
            customer_address_id__isnull=False).last()

        CustomerAddressEntityVarchar.objects.get_or_create(
            attribute=eav_attribute[0],
            entity_id=shipping_address.customer_address_id,
            value='tf31fqb',
            entity_type_id=1)
        eav_latitude = EavAttribute.objects.filter(
            attribute_code='latitude').last()
        eav_longitude = EavAttribute.objects.filter(
            attribute_code='longitude').last()
        eav_designated = EavAttribute.objects.filter(
            attribute_code='designated_store').last()

        CustomerAddressEntityVarchar.objects.filter(
            attribute=eav_latitude,
            entity_id=shipping_address.customer_address_id).update(value=12.9754)

        CustomerAddressEntityVarchar.objects.filter(
            attribute=eav_longitude,
            entity_id=shipping_address.customer_address_id).update(value=80.2206)
        CustomerAddressEntityVarchar.objects.filter(
            attribute=eav_designated,
            entity_id=shipping_address.customer_address_id).update(value='adayar')

        return shipping_address.parent

    def test_compute_eta(self):
        """Test store store to customer location eta computation.

        Asserts:
            1. If the eta is not None

        """
        order = self.mock_objects()
        controller = GoogleApiController(order)

        response = controller.compute_eta()

        sale_address = SalesFlatOrderAddress.objects.filter(
            parent=order).last()

        assert sale_address.eta is not None

        with mock.patch.object(GoogleApiController, 'compute_eta', side_effect={'geo_location': False}):
            response = controller.compute_eta()

            sale_address = SalesFlatOrderAddress.objects.filter(
                parent=order).last()

            assert sale_address.eta is not None
