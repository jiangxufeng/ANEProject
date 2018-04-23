from django.conf.urls import url
from .views import UserLoginView, UserDetailView, UserChangeInfoView


urlpatterns = [
    url(r'^login/', UserLoginView.as_view(), name='user_login'),
    url(r'^detail/(?P<pk>\d+)/$', UserDetailView.as_view(), name='user_detail'),
    url(r'^detail/(?P<pk>\d+)/changeInfo', UserChangeInfoView.as_view(), name='user_detail')
]