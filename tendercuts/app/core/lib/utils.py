"""Core Utilities."""


def get_user_id(request):
    """Initialize request user id.

    params:
        request (django request): Request object from Django.

    Returns:
        Get the user id from the request
        username contains u:18963 => 18963 is the magento IDS
        None in case no valid user Id is found

    """
    user = request.user
    user_id = user.username.split(":")

    if len(user_id) < 1:
        user_id = None
    else:
        user_id = user_id[1]

    return user_id
