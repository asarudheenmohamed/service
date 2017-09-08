"""Endpoint for the Profix key."""


def generate_profix_key(profix, key):
    """Generate the profix key."""
    return "{}:{}".format(profix, key)
