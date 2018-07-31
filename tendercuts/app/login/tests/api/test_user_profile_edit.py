"""Test User Profile Changes."""
import pytest
import random
from app.core.lib.test import generate_customer


@pytest.mark.django_db
class TestUserProfileEdit:
    """Test user profile Edit."""

    def test_profile_changes(self, rest):
        """Check test user profile changes.

        Params:
        auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response status code in equal to 200
            Check custermer email id is equal to changing email id
            Check custermer username is equal to changing username

        """
        # generate a new customer
        customer_data = generate_customer()

        data = {"email": customer_data['email'], "password": "12345678"}
        response = rest.post("/user/login", data=data)
        assert response.status_code == 200
        assert response.json()['email'] == customer_data['email']

    @pytest.mark.parametrize("field_value,code", (
        ["Testuser", "firstname"],
        [("testuser{}@gmail.com".format(random.randint(1, 1000000))), "email"],
        ["test123", "password_hash"],
        ["Testuser", "firstname"],
    ))
    def test_username_reset(self, auth_rest, field_value, code):
        """User details change in test user.

        Params:
        auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response status code in equal to 200
            Check response status is equal to True

        """
        response = auth_rest.post(
            "/user/edit_profile/", {'field_value': field_value,
                                    'code': code},
            format='json')
        assert response.status_code == 200
        assert response.json()['status'] == True
