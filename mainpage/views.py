# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-4-27

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
    BookListSerializer,
    ShopPublishSerializer,
    FoodCommentPublishSerializer,
    FoodCommentDetailSerializer,
    ShopDetailSerializer,
    ShopListSerializer,
    UploadImageSerializer,
    AnimalMsgPublishSerializer,
    AnimalMsgDetailSerializer,
    AnimalMsgListSerializer,
)
from .models import Book, Food, FoodComment, AnimalSaveMsg, Images, Animals
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
from rewrite.permissions import IsOwner
from rest_framework.authtoken.models import Token
from rewrite.permissions import get_authentication
from rest_framework.exceptions import APIException
from rewrite.exception import (
    FoundBookFailed,
    FoundCommentFailed,
    FoundShopFailed,
    FoundAnimalFailed,
    ParamsInvalid,
)


# 发布图书信息
class BookPublishView(APIView):
    # permission_classes = (IsAuthenticated, IsOwner)
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication,)
    serializer_class = BookPublishSerializer

    def post(self, request, pk):
        user = get_authentication(sign=request.META.get("HTTP_SIGN"), pk=pk)
        serializer = BookPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            country = serializer.validated_data['country']
            language = serializer.validated_data['language']
            types = serializer.validated_data['types']
            image = serializer.validated_data['image']
            place = serializer.validated_data['place']
            level = get_level(name)
            book = Book.objects.create(owner=user, name=name, country=country, language=language, types=types,
                                       image=image, place=place, level=level)
            book.save()
            msg = Response({
                'error': 0,
                'data': BookDetailSerializer(book, context={'request': request}).data,
                'message': 'Success to publish the book',
            }, HTTP_201_CREATED)
            return msg


# 获取全部图书并展示
class BookListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = BookListSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 筛选图书，筛选条件：交换状态、地点、作者国家、语言、类型
    filter_fields = ('status', 'place', 'country', 'language', 'types')
    ordering_fields = ('level', 'place')
    search_fields = ('name',)

    def get_queryset(self):
        queryset = Book.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.order_by('-created_at')


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
            msg = Response(data={
                'error': 0,
                'data': cont.data,
            }, status=HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            raise FoundBookFailed
        else:
            return msg


# 获取当前用户在平台上发布交换的图书
class UserBookListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = BookDetailSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = get_authentication(sign=self.request.META.get('HTTP_SIGN'), pk=self.kwargs['user_id'])
        queryset = Book.objects.filter(owner=user)
        return queryset.order_by('-create_at')


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
                'error': 0,
                'data': ShopDetailSerializer(food, context={'request': request}).data,
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
           raise FoundShopFailed
        return msg


# 获取所有商家信息
class GetAllShopView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = ShopListSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 筛选商家：信息学部、文理学部......
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

    def get_shop(self, shop_id):
        try:
            return Food.objects.get(id=shop_id)
        except Food.DoesNotExist:
            raise FoundShopFailed

    def post(self, request, pk, shop_id):
        serializer = FoodCommentPublishSerializer(data=request.data)
        owner = get_authentication(sign=request.META.get("HTTP_SIGN"), pk=pk)
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
                'error': 0,
                'data': FoodCommentDetailSerializer(comment, context={"request": request}).data,
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
                'error': 0,
                'data': cont.data,
            }, status=HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            raise FoundCommentFailed
        else:
            return msg


# 获取对某个商家的全部评价，或者发布对某商家的评价
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
        queryset = FoodComment.objects.filter(food=shop)
        queryset = FoodCommentDetailSerializer.setup_eager_loading(queryset)
        return queryset.order_by('-created_at')


# 上传图片(多张，每次一张，多次上传）
class UploadImagesView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UploadImageSerializer

    def get_model(self, bid, sid, aid):
        if bid != '0':
            try:
                return Book.objects.get(id=bid), None, None
            except Book.DoesNotExist:
                raise FoundBookFailed
        elif sid != '0':
            try:
                return None, Food.objects.get(id=sid), None
            except Food.DoesNotExist:
                raise FoundShopFailed
        elif aid != '0':
            try:
                return None, None, Animals.objects.get(id=aid)
            except Animals.DoesNotExist:
                raise FoundAnimalFailed
        else:
            raise ParamsInvalid

    def post(self, request, bid, sid, aid):
        serializer = UploadImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            book, shop, animal = self.get_model(bid, sid, aid)
            image = serializer.validated_data['image']
            img = Images.objects.create(bookOwner=book, shopOwner=shop, animalOwner=animal, image=image)
            img.save()
            msg = Response({
                'error': 0,
                'data': {"bookOwner": bid, "shopOwner": sid, "animalOwner": aid, "image": img.get_img_url()},
                'message': 'Success to upload the image.'
            }, HTTP_201_CREATED)
            return msg


# 发布流浪猫狗信息
class AnimalsMsgPublishView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnimalMsgPublishSerializer

    def post(self, request, pk):
        author = get_authentication(sign=request.META.get('HTTP_SIGN'), pk=pk)
        serializer = AnimalMsgPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data['title']
            content = serializer.validated_data['content']
            location = serializer.validated_data['location']
            animalMsg = Animals.objects.create(location=location, title=title, author=author, content=content)
            animalMsg.save()
            msg = Response({
                'error': 0,
                'data': AnimalMsgDetailSerializer(animalMsg, context={'request': request}).data,
                'message': 'Success to publish the message.'
            }, HTTP_201_CREATED)
            return msg


# 流浪猫狗具体详情
class AnimalsMsgDetailView(mixins.RetrieveModelMixin,
                           generics.GenericAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = AnimalMsgDetailSerializer
    queryset = Animals.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response(data={
                'error': 0,
                'data': cont.data,
            }, status=HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            raise FoundAnimalFailed
        else:
            return msg


# 获取所有的流浪猫狗信息
class AnimalsMsgListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = AnimalMsgListSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 筛选商家：信息学部、文理学部......
    filter_fields = ('location', )
    search_fields = ('title',)

    def get_queryset(self):
        queryset = Animals.objects.all()
        return queryset.order_by('-created_at')
