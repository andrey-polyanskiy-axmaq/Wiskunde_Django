from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
import logging
from datetime import datetime

logger = logging.getLogger('auth_backend')


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        usermod = get_user_model()

        users = usermod.objects.filter(Q(username__iexact=username) | Q(email__iexact=username))
        logger.debug(f"{datetime.now()} Authenticating user: {username}")

        for user in users:
            if user.check_password(password):
                logger.debug(f"{datetime.now()} User authenticated: {username}")
                return user
            else:
                logger.warning(f"{datetime.now()} Failed to authenticate user (wrong password): {username}")

        logger.warning(f"{datetime.now()} User not found: {username}")
        return None
