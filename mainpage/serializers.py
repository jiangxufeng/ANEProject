# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-4-27

from .models import (
    Book,
    Food,
    FoodComment,
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


# 图书详情
class BookDetailSerializer(HyperlinkedModelSerializer):
    # owner = ReadOnlyField(source='owner.username')
    owner = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    bookId = IntegerField(source='id')

    class Meta:
        model = Book
        fields = ('owner', 'bookId', 'name', 'image', 'level', 'language', 'types',
                  'country', 'place', 'create_at', 'status')
        read_only_fields = ('name', 'image', 'level', 'language', 'types',
                            'country', 'place', 'create_at', 'status')


# 发布图书
class BookPublishSerializer(ModelSerializer):
    image = ImageField(default="book/mask.png")

    class Meta:
        model = Book
        fields = ('name', 'image', 'language', 'types', 'country', 'place')


# 发布一个商家
class ShopPublishSerializer(ModelSerializer):
    image = ImageField(default="book/mask.png")

    class Meta:
        model = Food
        fields = ('name', 'location', 'image', 'introduce')


# 商家详情
class ShopDetailSerializer(ModelSerializer):
    #   comments = HyperlinkedRelatedField(view_name='foodComment_detail', many=True, read_only=True)
    image = ImageField()
    shopId = IntegerField(source='id')
    comment_num = SerializerMethodField()

    class Meta:
        model = Food
        fields = ('name', 'shopId', 'location', 'rating', 'introduce', 'image', 'comment_num')

    def get_comment_num(self, obj):
        return obj.comments.all().count()


# 发布对商家的评论
class FoodCommentPublishSerializer(ModelSerializer):

    class Meta:
        model = FoodComment
        fields = ('content', 'score',)


# 评论详情
class FoodCommentDetailSerializer(HyperlinkedModelSerializer):
    owner = HyperlinkedRelatedField(view_name='user_detail', read_only=True)
    shop = ReadOnlyField(source='food.name')
    commentId = IntegerField(source='id')

    class Meta:
        model = FoodComment
        fields = ('owner', 'commentId', 'shop', 'content', 'score', 'created_at')

