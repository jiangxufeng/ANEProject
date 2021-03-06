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
    ApplicationPublishSerializer,
    ApplicationDetailSerializer,
    ApplicationHandleSerializer,
)
from .models import Book, Food, FoodComment, AnimalSaveMsg, Images, Animals, Application
from account.models import LoginUser
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rewrite.authentication import MyAuthentication
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework.exceptions import NotFound, ValidationError
from .get_score import get_level
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rewrite.pagination import Pagination
from rewrite.permissions import IsReceiver, IsSender
# from rest_framework.authtoken.models import Token
# from rewrite.permissions import get_authentication
# from rest_framework.exceptions import APIException
from rewrite.exception import (
    FoundBookFailed,
    FoundCommentFailed,
    FoundShopFailed,
    FoundAnimalFailed,
    ParamsInvalid,
    FoundUserFailed,
    ExchangeIsYourself
)
from django.db.models import Q
import requests
import xmltodict
import json
# from rewrite.permissions import IsOwnerFilterBackend


# 发布图书信息
class BookPublishView(APIView):
    """
        已认证用户可以发布新的图书交换信息
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = BookPublishSerializer

    def post(self, request):
        user = request.user
        serializer = BookPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            country = serializer.validated_data['country']
            language = serializer.validated_data['language']
            types = serializer.validated_data['types']
            images = serializer.validated_data['images']
            place = serializer.validated_data['place']
            level = get_level(name)
            book = Book.objects.create(owner=user, name=name, country=country, language=language, types=types,
                                       images=images, place=place, level=level)
            book.save()
            msg = Response({
                'error': 0,
                'data': BookDetailSerializer(book, context={'request': request}).data,
                'message': 'Success to publish the book',
            }, HTTP_201_CREATED)
            return msg


# 获取全部图书并展示
class BookListView(generics.ListAPIView):
    """
        所有用户可以获取到全部交换的图书
    """
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
    """
        所有用户可以获取到图书详情
    """
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


# 获取用户在平台上发布交换的图书
class UserBookListView(generics.ListAPIView):
    """
       任意用户都可获取
    """
    permission_classes = (AllowAny,)
    # authentication_classes = (MyAuthentication,)
    serializer_class = BookDetailSerializer
    pagination_class = Pagination

    def get_queryset(self):
        try:
            user = LoginUser.objects.get(id=self.kwargs['pk'])
        except LoginUser.DoesNotExist:
            raise FoundUserFailed
        else:
            queryset = Book.objects.filter(owner=user)
            return queryset.order_by('-created_at')


# 发布商家信息
class ShopPublishView(APIView):
    """
        只有已认证用户可以发布新的商家信息
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = ShopPublishSerializer

    def post(self, request):
        serializer = ShopPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            location = serializer.validated_data['location']
            introduce = serializer.validated_data['introduce']
            images = serializer.validated_data['images']
            food = Food.objects.create(name=name, location=location, introduce=introduce, images=images)
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
    """
        所有用户可以获取到具体的某个商家信息
    """
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
    """
        所有用户可以获取到商家信息
    """
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
    """
        已认证用户可以发布对商家的评价
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = FoodCommentPublishSerializer

    def get_shop(self, shop_id):
        try:
            return Food.objects.get(id=shop_id)
        except Food.DoesNotExist:
            raise FoundShopFailed

    def post(self, request, shop_id):
        serializer = FoodCommentPublishSerializer(data=request.data)
        owner = request.user
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


# 获取对某个商家的全部评价
class GetShopCommentView(generics.ListAPIView):
    """
        所有用户可以获取到对商家的评价信息
    """
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


# 上传图片
class UploadImagesView(APIView):
    """
        只有已认证用户可以上传图片
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = UploadImageSerializer

    def post(self, request):
        serializer = UploadImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            image = serializer.validated_data['image']
            img = Images.objects.create(image=image)
            img.save()
            msg = Response({
                'error': 0,
                'data': {"image": img.get_img_url()},
                'message': 'Success to upload the image.'
            }, HTTP_201_CREATED)
            return msg


# 发布流浪猫狗信息
class AnimalsMsgPublishView(APIView):
    """
        只有已认证用户可以发布流浪猫狗信息
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = AnimalMsgPublishSerializer

    def post(self, request):
        author = request.user
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
    """
        所有用户可以获取具体的流浪猫狗信息
    """
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
    """
        所有用户可以获取流浪猫狗信息
    """
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
        # 对部分信息进行预加载
        queryset = self.get_serializer_class().set_eager_loading(queryset)
        return queryset.order_by('-created_at')


# 提出交换申请
class ApplicationPublishView(APIView):
    """
        已认证用户可以提出图书交换的申请
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = ApplicationPublishSerializer

    def get_book(self, bid):
        try:
            return Book.objects.get(id=bid)
        except Book.DoesNotExist:
            raise FoundBookFailed

    def post(self, request):
        sender = request.user
        serializer = ApplicationPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            from_bid = serializer.validated_data['from_bid']
            to_bid = serializer.validated_data['to_bid']

            if from_bid == to_bid:
                raise ExchangeIsYourself

            from_book = self.get_book(bid=from_bid)
            to_book = self.get_book(to_bid)
            receiver = to_book.owner
            application = Application.objects.create(sender=sender, receiver=receiver, frombook=from_book,
                                                     tobook=to_book)
            application.save()
            msg = Response({
                'error': 0,
                'data': {'sender': sender.nickname, 'receiver': to_book.owner.nickname,
                         'frombook': from_book.name, 'tobook': to_book.name},
                'message': 'Success to put forward an application for exchange.'
            }, HTTP_201_CREATED)
            return msg


# 获取收到的所有申请
class ApplicationReceiveView(generics.ListAPIView):
    """
        已认证的用户只能获取到申请接受者为自己的申请
    """
    permission_classes = (IsAuthenticated, IsReceiver)
    authentication_classes = (MyAuthentication,)
    serializer_class = ApplicationDetailSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)  # filters.SearchFilter,# filters.OrderingFilter)
    filter_fields = ('status', )
    #  search_fields = ('title',)

    def get_queryset(self):
        receiver = self.request.user
        queryset = Application.objects.filter(receiver=receiver)
        queryset = self.get_serializer_class().set_eager_loading(queryset)
        return queryset.order_by('status')


# 获取用户发出的所有申请
class ApplicationSendView(generics.ListAPIView):
    """
        已认证的用户只能获取到自己发出的请求
    """
    permission_classes = (IsAuthenticated, IsSender)
    authentication_classes = (MyAuthentication,)
    serializer_class = ApplicationDetailSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)  # filters.SearchFilter,# filters.OrderingFilter)
    filter_fields = ('status', )
    #  search_fields = ('title',)

    def get_queryset(self):
        sender = self.request.user
        queryset = Application.objects.filter(sender=sender)
        queryset = self.get_serializer_class().set_eager_loading(queryset)
        return queryset.order_by('status')


# 处理收到的申请
class ApplicationHandleView(APIView):
    """
        已认证用户只可以处理receiver为自己的申请
    """
    permission_classes = (IsAuthenticated, IsReceiver)
    authentication_classes = (MyAuthentication,)
    serializer_class = ApplicationHandleSerializer

    def post(self, request, apid):

        try:
            application = Application.objects.get(id=apid)
        except Application.DoesNotExist:
            raise NotFound("30007The Application does not exist.")
        else:
            serializer = ApplicationHandleSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                result = serializer.validated_data['result']
                application.status = result
                application.save()
                if result == 1:
                    book = application.tobook
                    book.status = True
                    book.save()
                # 将结果推送给申请发送者，后续添加
                msg = Response({
                    'error': 0,
                    'data': {'status': result},
                    'message': 'Success to handle the application.'
                }, HTTP_200_OK)
                return msg


# 天气接口
class Weather(APIView):
    """
        用户获取天气推荐接口
    """
    permission_classes = (AllowAny,)
    # authentication_classes = (MyAuthentication,)
    # serializer_class = ApplicationHandleSerializer

    def get(self, request):
        url = 'http://wthrcdn.etouch.cn/WeatherApi?city=%s' % request.GET.get('city')
        try:
            req = requests.get(url)
            if req.status_code == 200:
                conv = xmltodict.parse(req.text)
            else:
                return Response({
                    'error': '50001',
                    'error_msg': '获取天气失败,错误原因：API请求失败'
                }, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': '50001',
                'error_msg': '获取天气失败，错误原因：%s' % e
            }, status=HTTP_400_BAD_REQUEST)
        else:
            res = json.loads(json.dumps(conv))['resp']
            try:
                error = res['error']

                return Response({
                    'error': '50002',
                    'error_msg': error
                }, HTTP_400_BAD_REQUEST)
            except KeyError:
                return Response({
                    'error': '0',
                    'data': res,
                })

