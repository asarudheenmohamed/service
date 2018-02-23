from django.contrib.auth.models import User, Group
import pytest

@pytest.mark.django_db
def test_sm_login(rest):
    """verify login api.
    Verify if we got a user tokenc
    """

    user = User.objects.create_user(
        email="thoriapakkam@gmail.com",
        username="thoraipakkam",
        password="qwerty123")
    user.save()

    my_group = Group.objects.get(name='Store Manager')
    my_group.user_set.add(user)


    response = rest.post(
        "/store_manager/login/",
        {'email': "thoraipakkam", 'password': "qwerty123"},
        format='json')

    assert response.data['token'] is not None

@pytest.mark.django_db
def test_not_sm_login(rest):
    """verify login fails"""

    user = User.objects.create_user(
        email="thoriapakkam@gmail.com",
        username="thoraipakkam",
        password="qwerty123")
    user.save()

    response = rest.post(
        "/store_manager/login/",
        {'email': "thoraipakkam", 'password': "qwerty123"},
        format='json')

    assert response.status_code == 403


