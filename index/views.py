#_*_coding:UTF-8_*_
from django.shortcuts import render_to_response
from movie import models
from django.template.context import RequestContext
#from os import path
from packages.general import loginInfo, getTodayStr
from packages.movie_helper import replaceWrongImg

def index(request):
    ret = {'logined':False}
    #判断用户是否登录
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    #sliders
    ret['sliders'] = models.Index_Slider.objects.all().order_by('-id')[:5]
    
    today_str = getTodayStr()
    
    #Movies
    movie_new_obj = models.Movie.objects.filter(release_date__lte=today_str).order_by('-release_date')[:12]
    movie_future_obj = models.Movie.objects.filter(release_date__gt=today_str).order_by('release_date')[:12]
    ret['movie_new_release'] = replaceWrongImg(movie_new_obj, img_type='p')
    ret['movie_near_future'] = replaceWrongImg(movie_future_obj, img_type='p')
    movie_recommend_obj = models.Movie_Recommend.objects.filter(cate=1).order_by('-create_date')[:4]
    ret['movie_recommend'] = []
    for item in movie_recommend_obj:
        try:
            temp_obj = models.Movie.objects.get(id=item.media_id)
            temp_obj.reason = item.reason
            ret['movie_recommend'].append(temp_obj)
        except Exception:
            pass
    ret['movie_weekly_top'] = models.Movie.objects.filter(release_date__lte=today_str).values('id','ch_name', 'score').order_by('-week_visit_count', '-release_date')[:10]
    ret['movie_monthly_top'] = models.Movie.objects.filter(release_date__lte=today_str).values('id','ch_name', 'score').order_by('-month_visit_count', '-release_date')[:10]
    
    #TVs
    tv_new_obj = models.Tv.objects.filter(score__gt=0).order_by('-release_date')[:12]
    ret['tv_new_release'] = replaceWrongImg(tv_new_obj, img_type='p')
    tv_recommend_obj = models.Movie_Recommend.objects.filter(cate=2).order_by('-create_date')[:4]
    ret['tv_recommend'] = []
    for item in tv_recommend_obj:
        try:
            temp_obj = models.Tv.objects.get(id=item.media_id)
            temp_obj.reason = item.reason
            ret['tv_recommend'].append(temp_obj)
        except Exception:
            pass
    ret['tv_weekly_top'] = models.Tv.objects.values('id','ch_name', 'score').order_by('-week_visit_count', '-release_date')[:10]
    ret['tv_monthly_top'] = models.Tv.objects.values('id','ch_name', 'score').order_by('-month_visit_count', '-release_date')[:10]
    
    
    #News
    ret['news_new'] = models.News.objects.all().values('id', 'title', 'subtitle', 'news_image', 'create_date').order_by('-create_date')[:6]
    ret['news_hot'] = models.News.objects.all().values('id', 'title', 'subtitle', 'news_image', 'create_date').order_by('-week_visit_count')[:6]

    ret['news_weekly_top'] = models.News.objects.all().values('id', 'title').order_by('-week_visit_count', '-create_date')[:10]
    ret['news_daily_top'] = models.News.objects.all().values('id', 'title').order_by('-day_visit_count', '-create_date')[:10]
    
    #anime
    anime_new_obj = models.Anime.objects.filter(score__gt=0).order_by('-release_date')[:12]
    ret['anime_new_release'] = replaceWrongImg(anime_new_obj, img_type='p')
    anime_recommend_obj = models.Movie_Recommend.objects.filter(cate=3).order_by('-create_date')[:4]
    ret['anime_recommend'] = []
    for item in anime_recommend_obj:
        try:
            temp_obj = models.Anime.objects.get(id=item.media_id)
            temp_obj.reason = item.reason
            ret['anime_recommend'].append(temp_obj)
        except Exception:
            pass
    ret['anime_weekly_top'] = models.Anime.objects.values('id', 'ch_name', 'score').order_by('-week_visit_count', '-release_date')[:10]
    ret['anime_monthly_top'] = models.Anime.objects.values('id', 'ch_name', 'score').order_by('-month_visit_count', '-release_date')[:10]
    
    #show
    show_new_obj = models.Show.objects.filter(score__gt=0).order_by('-release_date')[:12]
    ret['show_new_release'] = replaceWrongImg(show_new_obj, img_type='p')
    show_recommend_obj = models.Movie_Recommend.objects.filter(cate=4).order_by('-create_date')[:4]
    ret['show_recommend'] = []
    for item in show_recommend_obj:
        try:
            temp_obj = models.Show.objects.get(id=item.media_id)
            temp_obj.reason = item.reason
            ret['show_recommend'].append(temp_obj)
        except Exception:
            pass
    ret['show_weekly_top'] = models.Show.objects.values('id', 'ch_name', 'score').order_by('-week_visit_count', '-release_date')[:10]
    ret['show_monthly_top'] = models.Show.objects.values('id', 'ch_name', 'score').order_by('-month_visit_count', '-release_date')[:10]
    
    return render_to_response('index/index.html', ret, context_instance=RequestContext(request))

def about_us(request):
    #ret = {}
    return render_to_response('others/about_us.html')

def nav(request):
    #ret = {}
    return render_to_response('others/nav.html')

def rss(request):
    #ret = {}
    return render_to_response('others/rss.html')
