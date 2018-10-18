# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-16


from django.conf.urls import url
from .views import (
    UserNoticeListView,
    HasReadTheNoticeView,
)


urlpatterns = [
    url(r'^$', UserNoticeListView.as_view(), name='user_all_notice'),
    url(r'^hasRead/(?P<nid>\d+)/$', HasReadTheNoticeView.as_view(), name='change_status'),
]