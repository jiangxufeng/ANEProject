# -*- coding:utf-8 -*-
# author: JXF
# date: 2018-1-27
from rest_framework import permissions
from rest_framework.authtoken.models import Token
import hashlib
from account.models import LoginUser
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import ugettext_lazy as _


class MyAuthenticationFalied(AuthenticationFailed):
    default_detail = _('Invalid token, Please login again.')


# 是否为当前用户
class IsOwner(permissions.BasePermission):
    """
    当前登录的用户只能获取与修改自己的资料
    """
    def has_object_permission(self, request, view, obj):
        key = request.META.get("HTTP_AUTHORIZATION")[6:]
        token = Token.objects.filter(key=key)
        if token is None:
            return False
        return token[0].user.username == obj.username


def get_authentication(sign, pk):
    try:
        user = LoginUser.objects.get(id=pk)
        token = Token.objects.get(user=user).key
        res = str(pk) + token
        if hashlib.md5(res.encode()).hexdigest() == sign:
            return user
        raise MyAuthenticationFalied
    except LoginUser.DoesNotExist:
        raise Http404
