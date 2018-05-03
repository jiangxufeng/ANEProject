# -*- coding:utf-8 -*-
# author: JXF
# date:2018-1-24

from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    ImageField,
    ReadOnlyField,
    ValidationError,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
)
from .models import LoginUser, Follow


# 关注返回信息
class FollowSerializer(HyperlinkedModelSerializer):
    follow = HyperlinkedRelatedField(
        view_name='user_detail',
        lookup_field='username',
        many=True,
        read_only=True
    )

    class Meta:
        model = Follow
        fields = (
            'follow',
        )


# 粉丝返回信息
class FansSerializer(HyperlinkedModelSerializer):
    fans = HyperlinkedRelatedField(many=True, view_name='user_detail', read_only=True)

    class Meta:
        model = Follow
        fields = (
            'fans',
        )


# 用户详情
class UserDetailSerializer(ModelSerializer):
    # username = ReadOnlyField()
    headimg = ImageField(default='moren.jpeg')
    # id = ReadOnlyField()
    # last_time = ReadOnlyField()
    # school_id = ReadOnlyField()
    # real_name = ReadOnlyField()
    # phone = ReadOnlyField()
    books = HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='book_detail'
    )

    class Meta:
        model = LoginUser
        fields = (
            'headimg',
            'id',
            'last_time',
            'nickname',
            'username',
            'school_id',
            'real_name',
            'signature',
            'sex',
            'phone',
            'books'
        )
        read_only_fields = ('username', 'id', 'last_time', 'school_id', 'real_name', 'phone')

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
        fields = (
            'username',
            'password',
        )
        extra_kwargs = {
            "password": {"write_only": True}
        }


# 修改密码
class UserPasswordResetSerializer(ModelSerializer):
    password = CharField(style={'input_type': 'password'})

    class Meta:
        model = LoginUser
        fields = (
            'password',
        )
        extra_kwargs = {
            "password": {"write_only": True}
        }


# 绑定手机
class UserBindPhoneSerializer(ModelSerializer):

    class Meta:
        model = LoginUser
        fields = (
            'phone',
        )

    def validate_phone(self, value):
        data = self.get_initial()['phone']
        if len(data) != 11:
            raise ValidationError("Invalid cell phone number.")
        elif data[0] != '1':
            raise ValidationError("Invalid cell phone number.")
        return value

