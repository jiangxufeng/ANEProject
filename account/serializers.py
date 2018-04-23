# -*- coding:utf-8 -*-
# author: JXF
# date:2018-1-24

from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    ImageField,
    ReadOnlyField,
    ValidationError,
    SerializerMethodField,
)
from .models import LoginUser


# 用户详情
class UserDetailSerializer(ModelSerializer):
    username = ReadOnlyField()
    headimg = ImageField(default='moren.jpeg')
    id = ReadOnlyField()
    last_time = ReadOnlyField()
    school_id = ReadOnlyField()
    real_name = ReadOnlyField()

    class Meta:
        model = LoginUser
        fields = [
            'headimg',
            'id',
            'last_time',
            'nickname',
            'username',
            'school_id',
            'real_name',
            'sex',
            'phone',
        ]

    def get_sex(self, obj):
        return obj.get_sex_display()

    # def get_username(self, obj):
    #     return obj.username
    #
    # def get_headimg(self, obj):
    #     return obj.headimg


# 用户登录创建
class UserLoginSerializer(ModelSerializer):
    username = CharField()
    password = CharField(style={'input_type': 'password'})

    class Meta:
        model = LoginUser
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }


class UserPasswordResetSerializer(ModelSerializer):
    password = CharField(style={'input_type': 'password'})

    class Meta:
        model = LoginUser
        fields = [
            'password',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }
