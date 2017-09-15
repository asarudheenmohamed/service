"""Integration testing on otp via login and forgot password."""
import pytest
from pytest_bdd import given, scenario, then, when

from app.otp.lib.otp_controller import OtpController
from app.core.lib import cache


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


@given('Generating OTP for the given mobile number: <phone> <otp_type>')
def generate_otp(cache, rest, phone, otp_type):
    """Test Send otp for customer mobile number.

    Params:
        auth_rest(pytest fixture): user requests
        phone(number): Customer mobile number
        otp_type(str): otp types are login,signup and forgot

    Asserts:
        Check response mobile is equal to test mobile number

    """
    response = rest.post(
        "/otp/generate/", {'mobile': phone, 'otp_mode': otp_type},
        format='json')
    cache['mobile'] = response.data['mobile']
    cache['otp_type'] = otp_type
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
    otp = cache.get_key(key)

    return otp


@when('the user enter the OTP <status> then the message should be <message>')
def otp_validation(cache, auth_rest, status, message):
    """Test Otp validation.

    Params:
        auth_rest(pytest fixture): user requests
        status(str): otp validation status
        message(str): otp validation message

    Asserts:
        Check response mobile is equal to test mobile number

    """
    otp = get_otp(cache['mobile'], cache['otp_type'])
    if status == 'False':
        otp = 1111
    response = auth_rest.post(
        "/otp/verify/", {'mobile': cache['mobile'],
                         'otp_mode': cache['otp_type'], 'otp': otp},
        format='json')

    assert str(response.data['status']) == status
    assert response.data['message'] == message


@given('the customer requests a resend via <resend_type>')
def resend_otp_methods(cache, auth_rest, resend_type):
    """Test resend otp methods.

    Params:
        auth_rest(pytest fixture): user requests
        resend_type(str): otp resend otp methods are text and voice

    Asserts:
        Check response mobile is equal to test mobile number

    """
    response = auth_rest.post(
        "/otp/retry/", {'mobile': cache['mobile'],
                        'otp_mode': cache['otp_type'], 'retry_mode': resend_type},
        format='json')
    assert response.data['status'] == True
    assert response.data['message'] == 'Successfully resend otp'


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


@then('forgot a password')
def forgot_password(cache, auth_rest):
    """Test forgot password.

    Params:
        auth_rest(pytest fixture): user requests

    Asserts:
        Check response mobile is equal to test mobile number

    """
    otp = get_otp(cache['mobile'], cache['otp_type'])
    data = {"mobile": cache['mobile'], "otp": otp}
    response = auth_rest.post("/user/forgot_password_otp/", data=data)
    assert response.data['mobile'] == cache['mobile']
