from django.db import models
from django.conf import settings
from django.db.models import signals
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


# Create your models here.
# 消息通知
class Notice(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notice_sender')  # 发送者
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notice_receiver')  # 接收者
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    event = fields.GenericForeignKey('content_type', 'object_id')
    status = models.BooleanField(default=False)  # 是否阅读
    type = models.IntegerField()  # 通知类型 0:评论 1:好友或系统消息 2:好友申请
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notice'
        ordering = ['-created_at']
        verbose_name_plural = 'notice'

    def __str__(self):
        return "%s的事件: %s" % (self.sender, self.description())

    def description(self):
        if self.event:
            return self.event.description()
        return "No Event"

    def reading(self):
        if not self.status:
            self.status = True