# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-5-2

from django.conf.urls import url
from .views import (
    BookDetailView,
    UserBookListView,
    BookPublishView,
    GetAllBookView,
    ShopPublishView,
    FoodCommentPublishView,
    FoodCommentDetailView,
    ShopDetailView,
    GetShopCommentView,
    GetAllShopView,
    UploadImagesView,
)


urlpatterns = [
    url(r'^books/(?P<pk>\d+)$', BookDetailView.as_view(), name='book_detail'),
    url(r'^books/user/(?P<user_id>\d+)$', UserBookListView.as_view(), name='user_book'),
    url(r'^books/(?P<pk>\d+)/publish/', BookPublishView.as_view(), name='book_publish'),
    url(r'^books/$', GetAllBookView.as_view(), name='get_all_books'),
    url(r'^shops/publish/', ShopPublishView.as_view(), name="shop_publish"),
    url(r'^shops/(?P<pk>\d+)/comment/(?P<shop_id>\d+)/$', FoodCommentPublishView.as_view(), name='shop_comment_pub'),
    url(r'^shops/comments/(?P<pk>\d+)$', FoodCommentDetailView.as_view(), name='foodComment_detail'),
    url(r'^shops/(?P<pk>\d+)$', ShopDetailView.as_view(), name='shop_detail'),
    url(r'^shops/(?P<shop_id>\d+)/comments', GetShopCommentView.as_view(), name='get_shop_comments'),
    url(r'^shops/$', GetAllShopView.as_view(), name='get_all_shop'),
    url(r'^(?P<pk>\d+)/uploadImage/$', UploadImagesView.as_view(), name='upload_image')
]
