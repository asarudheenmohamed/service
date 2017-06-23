import pytest
"""Test User Profile Changes."""


@pytest.mark.django_db
class TestUserProfileEdit:
    """Test user profile Edit."""

    def test_username_reset(self, auth_rest):
        """Username change in test user.

        Params:
        auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        response = auth_rest.post(
            "/user/edit_profile/", {'field_value': 'Testuser',
                                    'code': 'firstname'},
            format='json')
        assert response.status_code == 200
        assert response.json()['status'] == True

    def test_email_reset(self, auth_rest):
        """Email change in test user.

        Params:
        auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        response = auth_rest.post(
            "/user/edit_profile/", {'field_value': 'varun@tendercuts123.com',
                                    'code': 'email'},
            format='json')
        # assert not isinstance(response, None)
        assert response.status_code == 200
        assert response.json()['status'] == True

    def test_dob_reset(self, auth_rest):
        """Get reward point transection in 18963.

        Params:
        auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        response = auth_rest.post(
            "/user/edit_profile/", {'field_value': '2017-06-19 00:00:00',
                                    'code': 'dob'},
            format='json')
        # assert not isinstance(response, None)
        assert response.status_code == 200
        assert response.json()['status'] == True

    def test_password_reset(self, rest, auth_rest):
        """Get reward point transection in 18963.

        Params:
        auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        response = auth_rest.post(
            "/user/edit_profile/", {'field_value': 'test123',
                                    'code': 'password_hash'},
            format='json')
        assert response.status_code == 200
        assert response.json()['status'] == True

    def test_profile_changes(self, rest, auth_rest):
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
        data = {"email": "varun@tendercuts123.com", "password": "test123"}
        response = rest.post("/user/login", data=data)
        assert response.status_code == 200
        assert response.json()['email'] == "varun@tendercuts123.com"
        assert response.json()['firstname'] == "Testuser"
