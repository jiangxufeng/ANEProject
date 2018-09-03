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
    owner = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    bid = IntegerField(source='id')
    BookImages = SerializerMethodField()
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
        fields = ('owner', 'headimg', 'nickname', 'bid', 'name', 'image', 'level', 'language', 'types',
                  'country', 'place', 'created_at', 'status', 'BookImages')
        read_only_fields = ('name', 'image', 'level', 'language', 'types',
                            'country', 'place', 'created_at', 'status')

    def get_BookImages(self, obj):
        return UploadImageSerializer(obj.BookImages.all(), many=True).data[:3]

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
    owner = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    # oid = SerializerMethodField()
    bid = IntegerField(source='id')
    BookImages = UploadImageSerializer(many=True)
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
        fields = ('owner', 'headimg', 'nickname', 'bid', 'name', 'image', 'level', 'language', 'types',
                  'country', 'place', 'created_at', 'status', 'BookImages')
        read_only_fields = ('name', 'image', 'level', 'language', 'types',
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


# 发布图书
class BookPublishSerializer(ModelSerializer):
    image = ImageField(default="books/mask.png")

    class Meta:
        model = Book
        fields = ('name', 'image', 'language', 'types', 'country', 'place')


# 提出图书交换请求
class ApplicationPublishSerializer(ModelSerializer):
    sender = IntegerField()
    # receiver = IntegerField()
    bid = IntegerField()

    class Meta:
        model = Application
        fields = ('sender', 'bid')


# 查看收到的申请请求
class ApplicationDetailSerializer(HyperlinkedModelSerializer):
    sender = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    # receiver = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    book = HyperlinkedRelatedField(view_name='book_detail', read_only=True)
    sNickname = SerializerMethodField()
    # rNickname = SerializerMethodField()
    bookName = SerializerMethodField()
    status = SerializerMethodField()

    class Meta:
        model = Application
        fields = ('sender', 'book', 'sNickname', 'bookName', 'status')

    def get_sNickname(self, obj):
        return obj.sender.nickname
    #
    # def get_rNickname(self, obj):
    #     return obj.receiver.nickname

    def get_bookName(self, obj):
        return obj.book.name

    def get_status(self, obj):
        if obj.status == 0:
            return "未查看"
        elif obj.status == 1:
            return "已同意"
        else:
            return "未同意"
        # return "未查看" if obj.status == 0 elif ""


# 发布一个商家
class ShopPublishSerializer(ModelSerializer):
    image = ImageField(default="foods/mask.png")
    introduce = CharField(default="")

    class Meta:
        model = Food
        fields = ('name', 'location', 'image', 'introduce')


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
    image = ImageField()
    sid = IntegerField(source='id')
    comment_num = SerializerMethodField()

    class Meta:
        model = Food
        fields = ('name', 'sid', 'location', 'rating', 'introduce', 'image', 'comment_num')

    def get_comment_num(self, obj):
        return obj.comments.all().count()


# 商家详情
class ShopDetailSerializer(ModelSerializer):
    #   comments = HyperlinkedRelatedField(view_name='foodComment_detail', many=True, read_only=True)
    image = ImageField()
    sid = IntegerField(source='id')
    comment_num = SerializerMethodField()
    ShopImages = UploadImageSerializer(many=True)
    comments = SerializerMethodField()

    class Meta:
        model = Food
        fields = ('name', 'sid', 'location', 'rating', 'introduce', 'image', 'comment_num', 'ShopImages', 'comments')

    def get_comment_num(self, obj):
        return obj.comments.all().count()

    # 只返回前六条评论，更多评论需要进一步加载评论
    def get_comments(self, obj):
        return FoodCommentDetailSerializer(obj.comments.all(), many=True).data[:6]


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

    class Meta:
        model = Animals
        fields = ('title', 'location', 'content')

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
    author = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    headimg = SerializerMethodField()
    nickname = SerializerMethodField()
    aid = IntegerField(source='id')
    AnimalImages = SerializerMethodField()

    class Meta:
        model = Animals
        fields = ('author', 'headimg', 'nickname', 'aid', 'title', 'content', 'location', 'created_at', 'AnimalImages')

    def get_nickname(self, obj):
        return obj.author.nickname

    def get_headimg(self, obj):
        return obj.author.get_headimg_url()

    def get_AnimalImages(self, obj):
        return UploadImageSerializer(obj.AnimalImage.all(), many=True).data[:3]


# 详情
class AnimalMsgDetailSerializer(HyperlinkedModelSerializer):
    author = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    headimg = SerializerMethodField()
    nickname = SerializerMethodField()
    aid = IntegerField(source='id')
    AnimalImages = UploadImageSerializer(many=True)

    class Meta:
        model = Animals
        fields = ('author', 'headimg', 'nickname', 'aid', 'title', 'content', 'location', 'AnimalImages')

    def get_nickname(self, obj):
        return obj.author.nickname

    def get_headimg(self, obj):
        return obj.author.get_headimg_url()