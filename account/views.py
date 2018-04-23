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
from .serializers import UserLoginSerializer, UserDetailSerializer
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rewrite.authentication import ExpiringTokenAuthentication
from .UserLogin import Userlogin
from .models import LoginUser
from django.contrib.auth import authenticate
from rewrite.authentication import expire_token
from rewrite.permissions import IsOwner
from rest_framework import mixins
from rest_framework import generics

from django.conf import settings

EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


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
            indatabase = LoginUser.objects.filter(username=username)
            if indatabase:
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
                'error_msg': 'Not found',
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
        except:
            msg = Response({
                'error': '1',
                'data': '',
                'error_msg': 'Failed to update the information',
            }, HTTP_400_BAD_REQUEST)
        return msg
        #return self.update(request, *args, **kwargs)


# 用户忘记










