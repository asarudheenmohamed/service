"""Test reward Point transection."""
import pytest
from app.tcash.lib import reward_points_controller as reward_points_controller
from app.core.models.customer.entity import MRewardsTransaction, CustomerEntity
from datetime import datetime


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
        # add reward amount for mock user
        reward_point_obj = MRewardsTransaction(
            customer=CustomerEntity.objects.get(entity_id=mock_user.customer.entity_id), amount=10000,
            is_expired=0,
            created_at=datetime.now(),
            is_expiration_email_sent=1,
            comment="Test reward amount added")
        reward_point_obj.save()

        response = auth_rest.get(
            "/user/reward/",
            format='json')

        assert response.status_code == 200
        assert response.json()['results'][0][
            'customer'] == mock_user.customer.entity_id
