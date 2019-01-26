# -*- coding:utf-8 -*-
from functools import wraps
import datetime
from account.models import LoginUser
from django.conf import settings
# from rest_framework.authentication import TokenAuthentication
# from rest_framework import exceptions
# from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BaseAuthentication
from .exception import FoundUserFailed, MissingParameter, MyAuthenticationFailed
import hashlib
# from django.core.cache import cache

EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


# 用户认证
class MyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        :param pk: 用户id, 默认为None
        :param request: 当前请求
        :return: user 当前用户
        认证方式： pk + token + timestamp 的md5加密值是否与sign相等
        """
        pk = request.META.get('HTTP_NAMEPLATE')
        sign = request.META.get('HTTP_SIGN')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        if not pk:
            return None

        if not sign:
            return None

        if not timestamp:
            return None

        try:
            user = LoginUser.objects.get(id=pk[3:-2])
            token = Token.objects.get(user=user).key
            res = str(pk[3:-2]) + token + timestamp
        except LoginUser.DoesNotExist:
            raise FoundUserFailed
        else:
            if hashlib.md5(res.encode()).hexdigest() == sign:
                user.save()  # 更新最后登录时间
                return user, None
            raise MyAuthenticationFailed


# channels用户认证
def ws_auth_request_token(func):
    """
    Checks the presence of a "token" request parameter and tries to
    authenticate the user based on its content.
    The request url must include token.
    eg: /v1/channel/1/?token=abcdefghijklmn
    """

    @wraps(func)
    def inner(req, *args, **kwargs):
        headers = dict(req.scope['headers'])
        pk = headers[b'sign'].decode()
        sign = headers[b'sign'].decode()
        timestamp = headers[b'sign'].decode()

        if not pk:
            _close_reply_channel(req)
            raise ValueError("Missing token request parameter. Closing channel.")

        if not sign:
            _close_reply_channel(req)
            raise ValueError("Missing token request parameter. Closing channel.")

        if not timestamp:
            _close_reply_channel(req)
            raise ValueError("Missing token request parameter. Closing channel.")

        try:
            user = LoginUser.objects.get(id=pk[3:-2])
            token = Token.objects.get(user=user).key
            res = str(pk[3:-2]) + token + timestamp
        except LoginUser.DoesNotExist:
            raise FoundUserFailed
        else:
            if hashlib.md5(res.encode()).hexdigest() == sign:
                user.save()  # 更新最后登录时间
                return func(req, *args, **kwargs)
            raise MyAuthenticationFailed

    return inner


# 关闭websocket连接
def _close_reply_channel(req):
    req.close()


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
            'nickname': user.nickname,
            'token': token.key,
        }
    }
    return content
