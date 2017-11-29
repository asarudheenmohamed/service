"""Test driver login."""

import pytest


@pytest.mark.django_db
def test_driver_login(rest, mock_driver):
    """Test both driver and user login.

    Params:
        auth_rest(pytest fixture):user requests

    returns:
            this is return a user id request

    Asserts:
        Check response not equal to None
        Check response status code in equal to 200
        Check custermer id is equal to 18963

    """

    # driver login
    response = rest.post(
        "/driver/login/",
        {'phone': mock_driver._flat['mobilenumber'], 'password': "12345678"},
        format='json')

    assert response.json()['mobilenumber'] == mock_driver._flat['mobilenumber']
