from django.db import models
from django.conf import settings
# Create your models here.
from notice.models import Notice
from django.contrib.contenttypes import fields
from django.conf import settings
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# from django.shortcuts import reverse
# 消息推送
def push(username, event):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        username,
        {
            "type": "push.message",
            "event": event
        }
    )


def get_image_upload_to(instance, filename):

    return 'images/' + filename


# 图书
class Book(models.Model):
    LANGUAGE_CHOICE = (
        ('ch', '中文'),
        ('en', '英文')
    )
    COUNTRY_CHOICE = (
        ('in', '国内'),
        ('out', '国外')
    )
    TYPE_CHOICE = (
        ('1', '教辅'),
        ('2', '课外')
    )
    PLACE_CHOICE = (
        ('1', '信息学部'),
        ('2', '文理学部'),
        ('3', '工学部'),
        ('4', '医学部'),
    )
    # 图书所有者
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='books')
    # 图书名
    name = models.CharField(max_length=20, verbose_name='name')
    # 图书封面照片
    images = models.CharField(max_length=1024,
                              default=settings.PREFIX_URL + settings.QINIU_BUCKET_DOMAIN + '/' + "books/mask.png",
                              verbose_name='image')
    # 图书语言
    language = models.CharField(max_length=2, default='ch', choices=LANGUAGE_CHOICE, verbose_name='language')
    # 图书地界（国内或国外）
    country = models.CharField(max_length=3, default='in', choices=COUNTRY_CHOICE, verbose_name='country')
    # 图书类别（教辅或课外）
    types = models.CharField(max_length=1, default='2', choices=TYPE_CHOICE, verbose_name='types')
    # 地点
    place = models.CharField(max_length=1, default='1', choices=PLACE_CHOICE, verbose_name='place')
    # 图书等级
    level = models.CharField(max_length=4, verbose_name='level')
    # 消息通知
    notice = fields.GenericRelation(Notice)
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 最后一次更改时间
    updated_at = models.DateTimeField(auto_now=True)
    # 交换状态
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'Book'
        ordering = ['level']

    def __str__(self):
        return self.name

    def description(self):
        return '%s有图书《%s》在平台上等待交换' % (self.owner.nickname, self.name)


# 图书交换请求
class Application(models.Model):
    STATUS_CHOICE = (
        (0, '未查看'),
        (1, '已同意'),
        (2, '未同意')
    )
    # 请求方
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appli_sender')
    # 接收方
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appli_receiver')
    # 用于交换的图书
    frombook = models.ForeignKey(Book, related_name='frombook')
    # 想要交换的图书
    tobook = models.ForeignKey(Book, related_name='tobook')
    # 申请状态 0:未查看 1:同意 2:不同意
    status = models.IntegerField(default=0, choices=STATUS_CHOICE, verbose_name='status')

    def __str__(self):
        return self.sender.nickname

    def description(self):
        return {'sender': self.sender.nickname, 'frombook': self.frombook.name, 'tobook': self.tobook.name}

    class Meta:
        db_table = 'application'
        verbose_name_plural = u'图书交换申请'


# 商家
class Food(models.Model):
    PLACE_CHOICE = (
        ('1', '信息学部'),
        ('2', '文理学部'),
        ('3', '工学部'),
        ('4', '医学部'),
        ('5', '校外商家'),
        ('6', '校内商家'),
    )
    # 商家名称
    name = models.CharField(max_length=16, verbose_name='shop_name')
    # 商家地点
    location = models.CharField(max_length=1, verbose_name='location', default='1', choices=PLACE_CHOICE)
    # 图片
    images = models.CharField(max_length=1024,
                              default=settings.PREFIX_URL + settings.QINIU_BUCKET_DOMAIN + '/' + "shops/mask.png",
                              verbose_name='image')
    # 评分
    rating = models.FloatField(default=0.0, verbose_name='rating')
    # 商家介绍
    introduce = models.CharField(max_length=64, null=True, verbose_name='introduce')
    # 评论人数
    number = models.IntegerField(default=0, verbose_name='number')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Shop'
        ordering = ['created_at']

    def __str__(self):
        return self.name


# 对商家评论
class FoodComment(models.Model):
    # 评论者
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_owner')
    # 评论的商家
    food = models.ForeignKey(Food, related_name='comments')
    # 评论内容
    content = models.TextField(max_length=140, verbose_name='content', null=False)
    # 打分
    score = models.IntegerField(verbose_name='score', default=0)
    # 评论时间
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'FoodComment'
        ordering = ['created_at']

    def __str__(self):
        return self.food.name

    def description(self):
        return '%s评论了来自%s的美食' % (self.owner.nickname, self.food.name)


# 流浪猫狗信息
class Animals(models.Model):
    PLACE_CHOICE = (
        ('1', '信息学部'),
        ('2', '文理学部'),
        ('3', '工学部'),
        ('4', '医学部'),
    )
    # 地点
    location = models.CharField(max_length=1, default='1', choices=PLACE_CHOICE, verbose_name='location')
    # 作者(发布者)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='animalsAuthor')
    # 标题
    title = models.CharField(max_length=16, verbose_name='title')
    # 介绍
    content = models.CharField(max_length=114, verbose_name='content')
    # 创建时间
    created_at = models.DateTimeField(auto_now_add=True)
    # 图片
    images = models.CharField(max_length=1024, null=True, verbose_name='images')

    def __str__(self):
        return self.title


class AnimalSaveMsg(models.Model):
    PLACE_CHOICE = (
        ('1', '信息学部'),
        ('2', '文理学部'),
        ('3', '工学部'),
        ('4', '医学部'),
    )
    # 地点
    location = models.CharField(max_length=1, default='1', choices=PLACE_CHOICE, verbose_name='location')
    # 联系电话
    tel = models.CharField(max_length=149, verbose_name='telephone')
    # 救助群
    groupChat = models.CharField(max_length=149, verbose_name='groupChat')

    def __str__(self):
        return self.location


class Images(models.Model):
    # 图片
    image = models.ImageField(upload_to=get_image_upload_to, verbose_name='images', null=False)

    def __str__(self):
        return self.image

    def get_img_url(self):
        return settings.PREFIX_URL + settings.QINIU_BUCKET_DOMAIN + '/' + str(self.image)


@receiver(post_save, sender=Application)
def post_application_notice(sender, instance=None, created=False, **kwargs):
    entity = instance
    if created:
        event = Notice(sender=entity.sender, receiver=entity.receiver, event=entity, type=2)
        event.save()
        push(entity.receiver.username, {'type': 2})

