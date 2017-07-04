#_*_coding:UTF-8_*_

from django.conf.urls import url
from userinfo import views
from django.views.generic.base import TemplateView, RedirectView

urlpatterns = [
    
    url(r'^quicklogin/$', views.quickLogin),
    url(r'^login/$', views.loginPage),
    url(r'^login/submit/$', views.loginSubmit),
    url(r'^register/$', views.registerPage),
    url(r'^register/submit/$', views.registerSubmit),
    url(r'^register/active/$', views.registerActive),
    url(r'^change_code/$', views.changeCode),
    url(r'^polling/$', views.userPolling),
    url(r'^home/$', views.homePage),
    url(r'^home/notification/$', views.userNotification),
    url(r'^home/settings/$', views.userSettings),
    url(r'^home/messages/$', views.userMessages),
    url(r'^home/messages/remove_badge/$', views.removeBadge),
    url(r'^home/get_more_msg/$', views.getMoreMsg),
    url(r'^profile/(?P<uid>\d+)/(?P<uname>[^/]*)/{0,1}$', views.userProfile),
    url(r'^profile/(?P<uid>\d+)/(?P<uname>[^/]*)/{0,1}collection/(?P<cate>[a-zA-Z]+)/$', views.userCollection),
    url(r'^logout/$', views.logout),
    url(r'^avatar/upload/$', views.uploadAvatar),
    url(r'^photo/upload/$', views.uploadPhoto),
    url(r'^photo/manage/$', views.managePhoto),
    url(r'^modify_settings/$', views.modifySettings),
    url(r'^upload_bg/$', views.upload_bg),
    url(r'^publish_speak/$', views.publishSpeak),
    url(r'^submit_speak_reply/$', views.submitSpeakReply),
    url(r'^submit_speak_rr/$', views.submitSpeakRR),
    url(r'^like_speak/$', views.likeSpeak),
    url(r'^delete_speak_reply/$', views.deleteSpeakReply),
    url(r'^delete_speak_rr/$', views.deleteSpeakRR),
    url(r'^delete_speak/$', views.deleteSpeak),
    url(r'^upload_speak_img/$', views.upload_speak_img),
    url(r'^delete_speak_img/$', views.deleteSpeakImg),
    url(r'^forget_pwd/$', views.forgetPwdPage),
    url(r'^forget_pwd/submit/$',views.forgetPwdSubmit),
    url(r'^forget_pwd/verify/$', views.forgetPwdverify),
    url(r'^forget_pwd/change/$',views.forgetPwdChange),
    url(r'^focus/$', views.focus),
    url(r'^collect/$', views.collect),
    url(r'^cancel_collect/$', views.cancelCollect),
    url(r'^send_message/$', views.sendMessage),
    url(r'^reply_check_login/$', views.replyCheckLogin),
]
