"""Endpoint for the Prefix key."""

PREFIX_PINCODE = "PINCODE"


def generate_prefix_key(prefix, key):
    """Generate the prefix key."""
    return "{}:{}".format(prefix, key)
