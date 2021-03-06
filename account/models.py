# -*- coding:utf-8 -*-
# author: JXF
# date: 2018-1-24

from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from notice.models import Notice
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# from django.shortcuts import reverse
# 消息推送
def push(username, event):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        username,
        {
            "type": "push.message",
            "event": event
        }
    )


# 生成初始昵称
def random_name():
    str1 = str(random.choice(range(10000, 999999)))
    str2 = 'WHUer'
    str3 = str2+str1
    return str3


# 上传路径
def get_upload_to(instance, filename):
    user = str(instance.id)
    return 'users/' + user + '-' + 'headimg' + filename[-5:]


# 用户资料
class LoginUser(AbstractUser):
    SEX_CHOICE = (
        ('1', '男'),
        ('2', '女'),
    )
    # 昵称
    nickname = models.CharField(max_length=20, default=random_name(), verbose_name='nickname')
    # 头像
    headimg = models.ImageField(default='users/moren.png', upload_to=get_upload_to, verbose_name='headimg')
    # 签名
    signature = models.CharField(max_length=32, default='这个人很懒，啥也没有留下！', verbose_name='signature')
    # 首次登录时间
    first_time = models.DateTimeField(auto_now_add=True, verbose_name='first_time')
    # 上次登录时间
    last_time = models.DateTimeField(auto_now=True, verbose_name='last_time')
    # 性别
    sex = models.CharField(max_length=2, choices=SEX_CHOICE, default=1)
    # 真实姓名
    real_name = models.CharField(max_length=16, verbose_name="real_name", default="WHUer")
    # 学号
    school_id = models.CharField(max_length=13, verbose_name="school_id", default="", unique=True)
    # 手机
    phone = models.CharField(max_length=11, default="", verbose_name="phone")

    class Meta:
        db_table = 'LoginUser'
        verbose_name_plural = 'user'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    def get_headimg_url(self):
        return settings.PREFIX_URL + settings.QINIU_BUCKET_DOMAIN + '/' + str(self.headimg)
    #
    # def save(self, *args, **kwargs):
    #     self.school_id = int(self.get_username())


class Follow(models.Model):

    # owner = models.ForeignKey(LoginUser, related_name='follows_owner')
    follows = models.ForeignKey(LoginUser, related_name='follows')
    fans = models.ForeignKey(LoginUser, related_name='fans')

    def __str__(self):
        return self.follows.username

    def description(self):
        return {'fans_name': self.fans.nickname, 'fans_headimg': self.fans.get_headimg_url()}

# class Fans(models.Model):
#
#     owner = models.ForeignKey(LoginUser, related_name='fans_owner')
#     fans = models.ForeignKey(LoginUser, related_name='fans')
#
#     class Meta:
#         db_table = 'Fans'
#
#     def __str__(self):
#         return self.owner.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Follow)
def user_follow_notice(sender, instance=None, created=False, **kwargs):
    entity = instance
    if created:
        event = Notice(sender=entity.fans, receiver=entity.follows, event=entity, type=1)
        event.save()
        push(entity.follows.username, {'type': 1})

