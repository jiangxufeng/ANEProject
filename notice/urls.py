# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-16


from django.conf.urls import url
from .views import (
    UserNoticeListView,
    HasReadTheNoticeView,
    MessageDetailView,
    MessageListView,
    MessagePublishView,
)


urlpatterns = [
    url(r'^notices/$', UserNoticeListView.as_view(), name='user_all_notice'),
    url(r'^notices/hasRead/(?P<nid>\d+)/$', HasReadTheNoticeView.as_view(), name='change_status'),
    url(r'^message/(?P<pk>\d+)/$', MessageDetailView.as_view(), name='message_detail'),
    url(r'^message/$', MessageListView.as_view(), name='message_list'),
    url(r'^message/publish', MessagePublishView.as_view(), name='message_publish')
]