from rest_framework.serializers import (
    SerializerMethodField,
    ImageField,
    IntegerField,
    CharField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    ModelSerializer
)

from .models import PyPost, PostComment, PostLike, PostCommentReply


# 发布评论
class PostCommentPublishSerializer(ModelSerializer):
    pid = IntegerField()

    class Meta:
        model = PostComment
        fields = ('pid', 'content')


# 回复评论(二级)
class CommentsReplyPublishSerializer(ModelSerializer):
    comment = IntegerField(default=0)
    type = IntegerField(default=0)

    class Meta:
        model = PostCommentReply
        fields = ('comment', 'content', 'type')


# 回复评论详情(二级评论)
class CommentsReplyDetailSerializer(HyperlinkedModelSerializer):
    _to_nickname = SerializerMethodField()
    _from_nickname = SerializerMethodField()
    _from_url = HyperlinkedRelatedField(source="owner", view_name="user_public_detail", read_only=True)
    _to_url = HyperlinkedRelatedField(source="toWho", view_name="user_public_detail", read_only=True)
    rid = IntegerField(source='id')

    class Meta:
        model = PostCommentReply
        fields = ('_from_nickname', '_from_url', '_to_nickname', '_to_url', 'content', 'rid', 'created_at')

    def get__to_nickname(self, obj):
        return obj.toWho.nickname

    def get__from_nickname(self, obj):
        return obj.owner.nickname


# 评论详情
class PostCommentDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="user_public_detail", read_only=True)
    nickname = SerializerMethodField()
    headImg = SerializerMethodField()
    pcid = IntegerField(source='id')
    replies = CommentsReplyDetailSerializer(many=True)

    class Meta:
        model = PostComment
        fields = ('owner', 'headImg', 'nickname', 'content', 'pcid', 'created_at', 'replies')

    def get_nickname(self, obj):
        return obj.owner.nickname

    def get_headImg(self, obj):
        return obj.owner.get_headimg_url()


# 点赞
class PostLikePublishSerializer(ModelSerializer):
    # uid = IntegerField()
    pid = IntegerField()

    class Meta:
        model = PostLike
        fields = ('pid',)


# 点赞的返回信息
class PostLikeReturnSerializer(HyperlinkedModelSerializer):
    headimg = SerializerMethodField()
    owner = HyperlinkedRelatedField(view_name="user_public_detail", read_only=True)
    lid = IntegerField(source='id')

    class Meta:
        model = PostLike
        fields = ('owner', 'headimg', 'lid')

    def get_headimg(self, obj):
        return obj.owner.get_headimg_url()


# 发布帖子
class PyPostPublishSerializer(ModelSerializer):
    # uid = IntegerField()
    images = CharField(allow_null=True)

    class Meta:
        model = PyPost
        fields = ('title', 'content', 'images')


# 帖子列表
class PyPostListSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="user_public_detail", read_only=True)
    images = SerializerMethodField()
    likes_num = SerializerMethodField()
    nickname = SerializerMethodField()
    headImg = SerializerMethodField()
    comments_num = SerializerMethodField()
    pid = IntegerField(source='id')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('owner')
        return queryset

    class Meta:
        model = PyPost
        fields = ('owner', 'nickname', 'headImg', 'title', 'content',
                  'created_at', 'pid', 'likes_num', 'comments_num', 'images')

    def get_likes_num(self, obj):
        return obj.likes.all().count()

    def get_comments_num(self, obj):
        return obj.comments.all().count()

    def get_nickname(self, obj):
        return obj.owner.nickname

    def get_headImg(self, obj):
        return obj.owner.get_headimg_url()

    def get_images(self, obj):
        return obj.images.split(";")[:3] if obj.images else []


# 帖子详情
class PyPostDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="user_public_detail", read_only=True)
    nickname = SerializerMethodField()
    headImg = SerializerMethodField()
    likes = PostLikeReturnSerializer(many=True)
    comments = SerializerMethodField()
    pid = IntegerField(source='id')
    images = SerializerMethodField()

    class Meta:
        model = PyPost
        fields = ('owner', 'nickname', 'headImg', 'title', 'content',
                  'created_at', 'pid', 'likes', 'comments', 'images')

    def get_nickname(self, obj):
        return obj.owner.nickname

    def get_headImg(self, obj):
        return obj.owner.get_headimg_url()

    def get_comments(self, obj):
        return PostCommentDetailSerializer(obj.comments.all(), many=True, context={'request': None}).data[:6]

    def get_images(self, obj):
        return obj.images.split(";") if obj.images else []
