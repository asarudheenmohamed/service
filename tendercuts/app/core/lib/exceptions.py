class OrderNotFound(Exception):
    pass


class AuthenticationException(Exception):
    """Authendication Exception."""

    pass


class CustomerNotFound(AuthenticationException):
    """Customer object not found Exception."""

    pass


class InvalidCredentials(AuthenticationException):
    """Invalid credentials Exception."""

    pass