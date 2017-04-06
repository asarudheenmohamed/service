import pytest
from app.core.models.customer import *


@pytest.fixture
def cls():
    return FlatCustomer

class TestCustomerControllerFetch:


    def _verify_user(self, user):
        user = user._flat
        # assert isinstance(user, CustomerEntity)
        assert user['email'] == "mail@varun.xyz"
        assert user['mobilenumber'] == "9908765678"
        assert user['firstname'] == "TEST"
        # assert user.is_valid is True

    def test_instance(self, cls):
        assert cls is not None

    def test_customer_fetch(self, cls):
        user = cls.load_by_id(18963)
        self._verify_user(user)

    def test_customer_fetch_by_phone(self, cls):
        user = cls.load_by_phone_mail("9908765678")
        self._verify_user(user)

    def test_customer_fetch_by_phone(self, cls):
        user = cls.load_by_phone_mail("mail@varun.xyz")
        self._verify_user(user)

    def test_customer_fetch_negative(self, cls):
        with pytest.raises(CustomerNotFound):
            user = cls.load_by_phone_mail("il@varun.xyz")

        with pytest.raises(CustomerNotFound):
            user = cls.load_by_id(99999999)


class TestCustomerControllerAuth:
    def test_invalid_password(self, cls):
        with pytest.raises(InvalidCredentials):
            user_controller = cls.authenticate("mail@varun.xyz", "qwerty")

    def test_invalid_username(self, cls):
        with pytest.raises(CustomerNotFound):
            user_controller = cls.authenticate("mail@varun.xy", "qwerty123")

    def test_invalid_username(self, cls):
        flat = cls.authenticate("mail@varun.xyz", "qwerty123")
        assert flat.customer.email == "mail@varun.xyz"
