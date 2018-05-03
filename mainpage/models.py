from django.db import models
from django.conf import settings
# Create your models here.
from notice.models import Notice
from django.contrib.contenttypes import fields
from django.db.models import signals


def get_upload_to(instance, filename):
    user = instance.owner.username
    bookname = instance.name
    return 'book/' + user + '-' + bookname + filename[-5:]


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
    name = models.CharField(max_length=20, verbose_name='book_name')
    # 图书封面照片
    image = models.ImageField(upload_to=get_upload_to, null=True, verbose_name='book_image')
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
    create_at = models.DateTimeField(auto_now_add=True)
    # 最后一次更改时间
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Book'
        ordering = ['level']

    def __str__(self):
        return self.name

    def description(self):
        return '%s有图书《%s》在平台上等待交换' % (self.owner.nickname, self.name)


# def book_save(sender, instance, signal, *args, **kwargs):
#     entity = instance
#     if str(entity.create_at)[:19] == str(entity.updated_at)[:19]:
#         for i in entity.owner.fans:
#             event = Notice(sender=entity.owner, receiver=i, event=entity, type=1)
#             event.save()
#
#
# signals.post_save.connect(book_save, sender=Book)
