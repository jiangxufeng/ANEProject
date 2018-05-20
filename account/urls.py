# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-4-27

from django.conf.urls import url
from .views import (
    UserResetPasswordView,
    UserChangeInfoView,
    UserDetailView,
    UserLoginView,
    UserBindPhoneView,
    MakeFriendView,
    GetFollowView,
    GetFansView,
)


urlpatterns = [
    url(r'^login/$', UserLoginView.as_view(), name='user_login'),
    url(r'^detail/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^(?P<pk>\d+)/changeInfo/$', UserChangeInfoView.as_view(), name='change_info'),
    url(r'^(?P<pk>\d+)/resetPassword/$', UserResetPasswordView.as_view(), name='reset_password'),
    url(r'^(?P<pk>\d+)/phone/$', UserBindPhoneView.as_view(), name='bind_phone'),
    url(r'^(?P<fans>\d+)/follows/(?P<idol>\d+)/$', MakeFriendView.as_view(), name='make_friend'),
    url(r'^getFollow/(?P<user_id>\d+)/$', GetFollowView.as_view(), name='get_follow'),
    url(r'^getFans/(?P<user_id>\d+)/$', GetFansView.as_view(), name='get_fans'),
]