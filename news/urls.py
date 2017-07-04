#_*_coding:UTF-8_*_

from django.conf.urls import url
from news import views

urlpatterns = [
    url(r'^(\d+)/$', views.newstemplate),
    url(r'^get_more_news/$', views.getMoreNews),
    url(r'^submit_reply/$', views.submitReply),
    url(r'^submit_reply_reply/$', views.submitReplyReply),
    url(r'^reply_like/$', views.replyLike),
    url(r'^get_more_comments/$', views.getMoreComments),
    url(r'^get_more_replies/$', views.getMoreReplies),
]