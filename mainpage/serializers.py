# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-4-27

from .models import Book
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    ReadOnlyField,
    HyperlinkedRelatedField,
    ImageField
)


# 图书详情
class BookDetailSerializer(HyperlinkedModelSerializer):
    # owner = ReadOnlyField(source='owner.username')
    owner = HyperlinkedRelatedField(view_name='user_detail', read_only=True)

    class Meta:
        model = Book
        fields = ('owner', 'id', 'name', 'image', 'level', 'language', 'types',
                  'country', 'place', 'create_at')
        read_only_fields = ('name', 'image', 'level', 'language', 'types',
                            'country', 'place', 'create_at')


# 发布图书
class BookPublishSerializer(ModelSerializer):
    image = ImageField(allow_null=True)

    class Meta:
        model = Book
        fields = ('name', 'image', 'language', 'types', 'country', 'place')


