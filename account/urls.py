# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-4-27

from django.conf.urls import url
from .views import (
    UserResetPasswordView,
    UserChangeInfoView,
    UserSelfDetailView,
    UserPublicDetailView,
    UserLoginView,
    UserBindPhoneView,
    MakeFriendView,
    GetFollowView,
    GetFansView,
    UserListView,
)


urlpatterns = [
    url(r'^login/$', UserLoginView.as_view(), name='user_login'),
    url(r'^$', UserSelfDetailView.as_view(), name='user_self_detail'),
    url(r'^userlist$', UserListView.as_view(), name='user_list'),
    url(r'^(?P<pk>\d+)/$', UserPublicDetailView.as_view(), name='user_public_detail'),
    url(r'^changeInfo/$', UserChangeInfoView.as_view(), name='change_info'),
    url(r'^resetPassword/$', UserResetPasswordView.as_view(), name='reset_password'),
    url(r'^phone/$', UserBindPhoneView.as_view(), name='bind_phone'),
    url(r'^follow/(?P<idol>\d+)/$', MakeFriendView.as_view(), name='make_friend'),
    url(r'^(?P<pk>\d+)/followees$', GetFollowView.as_view(), name='get_follow'),
    url(r'^(?P<pk>\d+)/fans$', GetFansView.as_view(), name='get_fans'),
]


