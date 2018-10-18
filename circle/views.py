# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-08

from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
)
from .serializers import (
    PostCommentDetailSerializer,
    PostCommentPublishSerializer,
    PyPostPublishSerializer,
    PyPostDetailSerializer,
    PyPostListSerializer,
    PostLikePublishSerializer,
    PostLikeReturnSerializer,
    CommentsReplyDetailSerializer,
    CommentsReplyPublishSerializer,
)
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import PostLike, PostComment, PyPost, PostCommentReply
from rewrite.permissions import IsOwnerOrReadOnly
from rewrite.pagination import Pagination
from rewrite.authentication import MyAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rewrite.exception import (
    FoundPostFailed,
    UserLikedPost,
    FoundLikeFailed,
    UserIsNotTheOwnerOfLike,
    FoundCommentFailed
)
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from notice.models import Notice


def msg(request, username):
    return render(request, 'example/dongtai.html', {
        'room_name_json': mark_safe(json.dumps(username))
    })


# 发帖
class PyPostPublishView(APIView):
    """
       已认证用户具有权限
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = PyPostPublishSerializer
    authentication_classes = (MyAuthentication,)

    def post(self, request):
        owner = request.user
        serializer = PyPostPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data['title']
            content = serializer.validated_data['content']
            images = serializer.validated_data['images']
            passage = PyPost.objects.create(owner=owner, title=title, content=content, images=images)
            passage.save()
            msg = Response({
                'error': 0,
                'data': PyPostListSerializer(passage, context={'request': request}).data,
                'message': 'Success to publish the post.'
            }, HTTP_201_CREATED)
            return msg


# 获取全部帖子并展示
class PyPostListView(generics.ListAPIView):
    """
       未认证用户允许获取
    """
    permission_classes = (AllowAny,)
    # authentication_classes = (MyAuthentication, )
    serializer_class = PyPostListSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 筛选图书，筛选条件：交换状态、地点、作者国家、语言、类型
    # filter_fields = ('status', 'place', 'country', 'language', 'types')
    # ordering_fields = ('level', 'place')
    search_fields = ('title',)

    def get_queryset(self):
        queryset = PyPost.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.order_by('-created_at')


# 某个帖子详情
class PyPostDetailView(generics.RetrieveDestroyAPIView):
    """
       未认证用户允许获取，已认证用户允许获取与删除自己的帖子
    """
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (MyAuthentication,)
    serializer_class = PyPostDetailSerializer
    queryset = PyPost.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            cont = self.retrieve(request, *args, **kwargs)
            msg = Response(data={
                'error': 0,
                'data': cont.data,
            }, status=HTTP_200_OK)
        except Http404:  # 获取失败，没有找到对应数据
            raise FoundPostFailed
        else:
            return msg

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# 返回某用户发布的所有帖子
class PyPostOfUserListView(generics.ListAPIView):
    """
       返回已认证用户的所有帖子
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = PyPostListSerializer
    pagination_class = Pagination

    def get_queryset(self):
        user = self.request.user
        queryset = PyPost.objects.filter(owner=user)
        return queryset.order_by('-created_at')


# 评论
class PostCommentPublishView(APIView):
    """
       已认证用户允许评论
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = PostCommentPublishSerializer

    def get_posts(self, pid):
        try:
            return PyPost.objects.get(id=pid)
        except PyPost.DoesNotExist:
            raise FoundPostFailed

    def post(self, request):
        owner = request.user
        serializer = PostCommentPublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pid = serializer.validated_data['pid']
            psg = self.get_posts(pid)
            content = serializer.validated_data['content']
            passage = PostComment.objects.create(owner=owner, passage=psg, content=content)
            passage.save()
            msg = Response({
                'error': 0,
                'data': PostCommentDetailSerializer(passage, context={'request': request}).data,
                'message': 'Success to comment the post.'
            }, HTTP_201_CREATED)
            return msg


# 某篇帖子的所有评论
class PostCommentsListView(generics.ListAPIView):
    """
        所有用户都允许获取
    """
    permission_classes = (AllowAny,)
    # authentication_classes = (MyAuthentication,)
    serializer_class = PostCommentDetailSerializer
    pagination_class = Pagination

    def get_posts(self, pid):
        try:
            return PyPost.objects.get(id=pid)
        except PyPost.DoesNotExist:
            raise FoundPostFailed

    def get_queryset(self):
        passage = self.get_posts(pid=self.kwargs['pid'])
        queryset = PostComment.objects.filter(passage=passage)
        return queryset.order_by('-created_at')


# 点赞
class PostLikePublishView(APIView):
    """
        已认证用户允许点赞
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = PostLikePublishSerializer

    def get_posts(self, pid):
        try:
            return PyPost.objects.get(id=pid)
        except PyPost.DoesNotExist:
            raise FoundPostFailed

    def post(self, request):
        owner = request.user
        serializer = PostLikePublishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            pid = serializer.validated_data['pid']
            psg = self.get_posts(pid)
            try:
                PostLike.objects.get(owner=owner, passage=psg)
                raise UserLikedPost
            except PostLike.DoesNotExist:
                passage = PostLike.objects.create(owner=owner, passage=psg)
                passage.save()
                msg = Response({
                    'error': 0,
                    'data': PostLikeReturnSerializer(passage, context={'request': request}).data,
                    'message': 'Success to like the post.'
                }, HTTP_201_CREATED)
                return msg


# 取消点赞
class PostLikeDeleteView(generics.DestroyAPIView):
    """
        以认证用户允许取消自己所点的赞
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (MyAuthentication,)
    # serializer_class = PyPostDetailSerializer
    queryset = PostLike.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_destroy(self, instance):
        Notice.objects.get(object_id=instance.id, type=4).delete()
        instance.delete()


# 回复评论
class CommentReplyPublishView(APIView):
    """
        已认证用户可以回复其他用户的评论
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MyAuthentication,)
    serializer_class = CommentsReplyPublishSerializer

    def get_comment(self, comment):
        try:
            return PostComment.objects.get(id=comment)
        except PostComment.DoesNotExist:
            raise FoundCommentFailed

    def get_reply(self, comment):
        try:
            return PostCommentReply.objects.get(id=comment)
        except PostCommentReply.DoesNotExist:
            raise FoundCommentFailed

    def post(self, request):
        serializer = CommentsReplyPublishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        type = serializer.validated_data['type']

        if type:   # 如果rid为1，则代表回复的是一条评论下的其他回复
            reply = self.get_reply(type)
            comment = reply.commentParent
            toWho = reply.owner
        else:    # 如果rid为0，则代表回复的是一条评论
            comment = self.get_comment(serializer.validated_data['comment'])
            toWho = comment.owner

        content = serializer.validated_data['content']
        owner = request.user
        reply = PostCommentReply.objects.create(owner=owner, commentParent=comment, content=content, toWho=toWho)
        reply.save()
        return Response({
            'error': 0,
            'data': serializer.data,
            'message': 'Success to reply the comment.'
        }, status=HTTP_201_CREATED)


# 删除回复的评论
class CommentReplyDeleteView(generics.DestroyAPIView):
    """
        已认证用户删除自己回复他人的评论
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (MyAuthentication,)
    queryset = PostCommentReply.objects.all()