# coding=utf-8

from django.conf.urls import url
from tools import views

urlpatterns = [
    url(r'shadowsocks/$', views.shadowsocks),
    url(r'shadowsocks/see_world/$', views.see_world)
]