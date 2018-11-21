# -*- coding:utf-8 -*-
# author: jiangxf
# created: 2018-07-16


from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    HyperlinkedRelatedField,
    ImageField,
    CharField,
    IntegerField,
    SerializerMethodField
)
from .models import Notice, Messages


class NoticeListSerializer(HyperlinkedModelSerializer):
    sender = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    nickname = SerializerMethodField()
    data = SerializerMethodField()
    nid = IntegerField(source='id')

    class Meta:
        model = Notice
        fields = ('sender', 'nickname', 'nid', 'data', 'type')

    def get_nickname(self, obj):
        return obj.sender.nickname

    def get_data(self, obj):
        return obj.event.description()


class MessageDetailSerializer(ModelSerializer):
    # sender = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    # receiver = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    sender = SerializerMethodField()
    receiver = SerializerMethodField()

    class Meta:
        model = Messages
        fields = ('id', 'sender', 'receiver', 'body', 'created')
        read_only_fields = ('created', )

    def get_sender(self, obj):
        return obj.sender.nickname

    def get_receiver(self, obj):
        return obj.receiver.nickname


class MessagePublishSerializer(ModelSerializer):
    # sender = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    # receiver = HyperlinkedRelatedField(view_name='user_public_detail', read_only=True)
    receiver = CharField()

    class Meta:
        model = Messages
        fields = ('receiver', 'body',)
