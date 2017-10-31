"""Test Mcredit Balance."""
import pytest
from datetime import datetime


@pytest.mark.django_db
class TestMcredit:

    def test_creditbalance_api(self, auth_rest, mock_user):
        """Get reward point transaction.

        Params:
        auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response not equal to None
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        # Add mcredit balance for mock order
        from app.core.models.customer.entity import MCreditBalance, CustomerEntity
        MCreditBalance.objects.create(
            customer=CustomerEntity.objects.get(
                entity_id=mock_user.customer.entity_id),
            amount=1000,
            is_subscribed=1,
            created_at=datetime.now(),
            updated_at=datetime.now())

        response = auth_rest.get(
            "/user/mcredit/",
            format='json')

        assert response.status_code == 200
        assert response.json()['results'][0][
            'customer'] == mock_user.customer.entity_id
