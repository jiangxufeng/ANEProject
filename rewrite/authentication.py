# -*- coding:utf-8 -*-

import datetime
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.core.cache import cache

EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


class ExpiringTokenAuthentication(TokenAuthentication):
    """Set up token expired time"""

    def authenticate_credentials(self, key):
        # Search token in cache
        cache_user = cache.get(key)
        if cache_user:
            return cache_user, key

        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        time_now = datetime.datetime.now()

        if token.created < time_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
            raise exceptions.AuthenticationFailed(_('Token has expired. Please login again'))
            #raise Response()
        if token:
            # Cache token
            cache.set(key, token.user, EXPIRE_MINUTES * 60)

        return token.user, token


# token过期验证
def expire_token(user):
    token, created = Token.objects.get_or_create(user=user)
    time_now = datetime.datetime.now()

    if created or token.created < time_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
        # update the token
        token.delete()
        token = Token.objects.create(user=user)
        token.created = time_now
        token.save()

    content = {
        'error': "0",
        'data': {
            'uid': user.id,
            'username': user.username,
            'token': token.key,
        }
    }
    return content
