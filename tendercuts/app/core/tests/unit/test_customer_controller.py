"""Test cases for generating flat customer."""

import pytest

from app.core.lib.user_controller import (CustomerController)
from app.core.lib.exceptions import CustomerNotFound, InvalidCredentials


@pytest.fixture
def clsobj():
    """As a fixture wrapper for the class."""
    return CustomerController


@pytest.mark.django_db
class TestCustomerControllerAuth:
    """Test Customer controller.

    Asserts: Auth related test cases.

    """

    def test_invalid_password(self, clsobj, mock_user):
        """Test user invalid password.

        Asserts:
        1. Failure on login with invalid password

        """
        with pytest.raises(InvalidCredentials):
            clsobj.authenticate(mock_user.email, "INCORRECT_PW")

    def test_invalid_username(self, clsobj):
        """Test user invalid username.

        Asserts:
            1. Failure on login with invalid username

        """
        with pytest.raises(CustomerNotFound):
            clsobj.authenticate("mail@varun.xy", "qwerty123")

    def test_valid_username(self, clsobj, mock_user):
        """Test user valid username.

        Asserts:
            1. Succes on login with valid username

        """
        flat = clsobj.authenticate(mock_user.email, "12345678")
        assert flat.customer.email == mock_user.email

    def test_verify_token(self, clsobj, mock_user):
        """Test verify the user token.

        Asserts:
            Checks the response username

        """
        user = clsobj.verify_token(mock_user.generate_token())

        assert user.username == mock_user.dj_user_id

    def test_verify_invalid_token(self, clsobj):
        """Test user invalid token."""

        with pytest.raises(CustomerNotFound):
            user = clsobj.verify_token("ttttttttttttttt")

    def test_token_authenticate(self, clsobj, mock_user):
        """Test token authentication.

        Asserts:
            Checks the response username

        """
        user = clsobj.token_authenticate(mock_user.generate_token())

        assert user.dj_user_id == mock_user.dj_user_id


@pytest.mark.django_db
class TestCustomerPasswordReset:
    """Password reset test case."""

    def test_customer_password_change(self, clsobj, mock_user):
        """Test customer password changes functionality.

        Asserts:
            1. Success on password reset
            2. UserNotFound error on trying to relogin with old pass
            3. Succes login with new pass
            4. Reset the pass bas

        """
        old_pass = "12345678"
        new_pass = "abcdefgh"

        cus_obj = CustomerController(mock_user)
        cus_obj.reset_password(new_pass)

        # try loggin in with old passoword
        with pytest.raises(InvalidCredentials):
            clsobj.authenticate(mock_user.email, old_pass)

        flat = clsobj.authenticate(mock_user.email, new_pass)
        assert flat.email == mock_user.email

        cus_obj.reset_password(old_pass)

        flat = clsobj.authenticate(mock_user.email, old_pass)
        assert flat.email == mock_user.email
