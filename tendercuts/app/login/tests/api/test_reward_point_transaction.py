"""Test reward Point transection."""
import pytest
from app.tcash.lib import reward_points_controller as reward_points_controller


@pytest.mark.django_db
class TestReward:

    def test_rewardtransection(self, auth_rest, mock_user):
        """Get reward point transection in mock user.

        Params:
        auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response not equal to None
            Check response status code in equal to 200
            Check custermer id is equal to mock user id

        """
        response = auth_rest.get(
            "/user/reward/",
            format='json')
        # assert not isinstance(response, None)
        assert response.status_code == 200
        assert response.json()['results'][0][
            'customer'] == mock_user.customer.entity_id
