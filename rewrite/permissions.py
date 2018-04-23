# -*- coding:utf-8 -*-
# author: JXF
# date: 2018-1-27
from rest_framework import permissions
from rest_framework.authtoken.models import Token


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
        # print(token[0].user.username)
        # print(obj.username)
        return token[0].user.username == obj.username


