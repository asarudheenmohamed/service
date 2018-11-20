import logging

import jwt
from django.conf import settings

logger = logging.getLogger()


def verify_token(token):
    """Helper method to validate the token from flock"""
    try:
        resp = jwt.decode(
            token,
            settings.FLOCK_ADMIN_BOT_AUTH['APP_SECRET'],
            settings.FLOCK_ADMIN_BOT_AUTH['ALGO'])

        if resp['appId'] == settings.FLOCK_ADMIN_BOT_AUTH['APP_ID']:
            return resp

        raise Exception
    # bad, we just catch any exception and return None
    except Exception:
        return None
