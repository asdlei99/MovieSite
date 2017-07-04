#_*_coding:UTF-8_*_
from django.shortcuts import render_to_response, HttpResponse, Http404
from movie import models
from packages.general import try_int, loginInfo
from packages import html_helper, movie_helper, user_helper
from random import randint
from django.db.models import Q
from django.template.context import RequestContext
import json, re
#from datetime import datetime, date
from os import path
from MovieSite.settings import BASE_DIR
from packages.general import htmlContentFilter, CJsonEncoder, getTodayStr
from packages.templatetags.my_tags import my_datetrans



def movieDetail(request, *args, **kwargs):
    ret = {'logined':False, 'user_info':'', 'has_rated':False}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    if user_obj:
        uid = user_obj.id
    #右侧边栏
    billboard1 = models.Movie.objects.all().order_by('-week_visit_count')[0]
    billboard2 = models.Movie.objects.all().order_by('-week_visit_count')[1:10]
    ret['billboard1'] = billboard1
    if not path.exists(BASE_DIR+ret['billboard1'].poster):
        ret['billboard1'].poster = '/static/images/default/poster/p_200x284.png'
    ret['billboard2'] = billboard2
    for item in ret['billboard2']:
        if not path.exists(BASE_DIR+item.poster):
            item.poster = '/static/images/default/poster/p_200x284.png'
    
    #电影信息
    mid = args[0]
    ret['mid'] = mid
    try:
        movie_obj = models.Movie.objects.get(id=mid)
    except Exception:
        raise Http404
        #return render_to_response('404.html')
    
    movie_obj.visit_count += 1
    movie_obj.week_visit_count += 1
    movie_obj.month_visit_count += 1
    movie_obj.save()

    #ret['detail'] = movie_obj
    ret['detail'] = movie_helper.replaceWrongImg([movie_obj], 'ps')[0]
    #ret['face_id'] = str(randint(1,11))   #卡通头像文件名编号

    reply_obj = models.MovieReply.objects.filter(movie__id=mid).order_by('-create_date')[:10]
    reply_counts = movie_obj.movie_r.all().count()
    ret['reply_counts'] = reply_counts
    ret['reply'] = reply_obj
    
    #判断是否已评过分
    if user_obj:
        has_rated = models.MovieReply.objects.filter(movie__id=mid, user__id=user_obj.id, rating__gt=0)
        has_rated_counts = has_rated.count()
        if has_rated_counts == 1:
            ret['has_rated'] = True
            ret['cur_user_rating'] = has_rated[0].rating
        elif has_rated_counts > 1:
            ret['has_rated'] = 'error'

    #收藏
    if user_obj:
        collect_obj = models.Collect_Movie.objects.filter(movie__id=mid, user__id=uid)
        if collect_obj:
            ret['collected'] = True
    
    '''
        猜你喜欢
    '''
    all_movie_obj = models.Movie.objects.exclude(id=mid)
    movie_related_obj = movie_helper.relatedMovies(movie_obj, all_movie_obj)  
    ret['related'] = movie_helper.replaceWrongImg(movie_related_obj, 'p')

    #标签云
    tags_obj = models.Movie.objects.all().order_by('-week_visit_count').values('id','ch_name','director','actor')[:50]
    da_dict, mn_list = movie_helper.tagsCloud(tags_obj, 'movie')
    ret['da_dict'] = json.dumps(da_dict)
    ret['mn_list'] = json.dumps(mn_list)
    response = render_to_response('movie/movie_detail.html', ret, context_instance=RequestContext(request))
    
    #cookie
    """
    if user_obj:
        response.set_cookie('logined', 'yes')
    else:
        response.set_cookie('logined', 'no')
    """
    return response

def movieIndex(request, *args, **kwargs):
    ret = {'logined':False, 'show':'', 'pagelist':'', 'search_ok':False, 'counts':0}
    #判断用户是否登录，获取用户信息
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    bill_obj = models.Movie.objects.all().order_by('-week_visit_count')
    billboard1 = bill_obj[0]
    billboard2 = bill_obj[1:10]
    ret['billboard1'] = billboard1
    if not path.exists(BASE_DIR+ret['billboard1'].poster):
        ret['billboard1'].poster = '/static/images/default/poster/p_200x284.png'
    ret['billboard2'] = billboard2
    for item in ret['billboard2']:
        if not path.exists(BASE_DIR+item.poster):
            item.poster = '/static/images/default/poster/p_200x284.png'
            


    '''
    内容显示及分页
    '''
    
    page = try_int(request.GET.get('p', 1), 1)
    target_focus = request.GET.get('focus','af')
    target_type = request.GET.get('type','at')
    target_region = request.GET.get('region','ar')
    
    #type
    if target_type == 'at':
        type_result = models.Movie.objects.all()
    else:
        typedict = {'juqing':'剧情', 'xiju':'喜剧', 'aiqing':'爱情', 'qihuan':'奇幻', 'guzhuang':'古装',
                'dongzuo':'动作', 'maoxian':'冒险', 'kehuan':'科幻', 'xuanyi':'悬疑', 'jingsong':'惊悚', 
                'kongbu':'恐怖', 'fanzui':'犯罪', 'zhanzheng':'战争', 'donghua':'动画', 'duanpian':'短片', 'jilupian':'纪录片',
                 'tongxing':'同性', 'qingse':'情色', 'jiating':'家庭', 'ertong':'儿童', 'lishi':'历史', 'yundong':'运动', 'zhuanji':'传记'}
        for item in typedict:
            if target_type == item:
                type_result = models.Movie.objects.filter(types__contains = typedict[item])
        if not 'type_result' in dir():
            raise Http404
                 
    #region
    if target_region == 'ar':
        region_result = type_result
        
    elif target_region == 'otherregion':
        region_result = type_result.exclude(Q(region__contains='中国大陆') |
                                                Q(region__contains='香港') |
                                                Q(region__contains='台湾') |
                                                Q(region__contains='美国') |
                                                Q(region__contains='英国') |
                                                Q(region__contains='法国') |
                                                Q(region__contains='日本') |
                                                Q(region__contains='韩国') |
                                                Q(region__contains='泰国') |
                                                Q(region__contains='印度')
                                                )     
    else:
        regiondict = {'mainland':'中国大陆', 'hongkong':'香港', 'taiwan':'台湾', 'america':'美国', 'uk':'英国',
                      'french':'法国', 'japan':'日本', 'korea':'韩国', 'thailand':'泰国', 'india':'印度'}
        
        for item in regiondict:
            if target_region == item:
                region_result = type_result.filter(region__contains = regiondict[item])

        if not 'region_result' in dir():
            raise Http404

    #focus
    today_str = getTodayStr()
    if target_focus == 'af':
        focus_result = region_result.filter(release_date__lte=today_str).order_by('-release_date')
    elif target_focus == 'guonei':
        focus_result = region_result.filter(release_date_show__contains = '中国').exclude(score=0).order_by('-release_date')
    elif target_focus == 'guowai':
        focus_result = region_result.exclude(Q(release_date_show__contains = '中国') | Q(score=0)).order_by('-release_date')
    elif target_focus == 'gaofen':
        focus_result = region_result.filter(score__gte = 8).order_by('-score')
    elif target_focus == 'gengxin':
        focus_result = region_result.all().order_by('-create_date')
    elif target_focus == 'not_released':
        focus_result = region_result.filter(release_date__gt=today_str).order_by('release_date')
    if not 'focus_result' in dir():
        raise Http404

    items_per_page = try_int(request.COOKIES.get('page_num', 20), 20)
    try:
        all_item_counts = focus_result.count()
    except Exception:
        all_item_counts = 0
    ret['counts'] = all_item_counts
        
    pageObj = html_helper.PageInfo(page, all_item_counts, items_per_page)
    
    try:
        final_result = focus_result[pageObj.start : pageObj.end]
    except Exception:
        final_result = ''
    filter_url = '/movie/?focus=' + target_focus + '&type=' + target_type + '&region=' + target_region + '&p='
    page_list = html_helper.Pager(page, pageObj.total_page_counts, filter_url)
    
    #popular
    popular_id_list = []
    popular = bill_obj[:30]
    for item in popular:
        popular_id_list.append(item.id)

    #判断图片是否存在，不存在替换为默认图片
    ret['show'] = final_result
    for item in ret['show']:
        if not path.exists(BASE_DIR+item.poster):
            item.poster = '/static/images/default/poster/p_200x284.png'
        for p in popular_id_list:
            if p == item.id:
                item.popular = True

    ret['pages'] = pageObj.total_page_counts

    if pageObj.total_page_counts == 1:
        ret['page_list'] = ''
    elif pageObj.total_page_counts == 0:
        ret['no_result'] = True
    else:
        ret['page_list'] = page_list
        
        
    '''
    *标签云
    '''
    tags_obj = models.Movie.objects.all().order_by('-week_visit_count').values('id','ch_name','director','actor')[:50]
    da_dict, mn_list = movie_helper.tagsCloud(tags_obj, 'movie')
    ret['da_dict'] = json.dumps(da_dict)
    ret['mn_list'] = json.dumps(mn_list)
    

    thumb_switch = request.COOKIES.get('switch', 't1')
    if thumb_switch == 't1':
        response = render_to_response('movie/movie_index.html', ret, context_instance=RequestContext(request))
    elif thumb_switch == 't2':
        response = render_to_response('movie/movie_index_t2.html', ret, context_instance=RequestContext(request))
    elif thumb_switch == 't3':
        response = render_to_response('movie/movie_index_t3.html', ret, context_instance=RequestContext(request))
    response.set_cookie('page_num', items_per_page) 
    return response

        
def submitReply(request):
    ret = {'logined':False}
    uid = request.session.get('login_user_id', None)
    if request.method == 'POST':
        if uid:
            ret['logined'] = True
            mid = request.POST.get('id','')
            html_content = request.POST.get('content','')
            html_content = htmlContentFilter(html_content, 'static')
            rating = try_int(request.POST.get('rating', 0),0)
            if not all([mid,html_content]):
                if not mid:
                    ret['msg'] = '302'  #条目ID未得到
                else:
                    ret['msg'] = '901'  #内容为空
                return HttpResponse(json.dumps(ret))
            else:
                if re.search('^\s+$',html_content, re.S):
                    ret['msg'] = '902'  #全为空格
                    return HttpResponse(json.dumps(ret))
            try:
                user_obj = models.User.objects.get(id=uid)
            except Exception:
                ret['msg'] = '103'  #数据库条目不存在
                return HttpResponse(json.dumps(ret))
            
            try:
                movie_obj = models.Movie.objects.get(id=mid)
                if not rating:  #分数为0
                    new_reply_obj = models.MovieReply.objects.create(content=html_content, movie=movie_obj, user=user_obj)
                else:
                    #先判断是否已评过分
                    reply_with_rating = models.MovieReply.objects.filter(user__id=uid, movie__id=mid, rating__gt=0)
                    if not reply_with_rating.count():
                        new_reply_obj = models.MovieReply.objects.create(rating=rating, content=html_content, movie=movie_obj, user=user_obj)
                    else:
                        ret['msg'] = '909'
                        return HttpResponse(json.dumps(ret))
            except Exception:
                ret['msg'] = '101'  #数据库写入错误

            ret['uid'] = user_obj.id
            ret['avatar_s'] = str(user_obj.thumb_s)
            ret['uname'] = user_obj.username
            ret['content'] = new_reply_obj.content
            ret['new_rid'] = new_reply_obj.id
            user_helper.expAdd('comment', uid)
            ret['success'] = True
            return HttpResponse(json.dumps(ret))
        #未登录
        else:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))

    else:
        raise Http404
        
        
def submitReplyReply(request):
    ret = {'logined':False, 'success':False}
    uid = request.session.get('login_user_id', None)
    if request.method == 'POST':
        if uid:
            ret['logined'] = True
            rid = request.POST.get('rid')  #目标评论ID
            html_content = request.POST.get('content','')
            html_content = htmlContentFilter(html_content, 'static')
            if not all([rid,html_content]):
                if not rid:
                    ret['msg'] = '302'  #条目ID未得到
                else:
                    ret['msg'] = '901'  #内容为空
                return HttpResponse(json.dumps(ret))
            else:
                if re.search('^\s+$',html_content, re.S):
                    ret['msg'] = '902'  #全为空格
                    return HttpResponse(json.dumps(ret))
            try:
                user_obj = models.User.objects.get(id=uid)
            except Exception:
                ret['msg'] = '103'  #数据库条目不存在
                return HttpResponse(json.dumps(ret))
            
            try:
                reply_obj = models.MovieReply.objects.get(id=rid)
                new_rr_obj = models.MovieReplyReply.objects.create(content=html_content, movie_reply=reply_obj, user=user_obj)
            except Exception:
                ret['msg'] = '101'  #数据库错误（前端发送数据有误或数据库自身错误）
                return HttpResponse(json.dumps(ret))
            
            ret['new_username'] = user_obj.username
            ret['new_uid'] = user_obj.id
            ret['new_avatar'] = str(user_obj.thumb_s)
            ret['content'] = new_rr_obj.content
            ret['rrid'] = new_rr_obj.id
            user_helper.expAdd('comment_r', uid)
            target_uid = reply_obj.user.id
            if not target_uid == uid:
                check_obj = models.User_Notification_Check.objects.filter(target_user__id=target_uid)
                if check_obj.count() == 1:
                    try:
                        #存在即更新
                        check_obj.update(movie_rr=check_obj[0].movie_rr + 1)
                    except Exception:
                        ret['msg'] = '101'
                        return HttpResponse(json.dumps(ret))
                elif check_obj.count() == 0:  #以防万一
                    try:
                        models.User_Notification_Check.objects.create(target_user=models.User.objects.filter(id=target_uid)[0], movie_rr=1)
                    except Exception:
                        ret['msg'] = '103'  #用户不存在
                        return HttpResponse(json.dumps(ret))
                else:  #重复数据
                    ret['msg'] = '102'
                    return HttpResponse(json.dumps(ret))
                ret['success'] = True
                return HttpResponse(json.dumps(ret))
        #未登录
        else:
            ret['msg'] = '107'
        return HttpResponse(json.dumps(ret))
    else:
        return HttpResponse(json.dumps(ret))
    


def replyLike(request):
    if request.method == 'POST':
        ret = {}
        uid = request.session.get('login_user_id', None)
        print uid
        if not uid:
            ret['msg'] = '401'  #用户未登录
            return HttpResponse(json.dumps(ret))
        
        rid = request.POST.get('rid','')
        print rid
        if not rid.isdigit():
            ret['msg'] = '302' #前端数据错误
            return HttpResponse(json.dumps(ret))
        
        liked_obj_counts = models.MovieReplyLike.objects.filter(user__id=uid, movie_reply_like__id=rid).count()
        if liked_obj_counts: #该用户对该评论已赞
            ret['msg'] = '910'
        else:
            try:
                user_obj = models.User.objects.get(id=uid)
            except Exception:
                ret['msg'] = '101'
                return HttpResponse(json.dumps(ret))
            reply_obj = models.MovieReply.objects.get(id=rid)
            models.MovieReplyLike.objects.create(user=user_obj, movie_reply_like=reply_obj)
            user_helper.expAdd('like', uid)  #增加经验
            ret['msg'] = 'success'

        return HttpResponse(json.dumps(ret))
    else:
        raise Http404

def getMoreReplies(request):
    if request.method == 'POST':
        ret = {}
        rid = request.POST.get('rid', None)
        remainder = request.POST.get('remainder', None)
        if not rid.isdigit() or not remainder.isdigit():
            ret['msg'] = '302'
            return HttpResponse(json.dumps(ret))
        uid = request.session.get('login_user_id', None)
        if not uid:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        
        idx = int(remainder)  #目前剩余条数
        pref = int(idx-5)  #这次取完还剩余的条数
        if pref < 0:
            pref = 0
        rr_obj = models.MovieReplyReply.objects.filter(movie_reply__id=rid).values('id','content','create_date','user_id')[pref:idx]

        res_list = [pref]
        for item in rr_obj:
            try:
                user_obj = models.User.objects.get(id=item['user_id'])
            except Exception:
                continue
            item['thumb_s'] = str(user_obj.thumb_s)
            item['username'] = str(user_obj.username)
            item['create_date'] = my_datetrans(item['create_date'])
            res_list.append(item)
        print res_list
            
        return HttpResponse(json.dumps(res_list, cls=CJsonEncoder))


    else:
        raise Http404

    
def getMoreComments(request):
    if request.method == 'POST':
        ret = {}
        xid = request.POST.get('xid')
        remainder = request.POST.get('remainder')
        if xid.isdigit() and remainder.isdigit():
            idx = int(remainder)  #目前剩余条数
            pref = int(idx-10)  #这次取完还剩余的条数
            if pref < 0:
                pref = 0
            reply_obj = models.MovieReply.objects.filter(movie__id=xid).values('id','content','create_date','user_id')[pref:idx]
            res_list = [pref]
            
            for item in reply_obj:
                try:
                    user_obj = models.User.objects.get(id=item['user_id'])
                except Exception:
                    continue
                item['thumb_s'] = str(user_obj.thumb_s)
                item['uname'] = str(user_obj.username)
                item['create_date'] = my_datetrans(item['create_date'])
                
                #获取该评论下的回复
                rr_obj = models.MovieReplyReply.objects.filter(movie_reply__id=item['id']).values('id',
                                            'content','create_date','user_id')[:5]
                rr_list = []
                for rr in rr_obj:  #获取每个回复的用户信息
                    try:
                        rr_user_obj = models.User.objects.get(id=rr['user_id'])
                    except Exception:
                        continue
                    rr['thumb_s'] = str(rr_user_obj.thumb_s)
                    rr['uname'] = str(rr_user_obj.username)
                    rr['create_date'] = my_datetrans(rr['create_date'])
                    rr_list.append(rr)
                item['rr'] = rr_list
                item['rr_counts'] = models.MovieReplyReply.objects.filter(movie_reply__id=item['id']).count()
                #评论的like
                item['like_counts'] = models.MovieReplyLike.objects.filter(movie_reply_like__id=item['id']).count()
                res_list.append(item)
            return HttpResponse(json.dumps(res_list))
        else:
            ret['msg'] = '302'
            return HttpResponse(json.dumps(ret))

    else:
        raise Http404