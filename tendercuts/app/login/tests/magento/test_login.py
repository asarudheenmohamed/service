import pytest
import uuid
from random import randint

@pytest.fixture
def api(magento):
    return magento.api

class _TestLogin:
    def test_customer_login_with_mail(self, api):
        status = api.tendercuts_customer_apis.login("mail@varun.xyz", "qwerty123")

        assert status['status'] is True


    def test_customer_login_with_ph(self, api):
        status = api.tendercuts_customer_apis.login("9908765678", "qwerty123")
        assert status['status'] is True


    def test_customer_login_with_ph_failure(self, api):
        status = api.tendercuts_customer_apis.login("990765678", "qwerty123")

        assert status['status'] is False


    def test_customer_login_with_email_failure(self, api):
        status = api.tendercuts_customer_apis.login("mail@emil.com", "qwerty123")
        assert status['status'] is False


class TestSignUp:
    def test_endpoint(self, api):
        assert getattr(api.tendercuts_customer_apis, "signup", None)

    def test_login_create_success(self, api):
        """
        1. Create new
        2. Verify if the login happens with email and phnumber

        expected:
            1. User created and logged in
        """

        phno = randint(8000000000, 9999999999)
        password = "foobarbaz"
        email = "{}@test.com".format(uuid.uuid4())
        status = api.tendercuts_customer_apis.signup(
            "Test",
            email,
            str(phno),
            password)

        assert status['status'] == True

        status = api.tendercuts_customer_apis.login(str(phno), password)
        assert status['status'] is True

        status = api.tendercuts_customer_apis.login(str(email), password)
        assert status['status'] is True

    def test_signup_with_same_mail(self, api):
        """
        1. Create new with exiting username

        expected:
            1.  Should fail
        """
        status = api.tendercuts_customer_apis.signup(
            "Test",
            "mail@varun.xyz",
            "1212121212",
            "foobarbaz")

        assert status['status'] == False

    def test_signup_with_same_phone(self, api):
        """
        1. Create new with exiting username

        expected:
            1.  Should fail
        """
        status = api.tendercuts_customer_apis.signup(
            "Test",
            "mail@var.xyz",
            "9908765678",
            "foobarbaz")

        assert status['status'] == False





