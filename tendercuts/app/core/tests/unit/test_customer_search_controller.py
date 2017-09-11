"""Test cases for generating flat customer."""

import pytest

from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.exceptions import CustomerNotFound, InvalidCredentials


@pytest.fixture
def cls():
    """As s fixture wrapper for the class."""
    return CustomerSearchController


@pytest.mark.django_db
class TestCustomerControllerFetch(object):
    """Companion for CustomerController."""

    def _verify_user(self, user, expected_user):
        """As a simple unifed class for verify user."""
        user = user._flat
        # assert isinstance(user, CustomerEntity)
        assert user['email'] == expected_user.email
        assert user['mobilenumber'] == expected_user.mobilenumber
        assert user['firstname'] == expected_user.firstname
        # assert user.is_valid is True
        # assert if we are also fetching the billing address
        assert user['default_billing'] == user['address'][0]['address_id']
        assert 'thoraipakkam' == user['address'][0]['designated_store']

    def test_customer_fetch(self, cls, mock_user):
        """Test Fetch customer data based on customer id.

        Asserts:
         load by customer is valid

        """
        user = cls.load_by_id(mock_user.entity_id)
        self._verify_user(user, mock_user)

    def test_customer_fetch_by_phone(self, cls, mock_user):
        """Test customer data based on phone number.

        Asserts:
         load by customer ph no is valid

        """
        user = cls.load_by_phone_mail(mock_user.mobilenumber)
        self._verify_user(user, mock_user)

    def test_customer_fetch_by_mail(self, cls, mock_user):
        """Test Fetch customer data based on phone number.

        Asserts:
         load by customer mail is valid

        """
        user = cls.load_by_phone_mail(mock_user.email)
        self._verify_user(user, mock_user)

    def test_customer_fetch_negative(self, cls):
        """Test Fetch customer data based on email id.

        Asserts:
         load by customer mail fails

        """
        with pytest.raises(CustomerNotFound):
            cls.load_by_phone_mail("il@varun.xyz")

        with pytest.raises(CustomerNotFound):
            cls.load_by_id(99999999)


@pytest.mark.django_db
class TestCustomerBasicInfoSearch:
    """Test the class method of FlatCustomer."""

    def test_basic_info(self, cls, mock_user):
        """Test basic information in test user.

        Asserts:
            1. basic info is fetched
            2. mail, ph and name

        """
        user_data = cls.load_basic_info(mock_user.entity_id)
        assert user_data is not None
        assert user_data[0] == mock_user.entity_id
        assert str(user_data[1]) == mock_user.email
        assert str(user_data[2]) == mock_user.mobilenumber
        assert mock_user.firstname in user_data[3]

    def test_basic_info_for_unknown(self, cls):
        """Test invalid basic informaion Exception.

        Asserts:
            1. Raise exception for invliad customer

        """
        with pytest.raises(Exception) as exc:
            cls.load_basic_info(189631)
            assert "CustomerNotFound" in str(exc.value)
