import pytest
from django.contrib.auth.models import User

from rest_framework.views import APIView


# @pytest.fixture
# def view():
#     return views.DriverViewSet.as_view({"get": "retrieve"})


def _test_driver_login(rest, auth, username, password):
    """
    Kinda weird because, the login also serves as a usercreation in django

    Verify:
    1. user details retrieved.
    2. Django user created only once
    3. Django user is associated with the request
    """
    rest.credentials(HTTP_AUTHORIZATION=auth)
    response = rest.get("/drivers/account/{}/".format(username), format='json')

    assert response.data['phone'] == username
    assert response.data['name'] == "Tester1"

    # check if django user is created
    user = User.objects.get(username=username)
    assert user is not None
    assert user.username == username



