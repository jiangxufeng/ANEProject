# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-16


from django.conf.urls import url
from .views import (
    UserNoticeListView,
    PostLikeNoticeListView,
    PostCommentNoticeListView,
    HasReadTheNoticeView,
)


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', UserNoticeListView.as_view(), name='user_all_notice'),
    url(r'^(?P<pk>\d+)/likes/$', PostLikeNoticeListView.as_view(), name='user_like_notice'),
    url(r'^(?P<pk>\d+)/postComments/$', PostCommentNoticeListView.as_view(), name='user_comment_notice'),
    url(r'^(?P<pk>\d+)/hasRead/(?P<nid>\d+)/$', HasReadTheNoticeView.as_view(), name='change_status'),
]