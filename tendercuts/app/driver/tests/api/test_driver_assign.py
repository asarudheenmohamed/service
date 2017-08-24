"""Test Driver assign unassign orders."""

import pytest


@pytest.fixture
def mock_order(generate_mock_order):
    """Generate mock order.

    Returns:
        Return mock order increment id and store id.

    """
    return {'increment_id': generate_mock_order.increment_id,
            'store_id': generate_mock_order.store_id}


@pytest.mark.django_db
class TestDriverWorkflow:

    @pytest.mark.parametrize("store_id,message", (
        ["7", "Order Assigned successfully"],
        ["8", "Store mismatch"],
    ))
    def test_driver_assign(self, auth_rest, store_id, message, mock_order):
        """Generate mock order and assing to driver.

        Params:
            auth_rest(pytest fixture): user requests
            mock_order(dict): mock order id and store id

        Asserts:
            Check response not equal to None
            Check response status code in equal to 200
            Check response message is equal to Order Assigned successfully

        """
        response = auth_rest.post(
            "/driver/assign/",
            {'order_id': mock_order['increment_id'],
                'store_id': store_id},
            format='json')

        assert (response) is not None
        assert response.status_code == 200
        assert response.data['message'] == message

    def test_order_unassign(self, auth_rest, mock_order):
        """Generate mock order and assing to driver.

        Params:
            auth_rest(pytest fixture):user requests
            mock_order(dict): mock order id and store id

        Asserts:
            Check response not equal to None
            Check response status code in equal to 200
            Check response message is equal to Order UnAssigned successfully

        """
        response = auth_rest.post(
            "/driver/unassign/",
            {'order_id': mock_order['increment_id']},
            format='json')

        assert (response) is not None
        assert response.status_code == 200
        assert response.data['message'] == "Order UnAssigned successfully"

    def test_driver_order_complete(self, auth_rest, mock_order):
        """Mark the assigned order as complete.

        Params:
            auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response not equal to None
            Check response status code in equal to 201

        """
        response = auth_rest.post(
            "/driver/assign/complete/",
            {'order_id': mock_order['increment_id']},
            format='json')

        assert (response) is not None
        assert response.status_code == 201
