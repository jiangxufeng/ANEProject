# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-5-2

from django.conf.urls import url
from .views import (
    BookDetailView,
    UserBookListView,
    BookPublishView,
)


urlpatterns = [
    url(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book_detail'),
    url(r'^book/user/(?P<user_id>\d+)$', UserBookListView.as_view(), name='user_book'),
    url(r'^book/(?P<user_id>\d+)/publish/', BookPublishView.as_view(), name='book_publish'),
]
