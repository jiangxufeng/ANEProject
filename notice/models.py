from django.db import models
from django.conf import settings
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


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


# Create your models here.
# 消息通知
class Notice(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notice_sender')  # 发送者
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notice_receiver')  # 接收者
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    event = fields.GenericForeignKey('content_type', 'object_id')
    status = models.BooleanField(default=False)  # 是否阅读
    type = models.IntegerField()  # 通知类型 0:评论帖子 1:关注信息 2:图书交换请求 3:流浪动物评论 4:帖子点赞
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notice'
        ordering = ['-created_at']
        verbose_name_plural = 'notice'

    def __str__(self):
        return "%s的事件: %s" % (self.sender, self.description())

    def description(self):
        print(self.event)
        if self.event:
            return self.event.description()
        return "No Event"

    def reading(self):
        if not self.status:
            self.status = True


# 聊天记录
class Messages(models.Model):
    # 信息发送者
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_sender')
    # 信息接收者
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='message_receiver')
    # 信息内容
    body = models.CharField(max_length=1024, verbose_name='message_body')
    # 发送时间
    created = models.DateTimeField(auto_now_add=True)
    # 状态
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-created',)


# @receiver(post_save, sender=Messages)
# def post_application_notice(sender, instance=None, created=False, **kwargs):
#     entity = instance
#     if created:
#         push(entity.sender.username, {'type': 5, 'text': entity.id})
#         push(entity.receiver.username, {'type': 5, 'text': entity.id})
