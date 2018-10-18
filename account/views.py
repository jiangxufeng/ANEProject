# -*- coding:utf-8 -*-
# author: jiangxf
# updated: 2018-07-02

from django.shortcuts import render
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
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from .serializers import (
    UserPasswordResetSerializer,
    UserSelfDetailSerializer,
    UserPublicDetailSerializer,
    UserLoginSerializer,
    UserBindPhoneSerializer,
    FansSerializer,
    FollowSerializer,
    UserUpdateInfoSerializer,
)
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rewrite.authentication import ExpiringTokenAuthentication
from .UserLogin import Userlogin
from .models import LoginUser, Follow#, Fans
from django.contrib.auth import authenticate
from rewrite.authentication import expire_token, MyAuthentication
# from rewrite.permissions import IsOwnerOrReadOnly
from rest_framework import mixins
from rest_framework import generics
from rewrite.pagination import Pagination
# from django.conf import settings
# from rest_framework.authtoken.models import Token
# from rewrite.permissions import get_authentication
from rewrite.exception import FoundUserFailed, WrongUsernameOrPwd, FollowAuthenticationFailed, PasswordIsSame

#EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


# 用户登录
class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    # authentication_classes = (ExpiringTokenAuthentication,)

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            #  username = request.GET.get('username', '')
            #  password = request.GET.get('password', '')
            in_database = LoginUser.objects.filter(username=username)
            if in_database:
                user = authenticate(username=username, password=password)
                if user:
                    content = expire_token(user)
                    user.save()
                    return Response(content, HTTP_200_OK)
                else:
                    raise WrongUsernameOrPwd
            else:
                result = Userlogin(username, password)
                if result:
                    user = LoginUser.objects.create_user(username=username, password=password,
                                                         real_name=result, school_id=username)
                    user.save()
                    content = expire_token(user)
                    return Response(content, HTTP_201_CREATED)
                else:
                    raise WrongUsernameOrPwd


# 用户获取自己的信息
class UserSelfDetailView(mixins.RetrieveModelMixin,
                         generics.GenericAPIView):
    """
        仅限用户本人获取
    """

    # 该权限为当前登录用户只能获取自己信息
    permission_classes = (IsAuthenticated,)
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    # permission_classes = (AllowAny, )
    # queryset = LoginUser.objects.all()
    serializer_class = UserSelfDetailSerializer

    def get(self, request):
        user = request.user
        try:
            cont = UserSelfDetailSerializer(user)
            msg = Response(data={
                'error': '0',
                'data': cont.data,
            }, status=HTTP_200_OK)
        except Http404:    # 获取失败，没有找到对应数据
            raise FoundUserFailed
        return msg


# 获取用户对外显示信息
class UserPublicDetailView(mixins.RetrieveModelMixin,
                           generics.GenericAPIView):
    """
        所有用户可以获取
    """

    # 该权限为当前登录用户只能获取自己信息
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    # permission_classes = (AllowAny, )
    # queryset = LoginUser.objects.all()
    serializer_class = UserPublicDetailSerializer

    def get(self, request, pk):
        try:
            user = LoginUser.objects.get(pk=pk)
            cont = UserPublicDetailSerializer(user)
            msg = Response(data={
                'error': '0',
                'data': cont.data,
            }, status=HTTP_200_OK)
        except LoginUser.DoesNotExist:    # 获取失败，没有找到对应数据
            raise FoundUserFailed
        return msg


# 用户更改资料
class UserChangeInfoView(mixins.UpdateModelMixin,
                         generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = UserUpdateInfoSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # def put(self, request, pk):
    #     user = get_authentication(sign=request.META.get("HTTP_SIGN"), pk=pk)
    #     if user:
    #         serializer = UserDetailSerializer(data=request.data, partial=True)
    #         if serializer.is_valid(raise_exception=True):
    #             nickname = serializer.validated_data['nickname']
    #             headimg = serializer.validated_data['headimg']
    #             signature = serializer.validated_data['signature']
    #             sex = serializer.validated_data['sex']
    #             user.nickname = nickname
    #             user.headimg = headimg
    #             user.signature = signature
    #             user.sex = sex
    #             user.save(update_fields=['nickname', 'headimg', 'signature', 'sex'])
    #             msg = Response(HTTP_204_NO_CONTENT)
    #         else:
    #             msg = Response({
    #                 'error': '1',
    #                 'data': '',
    #                 'error_msg': 'Failed to update the information',
    #             })
    #         return msg
    #     else:
    #         return Response({
    #             'error': '1',
    #             'error_msg': 'Invalid token, Please login again'
    #         }, HTTP_400_BAD_REQUEST)


# 修改密码
class UserResetPasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserPasswordResetSerializer
    authentication_classes = (MyAuthentication,)

    def put(self, request):
        user = request.user
        serializer = UserPasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_password = serializer.validated_data['password']
            if user.check_password(new_password):
                raise PasswordIsSame
            else:
                try:
                    user.set_password(new_password)
                    user.save()
                    return Response(status=HTTP_204_NO_CONTENT)

                except Exception as e:
                    msg = {
                        'error': '1',
                        'data': '',
                        'error_msg': e
                    }
                    return Response(msg, HTTP_400_BAD_REQUEST)


# 绑定手机与解绑
class UserBindPhoneView(APIView):
    # permission_classes = (IsOwner, IsAuthenticated)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserBindPhoneSerializer
    authentication_classes = (MyAuthentication,)

    def put(self, request):
        user = request.user
        serializer = UserBindPhoneSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data['phone']
            try:
                user.phone = phone
                user.save(update_fields=['phone'])
                msg = Response(status=HTTP_204_NO_CONTENT)
            # except Http404:
            #     raise FoundUserFailed
            except Exception as e:
                msg = Response({
                    'error': 90500,
                    'error_msg': e
                }, HTTP_400_BAD_REQUEST)
            return msg

    def delete(self, request):
        user = request.user
        try:
            user.phone = ''
            user.save()
            msg = Response(status=HTTP_204_NO_CONTENT)
        except Http404:
            raise FoundUserFailed
        return msg


# 关注和取消关注
class MakeFriendView(APIView):
    # permission_classes = (IsAuthenticated, IsOwner)
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)

    def get(self, request, idol):
        user = request.user
        try:
            idols = LoginUser.objects.get(pk=idol)
        except LoginUser.DoesNotExist:
            raise FoundUserFailed

        if user == idols:
            raise FollowAuthenticationFailed

        follow = Follow.objects.create(follows=idols, fans=user)
        follow.save()
        msg = Response({
            'error': 0,
            'data': '',
            'message': 'Pay attention to the user successfully'
        }, HTTP_200_OK)
        return msg

    def delete(self, request, idol):
        fans = request.user
        try:
            idol = LoginUser.objects.get(pk=idol)
            follow = Follow.objects.get(fans=fans, follows=idol)
        except LoginUser.DoesNotExist:
            raise FoundUserFailed
        else:
            follow.delete()
            msg = Response({
                'error': 0,
                'data': '',
                'message': 'Unfollow the user successfully'
            }, HTTP_200_OK)
            return msg


# 获取关注的人
class GetFollowView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated, IsOwner)
    permission_classes = (AllowAny,)
    serializer_class = FollowSerializer
    pagination_class = Pagination
    # authentication_classes = (MyAuthentication,)

    def get_queryset(self):
        try:
            owner = LoginUser.objects.get(id=self.kwargs['pk'])
        except LoginUser.DoesNotExist:
            raise FoundUserFailed
        else:
            queryset = Follow.objects.filter(fans=owner)
            queryset = self.get_serializer().setup_eager_loading(queryset)
            return queryset.order_by('id')


# 获取粉丝列表
class GetFansView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FollowSerializer
    pagination_class = Pagination
    # authentication_classes = (MyAuthentication,)

    def get_queryset(self):
        try:
            owner = LoginUser.objects.get(id=self.kwargs['pk'])
        except LoginUser.DoesNotExist:
            raise FoundUserFailed
        else:
            queryset = Follow.objects.filter(follows=owner)
            return queryset.order_by('id')


# 404处理信息
def page_not_found(request):
    return render(request, '404.json')






