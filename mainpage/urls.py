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
)


urlpatterns = [
    url(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book_detail'),
    url(r'^book/user/(?P<user_id>\d+)$', UserBookListView.as_view(), name='user_book'),
    url(r'^book/(?P<pk>\d+)/publish/', BookPublishView.as_view(), name='book_publish'),
    url(r'^book/$', GetAllBookView.as_view(), name='get_all_books'),
    url(r'^shop/publish/', ShopPublishView.as_view(), name="shop_publish"),
    url(r'^shop/(?P<pk>\d+)/comment/(?P<shop_id>\d+)/$', FoodCommentPublishView.as_view(), name='shop_comment_pub'),
    url(r'^shop/comments/(?P<pk>\d+)$', FoodCommentDetailView.as_view(), name='foodComment_detail'),
    url(r'^shop/detail/(?P<pk>\d+)$', ShopDetailView.as_view(), name='shop_detail'),
    url(r'^shop/(?P<shop_id>\d+)/comments', GetShopCommentView.as_view(), name='get_shop_comments'),
    url(r'^shop/$', GetAllShopView.as_view(), name='get_all_shop')
]
