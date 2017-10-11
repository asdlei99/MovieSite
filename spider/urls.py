#_*_coding:UTF-8_*_

from django.conf.urls import url
from spider import views

urlpatterns = [
    url('crawl/$', views.crawl),
    url('update_score/$', views.update_score)
]
