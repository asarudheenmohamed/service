"""Test the update customer current location task."""

from app.driver import tasks

import pytest


@pytest.mark.django_db
def test_customer_current_location_task(generate_mock_order):
    """Test the customer current location task."""

    customer_location_obj = tasks.customer_current_location.apply_async(
        (generate_mock_order.customer_id, 11.342, 80.542))

    assert customer_location_obj.state == "success"
