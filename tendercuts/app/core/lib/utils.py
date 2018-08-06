"""Core Utilities."""
from app.core.models.customer import CustomerEntityVarchar
from django.db.models import Q


def get_user_id(request):
    """Initialize request user id.

    params:
        request (django request): Request object from Django.

    Returns:
        user_id (str)

    """
    user = request.user
    return get_mage_userid(user)


def get_mage_userid(user):
    """Get the magento user Id from django user object.

    params:
       user (Django user): User object in django.

    Returns:
        Get the user id from the request
        username contains u:18963 => 18963 is the magento IDS
        None in case no valid user Id is found

    """
    user_id = user.username.split(":")

    if len(user_id) < 1:
        user_id = None
    else:
        user_id = user_id[1]

    return user_id
