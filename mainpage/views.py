# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-4-27

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)
from .serializers import (
    BookDetailSerializer,
    BookPublishSerializer,
)
from .models import Book
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rewrite.authentication import ExpiringTokenAuthentication
from django.http import Http404
from rest_framework import mixins, generics
from account.models import LoginUser
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from .get_score import get_level


# 分页处理
class Pagination(PageNumberPagination):
    # 默认每页显示数据条数
    page_size = 8
    # 获取url参数中设置的每页显示数据条数
    page_size_query_param = 'size'
    # 获取url中传入的页码
    page_query_param = 'page'
    # 每页最大显示数量
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
            ('error', '0')
        ]))


# 某一本图书详情
class BookDetailView(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = BookDetailSerializer
    queryset = Book.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response({
                'error': '0',
                'data': cont.data,
            }, HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            msg = Response({
                'error': '1',
                'error_msg': 'Not found the book',
                'data': ''
            }, HTTP_404_NOT_FOUND)
        return msg


# 获取当前用户在平台上发布交换的图书
class UserBookListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = BookDetailSerializer
    pagination_class = Pagination

    def get_object(self, user_id):
        try:
            return LoginUser.objects.get(id=user_id)
        except LoginUser.DoesNotExist:
            raise Http404

    def get_queryset(self):
        user = self.get_object(user_id=self.kwargs['user_id'])
        queryset = Book.objects.filter(owner=user)
        return queryset.order_by('-create_at')


# 发布图书信息
class BookPublishView(APIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = BookPublishSerializer

    def get_user(self, user_id):
        try:
            return LoginUser.objects.get(id=user_id)
        except LoginUser.DoesNotExist:
            raise Http404

    def post(self, request, user_id):
        serializer = BookPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            country = serializer.validated_data['country']
            language = serializer.validated_data['language']
            types = serializer.validated_data['types']
            image = serializer.validated_data['image']
            place = serializer.validated_data['place']
            level = get_level(name)
            owner = self.get_user(user_id=user_id)
            book = Book.objects.create(owner=owner, name=name, country=country, language=language, types=types,
                                       image=image, place=place, level=level)
            book.save()
            msg = Response({
                'error': '0',
                'data': '',
                'message': 'Success to publish the book',
            }, HTTP_201_CREATED)
            return msg

