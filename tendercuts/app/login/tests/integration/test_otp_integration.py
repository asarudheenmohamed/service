"""Integration testing on otp via login and forgot password."""
import pytest
from pytest_bdd import given, scenario, then, when

from app.core.lib.otp_controller import OtpController
from app.core.lib.redis_controller import RedisController


@pytest.mark.django_db
@scenario(
    'otp.feature',
    'Login via OTP',
)
def test_loginvia():
    pass


@pytest.mark.django_db
@scenario(
    'otp.feature',
    'forgot password',
)
def test_forgot_pass():
    pass


@given('Generating OTP for the given otp type and mobile number <otp_type><phone>')
def generate_otp(cache, rest, otp_type, phone):
    """Test Send otp for customer mobile number.

    Params:
     auth_rest(pytest fixture): user requests
     otp_type(str): otp types are login,signup and forgot
     phone(number): Customer mobile number

    Asserts:
        Check response mobile is equal to test mobile number

    """
    response = rest.get(
        "/user/otp_view/{}/?otp_type={}".format(phone, otp_type),
        format='json')
    cache['mobile'] = response.data['mobile']
    assert response.data['mobile'] == phone


def get_otp(mobile, otp_type):
    """Get Otp based on custemer mobile number and otp type.

    Params:
     mobile(number): customer mobile number
     otp_type(str): otp types are login,signup and forgot

    Returns:
        return a otp

    """
    key = OtpController()._generate_redis_key(mobile, otp_type)
    otp = RedisController().get_key(key)
    return otp


@when('Validating the user entered OTP <otp_type><phone><status><message>')
def otp_validation(cache, auth_rest, phone, otp_type, status, message):
    """Test Otp validation.

    Params:
     rest(pytest fixture): user requests
     otp_type(str): otp types are login,signup and forgot

    Asserts:
        Check response mobile is equal to test mobile number

    """
    otp = get_otp(phone, otp_type)
    if status == 'False':
        otp = 1111
    response = auth_rest.get(
        "/user/otp_validation/{}/?otp_type={}&otp={}".format(
            phone, otp_type, otp),
        format='json')
    assert str(response.data['status']) == status
    assert response.data['message'] == message


@given('Resend otp for text and voice method <otp_type><phone><resend_type>')
def resend_otp_methods(auth_rest, otp_type, phone, resend_type):
    """Test resend otp methods.

    Params:
     auth_rest(pytest fixture): user requests
     otp_type(str): otp types are login,signup and forgot
     phone(number): customer mobile number
     resend_type(str): otp resend otp methods are text and voice

    Asserts:
        Check response mobile is equal to test mobile number

    """
    response = auth_rest.get(
        "/user/otp_view/{}/?resend_type={}&otp_type={}".format(
            phone, resend_type, otp_type),
        format='json')
    assert response.data['mobile'] == phone


@then('LogIn the user')
def otp_via_login(cache, auth_rest):
    """Test Otp via login.

    Params:
     auth_rest(pytest fixture): user requests

    Asserts:
     Check response mobile is equal to test mobile number

    """
    data = {"phone": cache['mobile'], "otp_mode": True}
    response = auth_rest.post("/user/login", data=data)
    assert response.data['mobilenumber'] == cache['mobile']


@then('forgot a password <phone><otp_type>')
def forgot_password(auth_rest, phone, otp_type):
    """Test forgot password.

    Params:
     auth_rest(pytest fixture): user requests
     phone(number): customer mobile number
     otp_type(str): otp types are login,signup and forgot

    Asserts:
     Check response mobile is equal to test mobile number

    """
    otp = get_otp(phone, otp_type)
    data = {"mobile": phone, "otp": otp}
    response = auth_rest.post("/user/forgot_password_otp/", data=data)
    assert response.data['mobile'] == phone
