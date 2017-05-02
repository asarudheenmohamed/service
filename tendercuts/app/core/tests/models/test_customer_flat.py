"""
Test cases for generating flat customer, ideally needs to be moved to a
serializer.
"""

import pytest
from app.core.models.customer import *


@pytest.fixture
def cls():
    """
    A fixture wrapper for the class
    """
    return FlatCustomer


class TestCustomerControllerFetch:
    """
    Companion for CustomerController
    """

    def _verify_user(self, user):
        """
        A simple unifed class for verify user
        """
        user = user._flat
        # assert isinstance(user, CustomerEntity)
        assert user['email'] == "mail@varun.xyz"
        assert user['mobilenumber'] == "9908765678"
        assert user['firstname'] == "TEST"
        # assert user.is_valid is True

    def test_instance(self, cls):
        """
        Asserts:
         Instance is valid
        """
        assert cls is not None

    def test_customer_fetch(self, cls):
        """
        Asserts:
         load by customer is valid
        """
        user = cls.load_by_id(18963)
        self._verify_user(user)

    def test_customer_fetch_by_phone(self, cls):
        """
        Asserts:
         load by customer ph no is valid
        """
        user = cls.load_by_phone_mail("9908765678")
        self._verify_user(user)

    def test_customer_fetch_by_mail(self, cls):
        """
        Asserts:
         load by customer mail is valid
        """
        user = cls.load_by_phone_mail("mail@varun.xyz")
        self._verify_user(user)

    def test_customer_fetch_negative(self, cls):
        """
        Asserts:
         load by customer mail fails
        """
        with pytest.raises(CustomerNotFound):
            user = cls.load_by_phone_mail("il@varun.xyz")

        with pytest.raises(CustomerNotFound):
            user = cls.load_by_id(99999999)


class TestCustomerControllerAuth:
    """
    Asserts: Auth related test cases.
    """

    def test_invalid_password(self, cls):
        """
        Asserts:
        1. Failure on login with invalid password
        """
        with pytest.raises(InvalidCredentials):
            user_controller = cls.authenticate("mail@varun.xyz", "qwerty")

    def test_invalid_username(self, cls):
        """
        Asserts:
            1. Failure on login with invalid username
        """
        with pytest.raises(CustomerNotFound):
            user_controller = cls.authenticate("mail@varun.xy", "qwerty123")

    def test_valid_username(self, cls):
        """
        Asserts:
            1. Succes on login with valid username
        """
        flat = cls.authenticate("mail@varun.xyz", "qwerty123")
        assert flat.customer.email == "mail@varun.xyz"


class TestCustomerPasswordReset:
    """
    Password reset test case
    """

    def test_customer_password_change(self, cls):
        """
        Asserts:
            1. Success on password reset
            2. UserNotFound error on trying to relogin with old pass
            3. Succes login with new pass
            4. Reset the pass bas
        """
        user = cls.load_by_id(18963)
        user.reset_password("qwerty123123")

        with pytest.raises(CustomerNotFound):
            user_controller = cls.authenticate("mail@varun.xy", "qwerty123")

        flat = cls.authenticate("mail@varun.xyz", "qwerty123123")
        assert flat.customer.email == "mail@varun.xyz"

        user.reset_password("qwerty123")

        flat = cls.authenticate("mail@varun.xyz", "qwerty123")
        assert flat.customer.email == "mail@varun.xyz"
