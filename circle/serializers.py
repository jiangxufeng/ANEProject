from rest_framework.serializers import (
    SerializerMethodField,
    ImageField,
    IntegerField,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    ModelSerializer
)

from .models import PyPost, PostComment, PostImage, PostLike


# 上传图片
class UploadPostImageSerializer(ModelSerializer):
    image = ImageField(allow_null=False)
    uid = IntegerField()
    pid = IntegerField()

    class Meta:
        model = PostImage
        fields = ('uid', 'pid', 'image')


# 图片返回
class PostImageReturnSerializer(ModelSerializer):
    image = ImageField(allow_null=False)

    class Meta:
        model = PostImage
        fields = ('image',)


# 发布评论
class PostCommentPublishSerializer(ModelSerializer):
    uid = IntegerField()
    pid = IntegerField()

    class Meta:
        model = PostComment
        fields = ('uid', 'pid', 'content')


# 评论详情
class PostCommentDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="user_detail", read_only=True)
    nickname = SerializerMethodField()
    headImg = SerializerMethodField()
    pcid = IntegerField(source='id')

    class Meta:
        model = PostComment
        fields = ('owner', 'headImg', 'nickname', 'content', 'pcid', 'created_at')

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
    headImg = SerializerMethodField()
    owner = HyperlinkedRelatedField(view_name="user_detail", read_only=True)
    lid = IntegerField(source='id')

    class Meta:
        model = PostLike
        fields = ('owner', 'headImg', 'lid')

    def get_headImg(self, obj):
        return obj.owner.get_headimg_url()


# 发布帖子
class PyPostPublishSerializer(ModelSerializer):
    #uid = IntegerField()

    class Meta:
        model = PyPost
        fields = ('title', 'content')


# 帖子列表
class PyPostListSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="user_detail", read_only=True)
    postImages = SerializerMethodField()
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
                  'created_at', 'pid', 'likes_num', 'comments_num', 'postImages')

    def get_likes_num(self, obj):
        return obj.likes.all().count()

    def get_comments_num(self, obj):
        return obj.comments.all().count()

    def get_nickname(self, obj):
        return obj.owner.nickname

    def get_headImg(self, obj):
        return obj.owner.get_headimg_url()

    def get_postImages(self, obj):
        return PostImageReturnSerializer(obj.images.all(), many=True).data[:3]


# 帖子详情
class PyPostDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name="user_detail", read_only=True)
    nickname = SerializerMethodField()
    headImg = SerializerMethodField()
    likes = PostLikeReturnSerializer(many=True)
    comments = SerializerMethodField()
    pid = IntegerField(source='id')
    images = PostImageReturnSerializer(many=True)

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
