from django.conf.urls import url, include
from django.contrib import admin
from index.views import index, about_us, nav, rss
from django.views.generic.base import RedirectView, TemplateView
from movie import views as movie_views
from tv import views as tv_views
from anime import views as anime_views
from show import views as show_views
from news import views as news_views
from search import views as search_views
from bbs import views as bbs_views
from topic import views as topic_views
from django.conf.urls.static import static
from django.conf import settings

RedirectView.permanent = True

urlpatterns = [
    url(r'^$', index),
    url(r'^acaiba/', admin.site.urls),
    #url(r'^favicon.ico$', RedirectView.as_view(url='/static/images/favicon.ico', )),
    url(r'^movie/', include('movie.urls')),
    url(r'^movie/$', movie_views.movieIndex),
    url(r'^search/', include('search.urls')),
    url(r'^search/$', search_views.searchIndex),
    url(r'^tv/', include('tv.urls')),
    url(r'^tv/$', tv_views.tvIndex),
    url(r'^anime/', include('anime.urls')),
    url(r'^anime/$', anime_views.animeIndex),
    url(r'^show/', include('show.urls')),
    url(r'^show/$', show_views.showIndex),
    url(r'^news/', include('news.urls')),
    url(r'^news/$', news_views.newsIndex),
    url(r'^topic/$', topic_views.topicIndex),
    url(r'^user/', include('userinfo.urls')),
    url(r'^bbs/', include('bbs.urls')),
    url(r'^bbs/$', bbs_views.bbsIndex),
    url(r'^about_us/$', about_us),
    url(r'^nav/$', nav),
    url(r'^rss/$', rss),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^sitemap\.xml$', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml')),
    url(r'^sitemap2\.xml$', TemplateView.as_view(template_name='sitemap2.xml', content_type='application/xml')),
    url(r'^sitemap3\.xml$', TemplateView.as_view(template_name='sitemap3.xml', content_type='application/xml')),
    url(r'^rss\.xml$', TemplateView.as_view(template_name='rss.xml', content_type='application/xml')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)