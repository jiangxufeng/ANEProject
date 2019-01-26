# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-09

from django.conf.urls import url
from .views import (
    PyPostPublishView,
    PyPostListView,
    PyPostDetailView,
    PostCommentPublishView,
    PostLikePublishView,
    PostLikeDeleteView,
    PostCommentsListView,
    PyPostOfUserListView,
    CommentReplyPublishView,
    CommentReplyDeleteView,
    msg
)

app_name = "post"

urlpatterns = [
    url(r'^posts/$', PyPostListView.as_view(), name='posts'),
    url(r'^posts/publish/', PyPostPublishView.as_view(), name='post_publish'),
    url(r'^posts/(?P<pk>\d+)$', PyPostDetailView.as_view(), name='post_detail'),
    url(r'^posts/user/$', PyPostOfUserListView.as_view(), name='user_posts'),
    url(r'^posts/comments/$', PostCommentPublishView.as_view(), name='post_comment_publish'),
    url(r'^posts/comments/reply/$', CommentReplyPublishView.as_view(), name='post_comment_reply'),
    url(r'^posts/comments/reply/(?P<pk>\d+)$', CommentReplyDeleteView.as_view(), name='post_comment_reply_delete'),
    url(r'^posts/(?P<pid>\d+)/comments/$', PostCommentsListView.as_view(), name='post_comments'),
    url(r'^posts/likes/$', PostLikePublishView.as_view(), name='post_like_publish'),
    url(r'^posts/likes/(?P<pk>\d+)$', PostLikeDeleteView.as_view(), name='post_like_delete'),
    url(r'^msg/(?P<username>[0-9a-zA-Z]+)$', msg, name='msg')
]