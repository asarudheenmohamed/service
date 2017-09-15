"""Endpoint for the Prefix key."""


def generate_prefix_key(prefix, key):
    """Generate the prefix key."""
    return "{}:{}".format(prefix, key)
