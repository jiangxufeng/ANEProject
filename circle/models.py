# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-08

from django.shortcuts import reverse
from django.db import models
from django.conf import settings
from django.db.models import signals
from notice.models import Notice
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


from django.shortcuts import reverse
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


def get_pyImage_upload_to():
    pass


# 帖子
class PyPost(models.Model):
    # 发帖人
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    # 帖子标题
    title = models.CharField(max_length=36, verbose_name="postTitle")
    # 帖子内容
    content = models.TextField(verbose_name="postContent", default="", max_length=144)
    # 发帖时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 图片
    images = models.CharField(max_length=1024, null=True, verbose_name='images')

    def __str__(self):
        return self.title

    #  @models.permalink
    def get_absolute_url(self):
        return reverse(viewname='post:post_detail', kwargs={'pk': self.pk})


# 评论
class PostComment(models.Model):
    # 评论者
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="postComments")
    # 评论的帖子
    passage = models.ForeignKey(PyPost, related_name="comments")
    # 评论时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 评论内容
    content = models.TextField(max_length=144, verbose_name='contents')

    def __str__(self):
        return self.passage.title

    def description(self):
        return {'passage': self.passage.title, 'passageUrl': self.passage.get_absolute_url(), 'content': self.content, 'created': self.created_at}


# 二级评论
class PostCommentReply(models.Model):
    # 回复的评论
    commentParent = models.ForeignKey(PostComment, related_name="replies")
    # 回复者
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commentReply')
    # 回复的对象
    toWho = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='replyTome')
    # 回复的内容
    content = models.CharField(max_length=144, verbose_name="content")
    # 回复的时间
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.owner.nickname


# 点赞
class PostLike(models.Model):
    # 点赞者
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="postLikes")
    # 点赞的帖子
    passage = models.ForeignKey(PyPost, related_name="likes")

    def __str__(self):
        return self.passage.title

    @models.permalink
    def get_absolute_url(self):
        return ('post:post_detail', (), {'pk': self.passage.pk})

    def description(self):
        return {'passage': self.passage.title, 'postUrl': self.get_absolute_url()}


# def comment_save(sender, instance, signal, *args, **kwargs):
#     entity = instance
#     print(kwargs)
#     if str(entity.created_at)[:19] == str(entity.updated_at)[:19]:
#         if entity.owner != entity.passage.owner:                       # 作者的回复不给作者通知
#             event = Notice(sender=entity.owner, receiver=entity.passage.owner, event=entity, type=0)
#             event.save()
#         if entity.comment_parent is not None:		              # 回复评论给要评论的人通知
#             if entity.author.id != entity.comment_parent.author.id:   # 自己给自己写评论不通知
#                 event = Notice(sender=entity.author, receiver=entity.comment_parent.author, event=entity, type=0)
#                 event.save()
#
#
# def like_save(sender, instance, signal, *args, **kwargs):
#     entity = instance
#     print(kwargs)
#     if str(entity.created_at)[:19] == str(entity.updated_at)[:19]:
#         if entity.owner != entity.passage.owner:                       # 作者的回复不给作者通知
#             event = Notice(sender=entity.owner, receiver=entity.passage.owner, event=entity, type=4)
#            event.save()
#
#
# signals.post_save.connect(comment_save, sender=PostComment)
#signals.post_save.connect(comment_save, sender=PostLike)


@receiver(post_save, sender=PostLike)
def post_like_notice(sender, instance=None, created=False, **kwargs):
    entity = instance
    if created:
        event = Notice(sender=entity.owner, receiver=entity.passage.owner, event=entity, type=4)
        event.save()
        # 消息推送
        # 推送对象为消息接受者，推送内容为消息类型
        push(entity.passage.owner.username, {'type': 4})


@receiver(post_save, sender=PostComment)
def post_comment_notice(sender, instance=None, created=False, **kwargs):
    entity = instance
    if created:
        event = Notice(sender=entity.owner, receiver=entity.passage.owner, event=entity, type=0)
        event.save()
        push(entity.passage.owner.username, {'type': 0})
