# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-5-2

from django.conf.urls import url
from .views import (
    BookDetailView,
    UserBookListView,
    BookPublishView,
    BookListView,
    ShopPublishView,
    FoodCommentPublishView,
    FoodCommentDetailView,
    ShopDetailView,
    GetShopCommentView,
    GetAllShopView,
    UploadImagesView,
    AnimalsMsgPublishView,
    AnimalsMsgDetailView,
    AnimalsMsgListView,
    ApplicationPublishView,
    ApplicationReceiveView,
    ApplicationSendView,
    ApplicationHandleView,
)


urlpatterns = [
    url(r'^books/(?P<pk>\d+)$', BookDetailView.as_view(), name='book_detail'),
    url(r'^books/user/(?P<pk>\d+)$', UserBookListView.as_view(), name='user_book'),
    url(r'^books/publish/$', BookPublishView.as_view(), name='book_publish'),
    url(r'^books/$', BookListView.as_view(), name='get_all_books'),
    url(r'^books/applications/publish/$', ApplicationPublishView.as_view(), name='application_publish'),
    url(r'^books/applications/$', ApplicationReceiveView.as_view(), name='application_receive_list'),
    url(r'^books/send-applications/$', ApplicationSendView.as_view(), name='application_send_list'),
    url(r'^books/applications/(?P<apid>\d+)$', ApplicationHandleView.as_view(), name='application_handle'),
    url(r'^shops/publish/$', ShopPublishView.as_view(), name="shop_publish"),
    url(r'^shops/(?P<shop_id>\d+)/comment/$', FoodCommentPublishView.as_view(), name='shop_comment_pub'),
    url(r'^shops/comments/(?P<pk>\d+)$', FoodCommentDetailView.as_view(), name='foodComment_detail'),
    url(r'^shops/(?P<pk>\d+)$', ShopDetailView.as_view(), name='shop_detail'),
    url(r'^shops/(?P<shop_id>\d+)/comments/', GetShopCommentView.as_view(), name='get_shop_comments'),
    url(r'^shops/$', GetAllShopView.as_view(), name='get_all_shop'),
    url(r'^uploadImage/$', UploadImagesView.as_view(), name='upload_image'),
    url(r'^animals/publish/', AnimalsMsgPublishView.as_view(), name='animal_publish'),
    url(r'^animals/$', AnimalsMsgListView.as_view(), name='animal_list'),
    url(r'^animals/(?P<pk>\d+)$', AnimalsMsgDetailView.as_view(), name='animal_detail'),

]
