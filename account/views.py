# -*- coding:utf-8 -*-
# author: JXF
# date: 2018-1-24

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_204_NO_CONTENT,
)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from rest_framework.response import Response
from .serializers import (
    UserPasswordResetSerializer,
    UserDetailSerializer,
    UserLoginSerializer,
    UserBindPhoneSerializer,
    FansSerializer,
    FollowSerializer,
)
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rewrite.authentication import ExpiringTokenAuthentication
from .UserLogin import Userlogin
from .models import LoginUser, Follow#, Fans
from django.contrib.auth import authenticate
from rewrite.authentication import expire_token
from rewrite.permissions import IsOwner
from rest_framework import mixins
from rest_framework import generics
from rewrite.pagination import Pagination
from django.conf import settings

#EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


# 用户登录
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
       # print(request.META.get("HTTP_ACCEPT"))
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            in_database = LoginUser.objects.filter(username=username)
            if in_database:
                user = authenticate(username=username, password=password)
                if user:
                    content = expire_token(user)
                    user.save()
                    return Response(content, HTTP_200_OK)
                else:
                    content = {
                        'error': "1",
                        'data': '',
                        'err_msg': 'Incorrect username or password',
                    }
                    return Response(content, HTTP_200_OK)
            else:
                result = Userlogin(username, password)
                if result:
                    user = LoginUser.objects.create_user(username=username, password=password,
                                                         real_name=result, school_id=username)
                    user.save()
                    content = expire_token(user)
                    return Response(content, HTTP_201_CREATED)
                else:
                    content = {
                        'error': "1",
                        'data': '',
                        'err_msg': 'Incorrect username or password',
                    }
                    return Response(content, HTTP_200_OK)


# 获取用户信息
class UserDetailView(mixins.RetrieveModelMixin,
                     generics.GenericAPIView):

    # 该权限为当前登录用户只能获取自己信息
    # permission_classes = (IsAuthenticated, IsOwner)
    #permission_classes = (IsAuthenticated,)
    #authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (AllowAny, )
    queryset = LoginUser.objects.all()
    serializer_class = UserDetailSerializer

    def get(self, request, *args, **kwargs):
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response({
                'error': '0',
                'data': cont.data,
            }, HTTP_200_OK)
        except Http404:    # 获取失败，没有找到对应数据
            msg = Response({
                'error': '1',
                'error_msg': 'Not found the user',
                'data': ''
            }, HTTP_404_NOT_FOUND)
        return msg


# 用户更改资料
class UserChangeInfoView(mixins.UpdateModelMixin,
                         generics.GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = LoginUser.objects.all()
    serializer_class = UserDetailSerializer

    def put(self, request, *args, **kwargs):
        try:
            self.update(request, *args, **kwargs)
            msg = Response({
                'error': '0',
                'data': '',
                'message': 'Success to update the information',
            }, HTTP_200_OK)
        except Http404:
            msg = {
                'error': '1',
                'data': '',
                'error_msg': 'Not found the user'
            }
            return Response(msg, HTTP_404_NOT_FOUND)
        except:
            msg = Response({
                'error': '1',
                'data': '',
                'error_msg': 'Failed to update the information',
            }, HTTP_400_BAD_REQUEST)
        return msg


# 修改密码
class UserResetPasswordView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = (IsAuthenticated, IsOwner)
    serializer_class = UserPasswordResetSerializer
    # authentication_classes = (ExpiringTokenAuthentication)

    def put(self, request, pk):
        serializer = UserPasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_password = serializer.validated_data['password']
            try:
                user = LoginUser.objects.get(pk=pk)
                user.set_password(new_password)
                user.save()
                msg = {
                    'error': '0',
                    'data': '',
                    'message': 'Success to change password'
                }
            except Http404:
                msg = {
                    'error': '1',
                    'data': '',
                    'error_msg': 'Not found the user'
                }
                return Response(msg, HTTP_404_NOT_FOUND)
            except:
                msg = {
                    'error': '1',
                    'data': '',
                    'error_msg': 'Failed to change password'
                }
            return Response(msg, HTTP_200_OK)
        msg = {
            'error': '1',
            'data': '',
            'error_msg': 'The data is invalid'
        }
        return Response(msg, HTTP_400_BAD_REQUEST)


# 绑定手机与解绑
class UserBindPhoneView(APIView):
    # permission_classes = (IsOwner, IsAuthenticated)
    permission_classes = (AllowAny,)
    serializer_class = UserBindPhoneSerializer
    # authentication_classes = (ExpiringTokenAuthentication)

    def put(self, request, pk):
        serializer = UserBindPhoneSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data['phone']
            try:
                user = LoginUser.objects.get(pk=pk)
                user.phone = phone
                user.save()
                print(user.phone)
                msg = Response(HTTP_204_NO_CONTENT)
            except Http404:
                msg = Response({
                    'error': '1',
                    'data': '',
                    'error_msg': 'Not found the user'
                }, HTTP_404_NOT_FOUND)
            except:
                msg = Response({
                    'error': '1',
                    'data': '',
                    'error_msg': 'Failed to change password'
                }, HTTP_400_BAD_REQUEST)
            return msg

    def delete(self, request, pk):
        try:
            user = LoginUser.objects.get(pk=pk)
            user.phone = ''
            user.save()
            msg = Response({
                'error': '0',
                'data': '',
                'message': 'unbind phone successfully'
            }, HTTP_200_OK)
        except Http404:
            msg = Response({
                'error': '1',
                'data': '',
                'error_msg': 'Not found the user'
            }, HTTP_404_NOT_FOUND)
        return msg


# 关注和取消关注
class MakeFriendView(APIView):
    #permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
    #authentication_classes = (ExpiringTokenAuthentication)

    def is_same(self, idol, fans):
        return idol == fans

    def get(self, request, idol, fans):
        if self.is_same(idol, fans):
            msg = Response({
                'error': '1',
                'data': '',
                'error_msg': "You can't follow yourself.It's invalid"
            }, HTTP_404_NOT_FOUND)
        else:
            try:
                idols = LoginUser.objects.get(pk=idol)
                fan = LoginUser.objects.get(pk=fans)
            except LoginUser.DoesNotExist:
                msg = Response({
                    'error': '1',
                    'data': '',
                    'error_msg': 'Not found the user'
                }, HTTP_404_NOT_FOUND)
                return msg
            follow = Follow.objects.create(follows=idols, fans=fan)
            follow.save()
            msg = Response({
                'error': '0',
                'data': '',
                'message': 'Pay attention to the user successfully'
            }, HTTP_200_OK)
        return msg

    def delete(self, request, idol, fans):
        try:
            idol = LoginUser.objects.get(pk=idol)
            fans = LoginUser.objects.get(pk=fans)
            follow = Follow.objects.get(fans=fans, follows=idol)
        except LoginUser.DoesNotExist:
            msg = Response({
                'error': '1',
                'data': '',
                'error_msg': 'Not found the user'
            }, HTTP_404_NOT_FOUND)
            return msg
        follow.delete()
        msg = Response({
            'error': '0',
            'data': '',
            'message': 'Unfollow the user successfully'
        }, HTTP_200_OK)
        return msg


# 获取关注的人

class GetFollowView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FollowSerializer
    pagination_class = Pagination

    def get_user(self, user_id):
        try:
            return LoginUser.objects.get(id=user_id)
        except LoginUser.DoesNotExist:
            raise Http404

    def get_queryset(self):
        owner = self.get_user(user_id=self.kwargs['user_id'])
        queryset = Follow.objects.filter(fans=owner)
        return queryset


# 获取粉丝列表
class GetFansView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (ExpiringTokenAuthentication)
    serializer_class = FansSerializer
    pagination_class = Pagination

    def get_user(self, user_id):
        try:
            return LoginUser.objects.get(id=user_id)
        except LoginUser.DoesNotExist:
            raise Http404

    def get_queryset(self):
        owner = self.get_user(user_id=self.kwargs['user_id'])
        queryset = Follow.objects.filter(follows=owner)
        return queryset









