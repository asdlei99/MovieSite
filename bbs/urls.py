#_*_coding:UTF-8_*_

from django.conf.urls import url
from bbs import views

urlpatterns = [
    url(r'^board/$', views.boardIndex),
    url(r'^post/(\d+)/$', views.postDetail),
    url(r'^upload_img/$', views.uploadImg),
    url(r'^submit_reply/$', views.submitReply),
    url(r'^submit_post/$', views.submitPost),
    url(r'^submit_layer_reply/$', views.submitLayerReply),
    url(r'^delete_reply/$', views.deleteReply),
    url(r'^delete_lr/$', views.deleteLR),
    url(r'^delete_post/$', views.deletePost),
    url(r'^get_layer_reply_items/$', views.getLayerReplyItems),
    #url(r'$', views.bbsIndex),
    

]
