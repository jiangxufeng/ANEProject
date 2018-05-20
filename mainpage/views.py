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
    ShopPublishSerializer,
    FoodCommentPublishSerializer,
    FoodCommentDetailSerializer,
    ShopDetailSerializer,
)
from .models import Book, Food, FoodComment
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rewrite.authentication import ExpiringTokenAuthentication
from django.http import Http404
from rest_framework import mixins, generics
from account.models import LoginUser
from .get_score import get_level
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rewrite.pagination import Pagination


# 某一本图书详情
class BookDetailView(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = BookDetailSerializer
    queryset = Book.objects.all()

    def get(self, request, *args, **kwargs):
        header = {}
        header['Connection'] = 'keep-alive'
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response(data={
                'error': '0',
                'data': cont.data,
            }, status=HTTP_200_OK)
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


# 获取全部图书并展示
class GetAllBookView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = BookDetailSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 筛选图书，筛选条件：交换状态、地点、作者国家、语言、类型
    filter_fields = ('status', 'place', 'country', 'language', 'types')
    ordering_fields = ('level', 'place')
    search_fields = ('name',)

    def get_queryset(self):
        queryset = Book.objects.all()
        return queryset.order_by('create_at')


# 发布商家信息
class ShopPublishView(APIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication,)
    serializer_class = ShopPublishSerializer

    def post(self, request):
        serializer = ShopPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            location = serializer.validated_data['location']
            introduce = serializer.validated_data['introduce']
            image = serializer.validated_data['image']
            food = Food.objects.create(name=name, location=location, introduce=introduce, image=image)
            food.save()
            msg = Response({
                'error': '0',
                'data': '',
                'message': 'Success to publish the shop information'
            }, HTTP_201_CREATED)
            return msg


# 获取某个商家信息
class ShopDetailView(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = ShopDetailSerializer
    queryset = Food.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response(data={
                'error': '0',
                'data': cont.data,
            }, status=HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            msg = Response({
                'error': '1',
                'error_msg': 'Not found the shop',
                'data': ''
            }, HTTP_404_NOT_FOUND)
        return msg


# 获取所有商家信息
class GetAllShopView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = ShopDetailSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 筛选图书，筛选条件：交换状态、地点、作者国家、语言、类型
    filter_fields = ('location', )
    ordering_fields = ('rating',)
    search_fields = ('name',)

    def get_queryset(self):
        queryset = Food.objects.all()
        return queryset.order_by('created_at')


# 发布对商家的评论
class FoodCommentPublishView(APIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication,)
    serializer_class = FoodCommentPublishSerializer

    def get_user(self, user_id):
        try:
            return LoginUser.objects.get(id=user_id)
        except LoginUser.DoesNotExist:
            raise Http404

    def get_shop(self, shop_id):
        try:
            return Food.objects.get(id=shop_id)
        except Food.DoesNotExist:
            raise Http404

    def post(self, request, user_id, shop_id):
        serializer = FoodCommentPublishSerializer(data=request.data)
        owner = self.get_user(user_id)
        shop = self.get_shop(shop_id)
        if serializer.is_valid(raise_exception=True):
            content = serializer.validated_data['content']
            score = serializer.validated_data['score']
            comment = FoodComment.objects.create(owner=owner, food=shop, content=content, score=score)
            comment.save()
            shop.number += 1
            shop.rating = float((shop.rating * (shop.number-1) + float(score)) / shop.number)
            shop.save()
            msg = Response({
                'error': '0',
                'data': '',
                'message': 'Success to comment'
            }, HTTP_201_CREATED)
            return msg


# 具体某一条评论详情
class FoodCommentDetailView(mixins.RetrieveModelMixin,
                            generics.GenericAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = FoodCommentDetailSerializer
    queryset = FoodComment.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response(data={
                'error': '0',
                'data': cont.data,
            }, status=HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            msg = Response({
                'error': '1',
                'error_msg': 'Not found the comment',
                'data': ''
            }, HTTP_404_NOT_FOUND)
        return msg


# 获取对某个商家的全部评价
class GetShopCommentView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = FoodCommentDetailSerializer
    pagination_class = Pagination

    def get_shop(self, pk):
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            raise Http404

    def get_queryset(self):
        shop = self.get_shop(pk=self.kwargs['shop_id'])
        print(shop)
        queryset = FoodComment.objects.filter(food=shop)
        return queryset.order_by('created_at')



