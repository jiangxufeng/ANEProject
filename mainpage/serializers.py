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
)
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    ReadOnlyField,
    HyperlinkedRelatedField,
    ImageField,
    CharField,
    IntegerField,
    SerializerMethodField
)
from rest_framework.validators import ValidationError



# 图书详情
class BookDetailSerializer(HyperlinkedModelSerializer):
    # owner = ReadOnlyField(source='owner.username')
    owner = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    bid = IntegerField(source='id')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('owner')
        return queryset

    class Meta:
        model = Book
        fields = ('owner', 'bid', 'name', 'image', 'level', 'language', 'types',
                  'country', 'place', 'create_at', 'status')
        read_only_fields = ('name', 'image', 'level', 'language', 'types',
                            'country', 'place', 'create_at', 'status')


# 发布图书
class BookPublishSerializer(ModelSerializer):
    image = ImageField(default="books/mask.png")

    class Meta:
        model = Book
        fields = ('name', 'image', 'language', 'types', 'country', 'place')


# 发布一个商家
class ShopPublishSerializer(ModelSerializer):
    image = ImageField(default="foods/mask.png")

    class Meta:
        model = Food
        fields = ('name', 'location', 'image', 'introduce')


# 商家详情
class ShopDetailSerializer(ModelSerializer):
    #   comments = HyperlinkedRelatedField(view_name='foodComment_detail', many=True, read_only=True)
    image = ImageField()
    sid = IntegerField(source='id')
    comment_num = SerializerMethodField()

    class Meta:
        model = Food
        fields = ('name', 'sid', 'location', 'rating', 'introduce', 'image', 'comment_num')

    def get_comment_num(self, obj):
        return obj.comments.all().count()


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


# 评论详情
class FoodCommentDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    shop = ReadOnlyField(source='food.name')
    commentId = IntegerField(source='id')

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('owner')
        queryset = queryset.select_related('food')
        return queryset

    class Meta:
        model = FoodComment
        fields = ('owner', 'commentId', 'shop', 'content', 'score', 'created_at')


# 上传图片
class UploadImageSerializer(ModelSerializer):
    image = ImageField(allow_null=False)

    class Meta:
        model = Images
        fields = ('types', 'image')


# 返回图片信息序列化
class UploadImageDetailSerializer(ModelSerializer):
    image = ImageField(allow_null=False)

    class Meta:
        model = Images
        fields = ('types', 'image', 'owner')
