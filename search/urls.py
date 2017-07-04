#_*_coding:UTF-8_*_

from django.conf.urls import url
from search import views
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'value_change/$', views.valueChange),
    url(r'result/$', views.searchResult),
]
