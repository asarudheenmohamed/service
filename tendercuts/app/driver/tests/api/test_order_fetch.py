"""Test driver order fetch."""

import pytest
from app.driver.models import DriverOrder

from app.driver.models import DriverOrder, DriverPosition, OrderEvents
from django.contrib.auth.models import User


@pytest.fixture
def driver_order(generate_mock_order, django_user):
    """Check and create"""
    driver_object = DriverOrder.objects.filter(
        increment_id=generate_mock_order.increment_id,
        driver_user=django_user)

    if not driver_object:
        driver_object = DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_user=django_user)

    return driver_object


@pytest.mark.django_db
class TestOrderFetch:

    @pytest.mark.parametrize('status', ['out_delivery', 'complete'])
    def test_driver_orders(
            self,
            auth_driver_rest,
            generate_mock_order,
            driver_order,
            status):
        """Get reward point transection in 18963.

        Params:
            auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response not equal to None
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        generate_mock_order.status = status
        generate_mock_order.save()

        user = User.objects.get_or_create(
            username='u:{}'.format(
                generate_mock_order.customer_id))

        # assign order
        DriverOrder.objects.create(
            driver_user=user[0],
            increment_id=generate_mock_order.increment_id)

        response = auth_driver_rest.get(
            "/driver/orders/?status={}".format(status),
            format='json')

        assert (response) is not None
        assert response.status_code == 200
        assert response.json()['results'][0]['status'] == status
