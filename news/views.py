#_*_coding:UTF-8_*_
from django.shortcuts import render_to_response, Http404
from django.http.response import HttpResponse
from movie import models
#from django.utils.safestring import mark_safe
from packages import html_helper, user_helper
from packages.general import try_int, loginCheck, loginInfo
import json
#from datetime import datetime, date
from django.template.context import RequestContext
import re
from datetime import datetime, date
from packages.general import htmlContentFilter
from packages.templatetags.my_tags import my_datetrans
from packages.movie_helper import replaceWrongImg

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        #如果对象时datetime格式，序列化为所定义格式的字符串
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            #默认序列化（不能格式化datetime格式）
            return json.JSONEncoder.default(self, obj)

def newsIndex(request):
    ret = {'logined':False}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    
    ret['slider'] = models.News_Index_Slider.objects.all().order_by('-create_date')[:5]
    
    ret['recommend'] = models.News.objects.filter(recommended=True).order_by('-create_date')[:9]
    
    news_list = models.News.objects.all().order_by('-create_date')[:12]
    ret['news_list'] = news_list
    
    return render_to_response('news/news_index.html', ret, context_instance=RequestContext(request))

def getMoreNews(request):  #news index
    if request.method == 'POST':
        ret = {}
        cur_news_counts = int(request.POST.get('cur_news_counts'))
        print cur_news_counts
        news_obj = models.News.objects.all().order_by('-create_date').values('id','title','subtitle','news_image','create_date')
        ret['more_news'] = list(news_obj[cur_news_counts:cur_news_counts+12]) 
        return HttpResponse(json.dumps(ret, cls=html_helper.CJsonEncoder))
        
    else:
        raise Http404

    

def newstemplate(request, *args):
    ret = {'logined':False}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    nid = args[0]
    try:
        news_obj = models.News.objects.get(id=nid)
    except Exception:
        raise Http404
    ret['news'] = news_obj
    
    news_obj.visit_count += 1
    news_obj.day_visit_count += 1
    news_obj.week_visit_count += 1
    news_obj.save()
    
    ret['detail'] = news_obj
    
    reply_obj = models.NewsReply.objects.filter(news__id=nid).order_by('-create_date')
    reply_counts = news_obj.news_r.all().count()
    ret['reply_counts'] = reply_counts
    ret['reply'] = reply_obj
    

    '''
    文章分页部分
    '''
    #page = try_int(page, 1)
    #news_content = news_obj.news_content
    #ret['news_content'] = news_content 
    ret['keywords'] = news_obj.keywords.split()
    keywords_a = []
    for keyword in ret['keywords']:
        keywords_a.append('<a href="/tags/?n='+keyword+'">'+keyword+'</a>')
        #keywords_a.append(keyword)
    ret['keywords_a'] = keywords_a
    
    
    #找出相关电影/电视剧链接
    temp_list = []
    rel_links =  re.findall(r'<a.*?href=[\'\"](/\w+/\d+/)[\'\""].*?>[^/].*?</a>', news_obj.news_content)
    for item in rel_links:
        temp_list.append(item)
    rel_link_set = set(temp_list)  #相关电影电视剧链接列表
    rel_link_list = []
    for item in rel_link_set:
        res = re.findall(r'^/(\w+)/(\d+)/', item)[0]  #拿出每个链接中的两部分
        item_category = res[0]
        item_id = res[1]
        if item_category == 'movie':
            try:
                item_obj = models.Movie.objects.filter(id=item_id)  #得到相关电影model对象
                item_obj = replaceWrongImg(item_obj, img_type='p')[0]
                item_obj.link = item
 
                item_obj.director = item_obj.director.split('/')[0].strip()
                item_obj.actor = item_obj.actor.split('/')[0].strip()
                rel_link_list.append(item_obj)
            except Exception:
                pass
            
        elif item_category == 'tv':
            try:
                item_obj = models.Tv.objects.filter(id=item_id)  #得到相关电影model对象
                item_obj = replaceWrongImg(item_obj, img_type='p')[0]
                item_obj.link = item
                item_obj.director = item_obj.director.split('/')[0].strip()
                item_obj.actor = item_obj.actor.split('/')[0].strip()
                rel_link_list.append(item_obj)
            except Exception:
                pass

    
    ret['rel_link_list'] = rel_link_list

    if news_obj.title_bg:
        return render_to_response('news/news_template_zhuanti.html', ret, context_instance=RequestContext(request))
    elif news_obj.ga_content:
        return render_to_response('news/news_template_ga.html', ret, context_instance=RequestContext(request))
    else:
        return render_to_response('news/news_template.html', ret, context_instance=RequestContext(request))

def submitReply(request):
    ret = {'logined':False, 'success':False}
    uid = request.session.get('login_user_id', None)
    if request.method == 'POST':
        if uid:
            ret['logined'] = True
            nid = request.POST.get('id','')
            content = request.POST.get('content','')
            html_content = htmlContentFilter(content, 'static')
            if not all([nid,html_content]):
                if not nid:
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
                news_obj = models.News.objects.get(id=nid)
                new_reply_obj = models.NewsReply.objects.create(content=html_content, news=news_obj, user=user_obj)
               
                ret['uid'] = user_obj.id
                ret['avatar_s'] = str(user_obj.thumb_s)
                ret['uname'] = user_obj.username
                ret['new_rid'] = new_reply_obj.id
                ret['content'] = new_reply_obj.content
                user_helper.expAdd('comment', uid)
                ret['success'] = True
            except Exception:
                ret['msg'] = '101'  #数据库写入错误
                return HttpResponse(json.dumps(ret))

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
            rid = request.POST.get('rid', None)  #目标评论ID
            content = request.POST.get('content')
            content = re.sub(r'<[^i].*?>', '', content); #过滤HTML标签，保留i开头的
            if not all([rid,content]):
                if not rid:
                    ret['msg'] = '302'  #条目ID未得到
                else:
                    ret['msg'] = '901'  #内容为空
                return HttpResponse(json.dumps(ret))
            else:
                if re.search('^\s+$',content, re.S):
                    ret['msg'] = '902'  #全为空格
                    return HttpResponse(json.dumps(ret))
            try:
                user_obj = models.User.objects.get(id=uid)
            except Exception:
                ret['msg'] = '103'  #数据库条目不存在
                return HttpResponse(json.dumps(ret))
            try:
                ret['new_username'] = user_obj.username  #前端动态添加评论
                ret['new_uid'] = user_obj.id
                ret['new_avatar'] = str(user_obj.thumb_s)
                reply_obj = models.NewsReply.objects.get(id=rid)
                new_rr_obj = models.NewsReplyReply.objects.create(content=content, news_reply=reply_obj, user=user_obj)
                ret['content'] = new_rr_obj.content
                ret['rrid'] = new_rr_obj.id
                user_helper.expAdd('comment_r', uid)
                ret['success'] = True
                return HttpResponse(json.dumps(ret))
            except Exception:
                ret['msg'] = '101'  #数据库错误（前端发送数据有误或数据库自身错误）
                return HttpResponse(json.dumps(ret))

        #未登录
        else:
            ret['msg'] = '401'
        return HttpResponse(json.dumps(ret))
    else:
        return HttpResponse(json.dumps(ret))
    


def replyLike(request):
    if request.method == 'POST':
        ret = {}
        uid = request.session.get('login_user_id', None)
        if not uid:
            ret['msg'] = '401'  #用户未登录
            return HttpResponse(json.dumps(ret))
        rid = request.POST.get('rid','')
        if not rid.isdigit():
            ret['msg'] = '302' #前端数据错误
            return HttpResponse(json.dumps(ret))
        
        liked_obj_counts = models.NewsReplyLike.objects.filter(user__id=uid, news_reply_like__id=rid).count()
        if liked_obj_counts: #该用户对该评论已赞
            ret['msg'] = '910'
        else:
            try:
                user_obj = models.User.objects.get(id=uid)
            except Exception:
                ret['msg'] = '101'
                return HttpResponse(json.dumps(ret))
            reply_obj = models.NewsReply.objects.get(id=rid)
            models.NewsReplyLike.objects.create(user=user_obj, news_reply_like=reply_obj)
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
        rr_obj = models.NewsReplyReply.objects.filter(news_reply__id=rid).values('id','content','create_date','user_id')[pref:idx]

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
        nid = request.POST.get('nid')
        remainder = request.POST.get('remainder')
        if nid.isdigit() and remainder.isdigit():
            idx = int(remainder)  #目前剩余条数
            pref = int(idx-10)  #这次取完还剩余的条数
            if pref < 0:
                pref = 0
            reply_obj = models.NewsReply.objects.filter(news__id=nid).values('id','content','create_date','user_id')[pref:idx]
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
                rr_obj = models.NewsReplyReply.objects.filter(news_reply__id=item['id']).values('id',
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
                item['rr_counts'] = models.NewsReplyReply.objects.filter(news_reply__id=item['id']).count()
                #评论的like
                item['like_counts'] = models.NewsReplyLike.objects.filter(news_reply_like__id=item['id']).count()
                res_list.append(item)
                
            return HttpResponse(json.dumps(res_list))
        else:
            ret['msg'] = '302'
            return HttpResponse(json.dumps(ret))

    else:
        raise Http404
