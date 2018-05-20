# -*- coding:utf-8 -*-
# author: JXF
# date:2018-1-24

from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    ImageField,
    IntegerField,
    ValidationError,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    SerializerMethodField,
)
from .models import LoginUser, Follow#, Fans
from django.shortcuts import reverse


# 关注返回信息
class FollowSerializer(ModelSerializer):
    # follows = HyperlinkedRelatedField(view_name='user_detail', many=True, read_only=True)
    url = SerializerMethodField()
    headimg = SerializerMethodField()
    nickname = SerializerMethodField()
    signature = SerializerMethodField()
    sex = SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'url',
            'headimg',
            'nickname',
            'signature',
            'sex',
        )

    def get_url(self, obj):
      #  print(obj.follows.headimg)
        return reverse('user_detail', args=(obj.follows.id,))

    def get_headimg(self, obj):
        return obj.follows.get_headimg_url()

    def get_nickname(self, obj):
        return obj.follows.nickname

    def get_signature(self, obj):
        return obj.follows.signature

    def get_sex(self, obj):
        return obj.follows.sex


# 粉丝返回信息
class FansSerializer(ModelSerializer):
    url = SerializerMethodField()
    headimg = SerializerMethodField()
    nickname = SerializerMethodField()
    signature = SerializerMethodField()
    sex = SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            #    'owner',
            'url',
            'headimg',
            'nickname',
            'signature',
            'sex',
        )

    def get_url(self, obj):
        #  print(obj.follows.headimg)
        return reverse('user_detail', args=(obj.fans.id,))

    def get_headimg(self, obj):
        return obj.fans.get_headimg_url()

    def get_nickname(self, obj):
        return obj.fans.nickname

    def get_signature(self, obj):
        return obj.fans.signature

    def get_sex(self, obj):
        return obj.fans.sex

# 用户详情
class UserDetailSerializer(ModelSerializer):
    # username = ReadOnlyField()
    headimg = ImageField(default='moren.jpeg')
    bookNum = SerializerMethodField()
    userId = IntegerField(source='id')
    fansNum = SerializerMethodField()
    followNum = SerializerMethodField()

    class Meta:
        model = LoginUser
        fields = (
            'headimg',
            'userId',
            'last_time',
            'nickname',
            'username',
            'school_id',
            'real_name',
            'signature',
            'sex',
            'phone',
            'bookNum',
            'fansNum',
            'followNum',
        )
        read_only_fields = ('username', 'userId', 'last_time', 'school_id', 'real_name', 'phone')

    def get_fansNum(self, obj):
        return obj.follows.all().count()

    def get_followNum(self, obj):
        return obj.fans.all().count()

    def get_bookNum(self, obj):
        return obj.books.all().count()

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

