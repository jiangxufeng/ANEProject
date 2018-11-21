# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-4-27

from .models import (
    Book,
    Food,
    FoodComment,
    Images,
    Animals,
    AnimalSaveMsg,
    Application,
)
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    ImageField,
    CharField,
    IntegerField,
    SerializerMethodField
)
from rest_framework.validators import ValidationError


# 上传图片
class UploadImageSerializer(ModelSerializer):
    image = ImageField(allow_null=False)

    class Meta:
        model = Images
        fields = ('image',)


# 图书列表
class BookListSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    bid = IntegerField(source='id')
    images = SerializerMethodField()
    headimg = SerializerMethodField()
    nickname = SerializerMethodField()
    place = SerializerMethodField()
    language = SerializerMethodField()
    types = SerializerMethodField()
    country = SerializerMethodField()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('owner')
        return queryset

    class Meta:
        model = Book
        fields = ('owner', 'headimg', 'nickname', 'bid', 'name', 'level', 'language', 'types',
                  'country', 'place', 'created_at', 'status', 'images')
        read_only_fields = ('name', 'images', 'level', 'language', 'types',
                            'country', 'place', 'created_at', 'status')

    def get_images(self, obj):
        return obj.images.split(";")[:3]

    def get_nickname(self, obj):
        return obj.owner.nickname

    def get_headimg(self, obj):
        return obj.owner.get_headimg_url()

    def get_place(self, obj):
        return obj.get_place_display()

    def get_language(self, obj):
        return obj.get_language_display()

    def get_types(self, obj):
        return obj.get_types_display()

    def get_country(self, obj):
        return obj.get_country_display()


# 图书详情
class BookDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    # oid = SerializerMethodField()
    bid = IntegerField(source='id')
    images = SerializerMethodField()
    headimg = SerializerMethodField()
    nickname = SerializerMethodField()
    place = SerializerMethodField()
    language = SerializerMethodField()
    types = SerializerMethodField()
    country = SerializerMethodField()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('owner')
        return queryset

    class Meta:
        model = Book
        fields = ('owner', 'headimg', 'nickname', 'bid', 'name', 'level', 'language', 'types',
                  'country', 'place', 'created_at', 'status', 'images')
        read_only_fields = ('name', 'images', 'level', 'language', 'types',
                            'country', 'place', 'created_at', 'status')

    # def get_oid(self, obj):
    #     return obj.owner.id
    def get_place(self, obj):
        return obj.get_place_display()

    def get_language(self, obj):
        return obj.get_language_display()

    def get_types(self, obj):
        return obj.get_types_display()

    def get_country(self, obj):
        return obj.get_country_display()

    def get_nickname(self, obj):
        return obj.owner.nickname

    def get_headimg(self, obj):
        return obj.owner.get_headimg_url()

    def get_images(self, obj):
        return obj.images.split(";")


# 发布图书
class BookPublishSerializer(ModelSerializer):
    images = CharField(default="http://p9260z3xy.bkt.clouddn.com/books/mask.png")

    class Meta:
        model = Book
        fields = ('name', 'images', 'language', 'types', 'country', 'place')


# 提出图书交换请求
class ApplicationPublishSerializer(ModelSerializer):
    # sender = IntegerField()
    # receiver = IntegerField()
    from_bid = IntegerField()
    to_bid = IntegerField()

    class Meta:
        model = Application
        fields = ('from_bid', 'to_bid')


# 查看收到的申请请求
class ApplicationDetailSerializer(HyperlinkedModelSerializer):
    sender = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    # receiver = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    frombook = HyperlinkedRelatedField(view_name='book_detail', read_only=True)
    tobook = HyperlinkedRelatedField(view_name='book_detail', read_only=True)
    sNickname = SerializerMethodField()
    fbookname = SerializerMethodField()
    tbookname = SerializerMethodField()
    status = SerializerMethodField()
    apid = IntegerField(source='id')

    @staticmethod
    def set_eager_loading(queryset):
        queryset = queryset.select_related('sender')
        queryset = queryset.select_related('frombook')
        queryset = queryset.select_related('tobook')
        return queryset

    class Meta:
        model = Application
        fields = ('sender', 'sNickname', 'frombook', 'fbookname', 'tobook', 'tbookname', 'status', 'apid')

    def get_sNickname(self, obj):
        return obj.sender.nickname
    #
    # def get_rNickname(self, obj):
    #     return obj.receiver.nickname

    def get_fbookname(self, obj):
        return obj.frombook.name

    def get_tbookname(self, obj):
        return obj.tobook.name

    def get_status(self, obj):
        return obj.get_status_display()


# 发布一个商家
class ShopPublishSerializer(ModelSerializer):
    images = CharField(default="http://p9260z3xy.bkt.clouddn.com/foods/mask.png")
    introduce = CharField(default="")

    class Meta:
        model = Food
        fields = ('name', 'location', 'images', 'introduce')


# 评论详情
class FoodCommentDetailSerializer(ModelSerializer):
    owner = SerializerMethodField()
    headimg = SerializerMethodField()

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('owner')
        queryset = queryset.select_related('food')
        return queryset

    class Meta:
        model = FoodComment
        fields = ('owner', 'headimg', 'content', 'score', 'created_at')

    def get_owner(self, obj):
        return obj.owner.nickname

    def get_headimg(self, obj):
        return obj.owner.get_headimg_url()


# 商家列表
class ShopListSerializer(ModelSerializer):
    images = SerializerMethodField()
    sid = IntegerField(source='id')
    comment_num = SerializerMethodField()
    location = SerializerMethodField()

    class Meta:
        model = Food
        fields = ('name', 'sid', 'location', 'rating', 'introduce', 'images', 'comment_num')

    def get_comment_num(self, obj):
        return obj.comments.all().count()

    def get_images(self, obj):
        return obj.images.split(";")[:3]

    def get_location(self, obj):
        return obj.get_location_display()


# 商家详情
class ShopDetailSerializer(ModelSerializer):
    #   comments = HyperlinkedRelatedField(view_name='foodComment_detail', many=True, read_only=True)
    sid = IntegerField(source='id')
    comment_num = SerializerMethodField()
    comments = SerializerMethodField()
    images = SerializerMethodField()
    location = SerializerMethodField()

    class Meta:
        model = Food
        fields = ('name', 'sid', 'location', 'rating', 'introduce', 'images', 'comment_num', 'comments')

    def get_comment_num(self, obj):
        return obj.comments.all().count()

    # 只返回前六条评论，更多评论需要进一步加载评论
    def get_comments(self, obj):
        return FoodCommentDetailSerializer(obj.comments.all(), many=True).data[:6]

    def get_images(self, obj):
        return obj.images.split(";")

    def get_location(self, obj):
        return obj.get_location_display()


# 发布对商家的评论
class FoodCommentPublishSerializer(ModelSerializer):

    class Meta:
        model = FoodComment
        fields = ('content', 'score',)

    def validate_score(self, value):
        data = int(self.get_initial()['score'])
        if data > 5 or data < 0:
            raise ValidationError('Your score needs to be between 0 and 5')
        return value


# 发布流浪猫狗信息
class AnimalMsgPublishSerializer(ModelSerializer):
    images = CharField(allow_null=True)

    class Meta:
        model = Animals
        fields = ('title', 'location', 'content', 'images')

    # def validate_location(self, value):
    #     data = self.get_initial()['location']
    #     choice = ["1", "2", "3", "4"]
    #     temp = set(choice)
    #     if data not in temp:
    #         raise ValidationError("Location needs to be between '1' and '4'")
    #     return value
    #
    # def validate_title(self, value):
    #     data = self.get_initial()['title']
    #     if len(data) > 16:
    #         raise ValidationError("Ensure this field has no more than 16 characters.")
    #     return value


# 流浪动物列表
class AnimalMsgListSerializer(HyperlinkedModelSerializer):
    author = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    headimg = SerializerMethodField()
    nickname = SerializerMethodField()
    aid = IntegerField(source='id')
    images = SerializerMethodField()
    location = SerializerMethodField()

    @staticmethod
    def set_eager_loading(queryset):
        queryset = queryset.select_related('author')
        return queryset

    class Meta:
        model = Animals
        fields = ('author', 'headimg', 'nickname', 'aid', 'title', 'content', 'location', 'created_at', 'images')

    def get_nickname(self, obj):
        return obj.author.nickname

    def get_headimg(self, obj):
        return obj.author.get_headimg_url()

    def get_images(self, obj):
        return obj.images.split(";")[:3] if obj.images else []

    def get_location(self, obj):
        return obj.get_location_display()


# 流浪猫狗信息详情
class AnimalMsgDetailSerializer(HyperlinkedModelSerializer):
    author = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    headimg = SerializerMethodField()
    nickname = SerializerMethodField()
    aid = IntegerField(source='id')
    images = SerializerMethodField()
    location = SerializerMethodField()

    class Meta:
        model = Animals
        fields = ('author', 'headimg', 'nickname', 'aid', 'title', 'content', 'location', 'images')

    def get_nickname(self, obj):
        return obj.author.nickname

    def get_headimg(self, obj):
        return obj.author.get_headimg_url()

    def get_images(self, obj):
        return obj.images.split(";") if obj.images else []

    def get_location(self, obj):
        return obj.get_location_display()


# 申请处理
class ApplicationHandleSerializer(ModelSerializer):
    result = IntegerField()

    class Meta:
        model = Application
        fields = ('result',)

    def validate_result(self, value):
        data = int(self.get_initial()['result'])
        if data not in [1, 2]:
            raise ValidationError('Invalid param!')
        return value

