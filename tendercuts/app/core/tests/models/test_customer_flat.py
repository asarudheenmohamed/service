"""Test cases for generating flat customer."""

import pytest
from app.core.models.customer import *
from app.core.lib.user_controller import *


@pytest.fixture
def cls():
    """A fixture wrapper for the class."""
    return CustomerSearchController


@pytest.fixture
def clsobj():
    """A fixture wrapper for the class."""
    return CustomerController


@pytest.mark.django_db
class TestCustomerControllerFetch:
    """Companion for CustomerController."""

    def _verify_user(self, user):
        """A simple unifed class for verify user."""
        user = user._flat
        # assert isinstance(user, CustomerEntity)
        assert user['email'] == "mail@varun.xyz"
        assert user['mobilenumber'] == "9908765678"
        assert user['firstname'] == "TEST"
        # assert user.is_valid is True

    def test_instance(self, cls):
        """A obj class validation.

        Asserts:
         Instance is valid

        """
        assert cls is not None

    def test_customer_fetch(self, clsobj):
        """Test Fetch customer data based on customer id.

        Asserts:
         load by customer is valid

        """
        user = clsobj.load_customer_obj(18963)
        self._verify_user(user)

    def test_customer_fetch_by_phone(self, cls):
        """Test customer data based on phone number.

        Asserts:
         load by customer ph no is valid

        """
        user = cls.load_by_phone_mail("9908765678")
        self._verify_user(user)

    def test_customer_fetch_by_mail(self, cls):
        """Test Fetch customer data based on phone number.

        Asserts:
         load by customer mail is valid

        """
        user = cls.load_by_phone_mail("mail@varun.xyz")
        self._verify_user(user)

    def test_customer_fetch_negative(self, cls, clsobj):
        """Test Fetch customer data based on email id.

        Asserts:
         load by customer mail fails

        """
        with pytest.raises(CustomerNotFound):
            user = cls.load_by_phone_mail("il@varun.xyz")

        with pytest.raises(CustomerNotFound):
            user = clsobj.load_customer_obj(99999999)


@pytest.mark.django_db
class TestCustomerControllerAuth:
    """Test Customer controller.

    Asserts: Auth related test cases.

    """

    def test_invalid_password(self, clsobj):
        """Test user invalid password.

        Asserts:
        1. Failure on login with invalid password

        """
        with pytest.raises(InvalidCredentials):
            user_controller = clsobj.authenticate(
                "mail@varun.xyz", "qwerty", None)

    def test_invalid_username(self, clsobj):
        """Test user invalid username.

        Asserts:
            1. Failure on login with invalid username

        """
        with pytest.raises(CustomerNotFound):
            user_controller = clsobj.authenticate(
                "mail@varun.xy", "qwerty123", None)

    def test_valid_username(self, clsobj):
        """Test user valid username.

        Asserts:
            1. Succes on login with valid username

        """
        flat = clsobj.authenticate(
            "mail@varun.xyz", "qwerty123", None)
        assert flat.customer.email == "mail@varun.xyz"


@pytest.mark.django_db
class TestCustomerPasswordReset:
    """Password reset test case."""

    def test_customer_password_change(self, clsobj):
        """Test customer password changes functionality.

        Asserts:
            1. Success on password reset
            2. UserNotFound error on trying to relogin with old pass
            3. Succes login with new pass
            4. Reset the pass bas

        """
        user = clsobj.load_customer_obj(18963)
        user.reset_password("qwerty123123")

        with pytest.raises(CustomerNotFound):
            user_controller = clsobj.authenticate(
                "mail@varun.xy", "qwerty123123", None)

        flat = clsobj.authenticate(
            "mail@varun.xyz", "qwerty123123", None)
        assert flat.customer.email == "mail@varun.xyz"

        user.reset_password("qwerty123")

        flat = clsobj.authenticate(
            "mail@varun.xyz", "qwerty123", None)
        assert flat.customer.email == "mail@varun.xyz"


@pytest.mark.django_db
class TestFlatCustomerClassMethods:
    """Test the class method of FlatCustomer."""

    def test_basic_info(self, cls):
        """Test basic information in test user.

        Asserts:
            1. basic info is fetched
            2. mail, ph and name

        """
        user_data = cls.load_basic_info(18963)
        assert user_data is not None
        assert user_data[0] == 18963
        assert str(user_data[1]) == "mail@varun.xyz"
        assert str(user_data[2]) == "9908765678"
        assert "TEST" in str(user_data[3])

    def test_basic_info_for_unknown(self, cls):
        """Test invalid basic informaion Exception.

        Asserts:
            1. Raise exception for invliad customer

        """
        with pytest.raises(Exception) as exc:
            _ = cls.load_basic_info(189631)
            assert "CustomerNotFound" in str(exc.value)
