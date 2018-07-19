# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-16

from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rewrite.pagination import Pagination
from rewrite.permissions import get_authentication
from .serializers import NoticeListSerializer
from .models import Notice
from django.http import Http404
from rewrite.exception import FoundNoticeFailed
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST


# 获取当前用户的所有通知
class UserNoticeListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = NoticeListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = get_authentication(sign=self.request.META.get('HTTP_SIGN'), pk=self.kwargs['pk'])
        queryset = Notice.objects.filter(receiver=user, status=False)
        return queryset.order_by('-created_at')


# 获取当前用户的帖子被点赞通知
class PostLikeNoticeListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = NoticeListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = get_authentication(sign=self.request.META.get('HTTP_SIGN'), pk=self.kwargs['pk'])
        queryset = Notice.objects.filter(receiver=user, type=4, status=False)
        return queryset.order_by('-created_at')


# 获取当前用户的帖子被评论通知
class PostCommentNoticeListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = NoticeListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = get_authentication(sign=self.request.META.get('HTTP_SIGN'), pk=self.kwargs['pk'])
        queryset = Notice.objects.filter(receiver=user, type=0, status=False)
        return queryset.order_by('-created_at')


# 通知标记为已读
class HasReadTheNoticeView(APIView):
    permission_classes = (AllowAny,)

    def get_notice(self, nid):
        try:
            Notice.objects.filter(id=nid).update(status=True)
            return True
        except Notice.DoesNotExist:
            raise FoundNoticeFailed

    def get(self, request, nid, pk):
        get_authentication(sign=request.META.get('HTTP_SIGN'), pk=pk)
        notice = self.get_notice(nid=nid)
        if notice:
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "error": 50002,
                "error_msg": "Failed to change the status of the notice"
            }, HTTP_400_BAD_REQUEST)
