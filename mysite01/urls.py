"""mysite01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from mysite01 import views
from django.conf import settings
from django.conf.urls.static import static

# from . import views

'''
path转换器：
str:匹配除了“/”之外的非空字符串
int:匹配0或任何正整数
slug:匹配任意由ASCII字母或数字以及连字符和下划线组成的短标签
path:匹配非空字段，包括路径分隔符“/”
'''
urlpatterns = [
    # 配置主路由
    path('admin/', admin.site.urls),
    # http://127.0.0.1:8000/page/2003/
    path('page/2003/', views.page_2003_view),
    # http://127.0.0.1:8000/
    path('', views.index_view),
    # http://127.0.0.1:8000/page/1
    path('page/1', views.page1_view),
    # http://127.0.0.1:8000/page/2
    path('page/2', views.page2_view),

    path('page/<int:pg>', views.pagen_view),

    # re_path()  ,只匹配两位以内的
    re_path(r'^(?P<x>\d{1,2})/(?P<op>\w+)/(?P<y>\d{1,2})$', views.cal2_view),

    # http://127.0.0.1:8000/整数/操作符/整数
    path('<int:n>/<str:op>/<int:m>', views.cal_view),

    # http://127.0.0.1:8000/birthday/年4/月2/日2
    re_path(r'^birthday/(?P<y>\d{4})/(?P<m>\d{1,2})/(?P<d>\d{1,2})$', views.birthday_view),
    # http://127.0.0.1:8000/birthday/月2/日2/年4
    re_path(r'^birthday/(?P<m>\d{1,2})/(?P<d>\d{1,2})/(?P<y>\d{4})$', views.birthday_view),

    # path('test_request', views.test_request),
    path('test_get_post', views.test_get_post),

    # http://127.0.0.1:8000/test_html/
    path('test_html/', views.test_html),
    # http://127.0.0.1:8000/test_if_for/
    path('test_if_for/', views.test_if_for),
    path('mycal/', views.test_mycal),

    path('base_index', views.base_view, name='base_index'),
    path('music_index', views.music_view),
    path('sport_index', views.sport_view),

    # http://127.0.0.1:8000/test/url
    path('test/url', views.test_url),
    # http://127.0.0.1:8000/test_url_result
    path('test_urls_result/<int:age>', views.test_url_result, name='tr'),

    path('test_static', views.test_static),

    # 配置分布式路由的主路由
    path('music/', include('music.urls')),
    path('news/', include('news.urls')),
    path('sports/', include('sports.urls')),

    path('bookstore/', include('bookstore.urls')),

    path('set_cookies/', views.set_cookies),
    path('get_cookies/', views.get_cookies),

    path('set_session/', views.set_session),
    path('get_session/', views.get_session),

    # 缓存测试
    path('test_cache/', views.test_cache),

    # 分页测试
    path('test_page/', views.test_page),

    # csv测试
    path('test_csv/', views.test_csv),

    path('make_page_csv', views.make_page_csv),

    # 上传文件
    path('test_upload/', views.test_upload)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
