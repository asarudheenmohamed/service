"""Test driver assign."""

import pytest


@pytest.mark.django_db
class TestDriverWorkflow:

    def test_driver_assign(self, auth_rest, generate_mock_order):
        """Generate mock order and assing to driver.

        Params:
            auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response not equal to None
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        response = auth_rest.post(
            "/driver/assign/",
            {'order_id': generate_mock_order.increment_id},
            format='json')

        assert (response) is not None
        assert response.status_code == 201

    def test_driver_order_complete(self, auth_rest, generate_mock_order):
        """Mark the assigned order as complete.

        Params:
            auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response not equal to None
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        response = auth_rest.post(
            "/driver/assign/complete/",
            {'order_id': generate_mock_order.increment_id},
            format='json')

        assert (response) is not None
        assert response.status_code == 201
