# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-16

from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rewrite.pagination import Pagination
# from rewrite.permissions import get_authentication
from rewrite.authentication import MyAuthentication
from .serializers import NoticeListSerializer, MessageDetailSerializer, MessagePublishSerializer
from .models import Notice, Messages
# from django.http import Http404
from rewrite.exception import FoundNoticeFailed, FoundUserFailed
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
# from rest_framework import filters
from account.models import LoginUser
from django.conf import settings


# 获取当前用户的所有通知
class UserNoticeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = NoticeListSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    # 筛选图书，筛选条件：交换状态、地点、作者国家、语言、类型
    filter_fields = ('type', 'status')

    def get_queryset(self):
        user = self.request.user
        queryset = Notice.objects.filter(receiver=user)
        return queryset.order_by('-created_at')


# 通知标记为已读
class HasReadTheNoticeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)

    def get_notice(self, nid):
        try:
            Notice.objects.filter(id=nid).update(status=True)
            return True
        except Notice.DoesNotExist:
            raise FoundNoticeFailed

    def get(self, request, nid):
        notice = self.get_notice(nid=nid)
        if notice:
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response({
                "error": 50002,
                "error_msg": "Failed to change the status of the notice"
            }, HTTP_400_BAD_REQUEST)


# 获取某一条消息
class MessageDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = MessageDetailSerializer

    def get(self, request, pk):
        message = Messages.objects.filter(Q(receiver=request.user) | Q(sender=request.user))
        try:
            message = message.get(id=pk)
            # print(MessageDetailSerializer(message))
        except Messages.DoesNotExist:
            raise NotFound('60001Not found the message.')
        else:
            msg = Response({
                'error': '0',
                'data': MessageDetailSerializer(message).data,
            }, HTTP_200_OK)
            return msg


# 获取消息列表
class MessageListView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = MessageDetailSerializer

    def get(self, request):
        target = request.GET.get('target')
        try:
            LoginUser.objects.get(nickname=target)
        except LoginUser.DoesNotExist:
            raise FoundUserFailed
        else:

            messages = Messages.objects.filter(Q(receiver=request.user) | Q(sender=request.user))

            message = messages.filter(Q(sender__nickname=target) | Q(receiver__nickname=target))

            msg = Response({
                'error': '0',
                'data': MessageDetailSerializer(message, many=True).data
            })
            return msg


# 发送消息
class MessagePublishView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication, )
    serializer_class = MessagePublishSerializer

    def post(self, request):
        user = request.user
        serializer = MessagePublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                receiver = LoginUser.objects.get(nickname=serializer.validated_data['receiver'])
            except LoginUser.DoesNotExist:
                raise FoundUserFailed
            body = serializer.validated_data['body']

            message = Messages.objects.create(sender=user, receiver=receiver, body=body)
            message.save()
            msg = Response({
                'error': '0',
                'data': MessageDetailSerializer(message).data
            }, HTTP_200_OK)
            return msg
