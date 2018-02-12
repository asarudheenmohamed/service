"""Test exist user details"""
import pytest


@pytest.mark.django_db
class TestUserExists:
    """Test user Exist method."""

    def test_user_exists_phone(self, auth_rest):
        """Test Existing Customer.

        Asserts:
            Check response equals to True
        """
        response = auth_rest.get(
            "/user/exists/?phone=9908765678",
            format='json')
        assert not isinstance(response, type(None))
        assert response.data['result'] is True

    def test_user_exists_email(self, auth_rest):
        """Test Existing email.

        Asserts:
            Check response equals to True
        """
        response = auth_rest.get(
            "/user/exists/?email=mail@varunprasad.in", format='json')
        assert not isinstance(response, type(None))
        assert response.data['result'] is True

    def test_user_exists_invalid(self, auth_rest):
        """Test Customer Exist Invalid.

        Asserts:
            Check response equals to True
        """
        response = auth_rest.get("/user/exists/", format='json')
        assert not isinstance(response, type(None))
        assert response.data['result'] is True

    def test_user_exists_valid_phone(self, auth_rest):
        """Test customer valid mobile number.

        Asserts:
            Check response equals to False

        """
        response = auth_rest.get("/user/exists/?phone=90909090", format='json')
        assert not isinstance(response, type(None))
        assert response.data['result'] is False

    def test_user_exists_valid_email(self, auth_rest):
        """Test  customer valid email.

        Asserts:
            Check response equals to False

        """
        response = auth_rest.get(
            "/user/exists/?email=90909090@xoxo.com", format='json')
        assert not isinstance(response, type(None))
        assert response.data['result'] is False
