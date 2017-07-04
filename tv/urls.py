#_*_coding:UTF-8_*_

from django.conf.urls import url
from tv import views
#from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^(\d+)/$', views.tvDetail),
    url(r'^submit_reply/$', views.submitReply),
    url(r'^submit_reply_reply/$', views.submitReplyReply),
    url(r'^reply_like/$', views.replyLike),
    url(r'^get_more_comments/$', views.getMoreComments),
    url(r'^get_more_replies/$', views.getMoreReplies),
]
