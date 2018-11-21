"""appapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from account.views import page_not_found


urlpatterns = [
    url(r'^ANEPAdmin/', admin.site.urls),
    url(r'^v1/users/', include('account.urls')),
    url(r'^v1/', include('mainpage.urls')),
    url(r'^v1/', include('circle.urls'),),
    url(r'^v1/', include('notice.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = page_not_found