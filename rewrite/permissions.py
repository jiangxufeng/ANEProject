# -*- coding:utf-8 -*-
# author: JXF
# date: 2018-1-27
from rest_framework import permissions
from rest_framework.authtoken.models import Token
import hashlib
from account.models import LoginUser
from .exception import MyAuthenticationFailed, FoundUserFailed, MissingParameter


# 拥有者是否为当前用户
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        当请求方式为POST、PUT、DELETE等非安全方式时，判断obj拥有者是否为当前认证用户
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


# 申请接受者是否为当前认证用户
class IsReceiver(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.receiver == request.user


def get_authentication(request, pk=None):
    """
    :param pk: 用户id, 默认为None
    :param request: 当前请求
    :return: user 当前用户
    认证方式： pk + token + timestamp 的md5加密值是否与sign相等
    """
    try:
        if pk is None:
            pk = request.META.get('HTTP_NAMEPLATE')[3:-2]
        sign = request.META.get('HTTP_SIGN')
        timestamp = request.META.get('HTTP_TIMESTAMP')
        user = LoginUser.objects.get(id=pk)
        token = Token.objects.get(user=user).key
        res = str(pk) + token + timestamp
    except LoginUser.DoesNotExist:
        raise FoundUserFailed
    except TypeError:  # 没有对应的请求头
        raise MissingParameter
    else:
        if hashlib.md5(res.encode()).hexdigest() == sign:
            user.save()  # 更新最后登录时间
            return user
        raise MyAuthenticationFailed
