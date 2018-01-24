"""Test driver order fetch."""

import pytest
from app.driver.models import DriverOrder


@pytest.mark.django_db
class TestOrderFetch:

    @pytest.mark.parametrize('status', ['complete', 'out_delivery'])
    def test_driver_orders(
            self,
            auth_driver_rest,
            generate_mock_order,
            mock_user,
            django_user,
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
        driver_object = DriverOrder.objects.create(
            increment_id=generate_mock_order.increment_id,
            driver_user=django_user)
        generate_mock_order.status = status
        generate_mock_order.save()

        response = auth_driver_rest.get(
            "/driver/orders/?status={}".format(status),
            format='json')

        assert (response) is not None
        assert response.status_code == 200
        assert len(response.json()['results']) == 1
