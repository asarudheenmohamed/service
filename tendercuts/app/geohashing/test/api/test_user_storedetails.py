"""Test the user store details."""
import pytest


@pytest.mark.django_db
def test_user_store_details(rest, auth_sm):
    """Test the user store details..

    Params:
        auth_sm(pytest fixture):store manager requests

    Asserts:
        Check response store is equal to mocking store id

    """

    response = auth_sm.get(
        "/geohash/store_details/",
        format='json')

    assert response.json().store_id == 4
