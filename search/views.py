#coding:UTF-8
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.db.models import Q
import json
from movie import models
from packages import movie_helper, general, html_helper
import sys
from os import path
from MovieSite.settings import BASE_DIR
from itertools import chain
from operator import attrgetter
from random import sample, shuffle
#import jieba
import jieba.analyse
jieba.load_userdict('D:\Python27\Lib\site-packages\jieba\my_dict.txt')
from collections import Counter
from django.core.exceptions import ObjectDoesNotExist
reload(sys)
sys.setdefaultencoding('utf8')
# Search related views.

typedict = {'juqing':'剧情', 'xiju':'喜剧', 'aiqing':'爱情', 'qihuan':'奇幻', 'guzhuang':'古装',
            'dongzuo':'动作', 'maoxian':'冒险', 'kehuan':'科幻', 'xuanyi':'悬疑', 'jingsong':'惊悚', 
            'kongbu':'恐怖', 'fanzui':'犯罪', 'zhanzheng':'战争', 'donghua':'动画', 'jilupian':'纪录片',
            'tongxing':'同性', 'qingse':'情色', 'jiating':'家庭', 'ertong':'儿童', 'lishi':'历史', 'yundong':'运动',
            'zhuanji':'传记', 'yinyue':'音乐', 'gewu':'歌舞', 'xiqu':'戏曲'}


def searchIndex(request):
    ret = {}
    s_movie = models.Movie.objects.all().order_by('-week_visit_count')[:10]
    s_tv = models.Tv.objects.all().order_by('-week_visit_count')[:10]
    s_anime = models.Anime.objects.all().order_by('-week_visit_count')[:10]
    s_show = models.Anime.objects.all().order_by('-week_visit_count')[:10]
    final_set = sorted(chain(s_movie, s_tv, s_anime, s_show),key=attrgetter('week_visit_count'), reverse=True)
    #热门标签
    movie_top = models.Movie.objects.all().order_by('-week_visit_count')[:40]
    types_list = [t.strip() for item in movie_top for t in item.types.split('/') if t]
    ct = Counter(types_list)
    del ct[u'剧情']
    common_types = ct.most_common(6)
    hot_tags = []
    color_list = ['blue','yellow','purple','orange','gray','red','green']
    for t in common_types:
        type_name = t[0]
        for k,v in typedict.items():
            if v == type_name:
                type_url = '/movie/?type=%s'%k
                hot_tags.append({'name':type_name, 'url':type_url, 'color':sample(color_list,1)[0]})
    
    actor_list = [a.strip() for item in final_set for a in item.actor.split('/') if a]
    ca = Counter(actor_list)
    common_actors = ca.most_common(6)
    for actor in common_actors:
        actor_name = actor[0]
        actor_url = '/search/result/?keyword=%s' %actor_name
        hot_tags.append({'name':actor_name, 'url':actor_url, 'color':sample(color_list,1)[0]})

    name_list = [item for item in final_set[:20]]
    for item in name_list:
        name_name = item.ch_name
        name_url = '/%s/%s/' %(item.cate, item.id)
        hot_tags.append({'name':name_name, 'url':name_url, 'color':sample(color_list,1)[0]})
    
    hot_tags.append({'name':'豆瓣高分', 'url':'/movie/?focus=gaofen', 'color':sample(color_list,1)[0]})
    hot_tags.append({'name':'韩剧', 'url':'/tv/?region=korea', 'color':sample(color_list,1)[0]})
    hot_tags.append({'name':'美剧', 'url':'/tv/?region=america', 'color':sample(color_list,1)[0]})
    shuffle(hot_tags)
    ret['hot_tags'] = hot_tags
    
    ret['search_recommend'] = list(final_set)[:5]
    for item in ret['search_recommend']:
        item.url = '/%s/%s/' %(item.cate, item.id)

        if not path.exists(BASE_DIR+item.poster):
            item.poster = '/static/images/default/poster/p_200x284.png'

    return render_to_response('search/search_index.html', ret, context_instance=RequestContext(request))

# run this function when search input value is changed.
def valueChange(request):
    try:
        sv_str = request.POST.get('sv').strip()
        #关键词拆分
        """
        "搜索包括：电影名，外文名，又名，演员，导演。
        "返回的json中，类型按电影>电视剧>...>顺序排列
        """
        if sv_str:
            #过滤特殊字符
            illegal_chars = ['!','！','@','#','$','%','^','&','*','-','_','"',"'",':','：','·',
                             '+','=','~','`','|','\\','/',',','，','.','。','?','？',
                             '(',')','<','>','{','}','[',']','【','】',' ']  #空格也去掉
            for item in illegal_chars:
                if item in sv_str:
                    sv_str = sv_str.replace(item, '')
            if not sv_str:
                ret = {'illegal':True}
                return HttpResponse(json.dumps(ret))
    
            #去掉所有特殊字符后用jieba分词
            sv_list_filtered = jieba.lcut(sv_str)
            try:
                key_word = jieba.analyse.extract_tags(sv_str, topK=1)[0]
            except IndexError:
                key_word = ''
            if sv_list_filtered:
                #print 'sv_list_f:' + str(sv_list_filtered)
                all_list = []  #查询到的结果结合
                for item in sv_list_filtered:
                    movie_set = models.Movie.objects.filter(Q(ch_name__contains = item) |
                                                    Q(foreign_name__contains = item) |
                                                    Q(other_name__contains = item))
                    if movie_set:
                        all_list.extend(movie_set)
                    tv_set = models.Tv.objects.filter(Q(ch_name__contains = item) |
                                                    Q(foreign_name__contains = item) |
                                                    Q(other_name__contains = item))
                    if tv_set:
                        all_list.extend(tv_set)
                    anime_set = models.Anime.objects.filter(Q(ch_name__contains = item) |
                                                    Q(foreign_name__contains = item) |
                                                    Q(other_name__contains = item))
                    if anime_set:
                        all_list.extend(anime_set)
                    show_set = models.Show.objects.filter(Q(ch_name__contains = item) |
                                                    Q(foreign_name__contains = item) |
                                                    Q(other_name__contains = item))
                    if show_set:
                        all_list.extend(show_set)
    
                c = Counter(all_list)
    
                if key_word:
                    sorted_list = sorted(c.items(), key=lambda x: (-(key_word == x[0].ch_name), -x[1], -(key_word in x[0].ch_name)))[:6]
                else:
                    sorted_list = sorted(c.items(), key=lambda x: ((sv_list_filtered[0] == x[0].ch_name), x[1], sv_list_filtered[0] in x[0].ch_name), reverse=True)[:6]
                
                truncated_list = [x[0] for x in sorted_list]
                final_list = []
                for item in truncated_list:
                    item.url = '/%s/%s/' %(item.cate, item.id)
                    if not path.exists(BASE_DIR+item.poster):
                        item.poster = '/static/images/default/poster/p_200x284.png'
                    try:
                        eps = item.eps
                    except Exception:
                        eps = ''
                    final_list.append({'id':item.id, 'ch_name':item.ch_name, 'year':item.year,'url':item.url,
                                    'foreign_name':item.foreign_name, 'poster':item.poster, 'cate':item.cate, 'eps':eps})
    
                final_list = json.dumps(final_list, cls=general.CJsonEncoder)
                return HttpResponse(final_list)
    
        
            else: #无搜索词
                ret = {'illegal':True}
                return HttpResponse(json.dumps(ret))
        else:
            ret = {'illegal':True}
            return HttpResponse(json.dumps(ret))
    except Exception,e:
        print e


def searchResult(request, *args, **kwargs):
    ret = {'logined':False, 'show':'', 'pagelist':'', 'search_ok':False}
    #判断用户是否登录，获取用户信息
    ret, user_obj = general.loginInfo(request, ret)
    ret['user_info'] = user_obj

    '''
    内容显示及分页
    '''
    
    page = general.try_int(request.GET.get('p', 1), 1)
    u_focus = request.GET.get('focus','af')
    u_type = request.GET.get('type','at')
    u_region = request.GET.get('region','ar')
    u_category = request.GET.get('category','all')

    type_list = ['at','juqing', 'xiju', 'aiqing', 'qihuan', 'guzhuang','dongzuo', 'maoxian', 'kehuan', 'xuanyi', 'jingsong', 
            'kongbu', 'fanzui', 'zhanzheng', 'donghua', 'jilupian','tongxing', 'qingse', 'jiating', 'ertong', 'lishi', 'yundong',
            'zhuanji', 'yinyue', 'gewu', 'xiqu']
    region_list = ['ar','otherregion','mainland', 'hongkong', 'taiwan', 'america', 'uk', 'french', 'japan', 'korea', 'thailand', 'india']
    focus_list = ['af','guonei','guowai','gaofen','gengxin','not_released']
    category_list = ['all','movie','tv','anime','show']

    
    if not all([u_focus in focus_list, u_type in type_list, u_region in region_list, u_category in category_list]):
        raise Http404
    
    u_sv_str = request.GET.get('keyword', '').strip()
    if not u_sv_str:
        return HttpResponseRedirect('/search/')
    
    #type filter
    if u_type == 'at':
        movie_result = models.Movie.objects.all()
        tv_result = models.Tv.objects.all()
        anime_result = models.Anime.objects.all()
        show_result = models.Show.objects.all()
    else:
        #type_query = False
        for item in typedict:
            if u_type == item:
                movie_result = models.Movie.objects.filter(types__contains = typedict[item])
                tv_result = models.Tv.objects.filter(types__contains = typedict[item])
                anime_result = models.Anime.objects.filter(types__contains = typedict[item])
                show_result = models.Show.objects.filter(types__contains = typedict[item])
                #type_query = True
        #if not type_query:
            #raise Http404
    
    #region filter
    if u_region == 'ar':
        pass
    elif u_region == 'otherregion':
        movie_result = movie_result.exclude(Q(region__contains='中国大陆')|Q(region__contains='香港')|Q(region__contains='台湾')|Q(region__contains='美国')|Q(region__contains='英国')|Q(region__contains='法国')|Q(region__contains='日本')|Q(region__contains='韩国')|Q(region__contains='泰国')|Q(region__contains='印度'))
        tv_result = tv_result.exclude(Q(region__contains='中国大陆')|Q(region__contains='香港')|Q(region__contains='台湾')|Q(region__contains='美国')|Q(region__contains='英国')|Q(region__contains='法国')|Q(region__contains='日本')|Q(region__contains='韩国')|Q(region__contains='泰国')|Q(region__contains='印度'))
        anime_result = anime_result.exclude(Q(region__contains='中国大陆')|Q(region__contains='香港')|Q(region__contains='台湾')|Q(region__contains='美国')|Q(region__contains='英国')|Q(region__contains='法国')|Q(region__contains='日本')|Q(region__contains='韩国')|Q(region__contains='泰国')|Q(region__contains='印度'))
        show_result = show_result.exclude(Q(region__contains='中国大陆')|Q(region__contains='香港')|Q(region__contains='台湾')|Q(region__contains='美国')|Q(region__contains='英国')|Q(region__contains='法国')|Q(region__contains='日本')|Q(region__contains='韩国')|Q(region__contains='泰国')|Q(region__contains='印度'))
    else:
        regiondict = {'mainland':'中国大陆', 'hongkong':'香港', 'taiwan':'台湾', 'america':'美国', 'uk':'英国',
                'french':'法国', 'japan':'日本', 'korea':'韩国', 'thailand':'泰国', 'india':'印度'}
        #region_query = False
        for item in regiondict:
            if u_region == item:
                movie_result = movie_result.filter(region__contains = regiondict[item])
                tv_result = tv_result.filter(region__contains = regiondict[item])
                anime_result = anime_result.filter(region__contains = regiondict[item])
                show_result = show_result.filter(region__contains = regiondict[item])
                #region_query = True

        #if not region_query:
            #raise Http404

    #focus filter
    if u_focus == 'af':
        pass
    elif u_focus == 'guonei':
        movie_result = movie_result.filter(release_date_show__contains = '中国').exclude(score=0)
        tv_result = tv_result.filter(release_date_show__contains = '中国').exclude(score=0)
        anime_result = anime_result.filter(release_date_show__contains = '中国').exclude(score=0)
        show_result = show_result.filter(release_date_show__contains = '中国').exclude(score=0)
    elif u_focus == 'guowai':
        movie_result = movie_result.exclude(Q(release_date_show__contains = '中国') | Q(score=0))
        tv_result = tv_result.exclude(Q(release_date_show__contains = '中国') | Q(score=0))
        anime_result = anime_result.exclude(Q(release_date_show__contains = '中国') | Q(score=0))
        show_result = show_result.exclude(Q(release_date_show__contains = '中国') | Q(score=0))
    elif u_focus == 'gaofen':
        movie_result = movie_result.filter(score__gte = 8)
        tv_result = tv_result.filter(score__gte = 8)
        anime_result = anime_result.filter(score__gte = 8)
        show_result = show_result.filter(score__gte = 8)
    elif u_focus == 'gengxin':
        pass  #后面排序
    elif u_focus == 'not_released':
        movie_result = movie_result.filter(score=0)
        tv_result = tv_result.filter(score=0)
        anime_result = anime_result.filter(score=0)
        show_result = show_result.filter(score=0)
    #else:
        #raise Http404
            
    #keywords
    print 'u_sv_str: ' + u_sv_str
    if u_sv_str:
        sv_str = u_sv_str  #待处理
        #u_sv_list = u_sv_str.split()  #需返回给前端
        illegal_chars = ['!','！','@','#','$','%','^','&','*','-','_','"',"'",':','：','·',
                         '+','=','~','`','|','\\','/',',','，','.','。','?','？',
                         '(',')','<','>','{','}','[',']','【','】',' ']  #空格也去掉
        for item in illegal_chars:
            if item in sv_str:
                sv_str = sv_str.replace(item, '')
        print 'sv_str: ' + sv_str
        try:
            key_word = jieba.analyse.extract_tags(sv_str, topK=1)[0]
        except IndexError:
            key_word = ''

        #去掉所有特殊字符后用jieba分词
        sv_list_filtered = jieba.lcut(sv_str)
        print 'sv_list_filtered: ' + str(sv_list_filtered)
        all_list = []  #查询到的结果结合（含重复项）
        m_list,t_list,a_list,s_list = [],[],[],[]
        # 求并集
        for item in sv_list_filtered:

            temp_m = movie_result.filter(Q(ch_name__contains=item) | Q(actor__contains=item) |Q(director__contains=item) |Q(other_name__contains=item) |Q(foreign_name__contains=item))
            if temp_m:
                m_list.extend(temp_m)
            temp_t = tv_result.filter(Q(ch_name__contains=item) | Q(actor__contains=item) |Q(director__contains=item) |Q(other_name__contains=item) |Q(foreign_name__contains=item))
            if temp_t:
                t_list.extend(temp_t)
            temp_a = anime_result.filter(Q(ch_name__contains=item) | Q(actor__contains=item) |Q(director__contains=item) |Q(other_name__contains=item) |Q(foreign_name__contains=item))
            if temp_a:
                a_list.extend(temp_a)
            temp_s = show_result.filter(Q(ch_name__contains=item) | Q(actor__contains=item) |Q(director__contains=item) |Q(other_name__contains=item) |Q(foreign_name__contains=item))
            if temp_s:
                s_list.extend(temp_s)
        if u_category == 'all':
            all_list = m_list + t_list + a_list + s_list
        elif u_category == 'movie':
            all_list = m_list
        elif u_category == 'tv':
            all_list = t_list
        elif u_category == 'anime':
            all_list = a_list
        elif u_category == 'show':
            all_list = s_list
        

        # 统计（去重）
        c = Counter(all_list)
        #print c
        #print 'dict_c:'+ str(c.items())
          
        # 数量
        m_counts = len(set(m_list))
        t_counts = len(set(t_list))
        a_counts = len(set(a_list))
        s_counts = len(set(s_list))
        ret['movie_counts'] = m_counts
        ret['tv_counts'] = t_counts
        ret['anime_counts'] = a_counts
        ret['show_counts'] = s_counts
        ret['all_counts'] = sum([m_counts, t_counts, a_counts, s_counts])

        print ret['all_counts']
        
        #排序
        if key_word:
            sorted_all_list = sorted(c.items(), key=lambda x: (-(key_word == x[0].ch_name), -x[1], -(key_word in x[0].ch_name)))
        else:
            sorted_all_list = sorted(c.items(), key=lambda x: ((sv_list_filtered[0] == x[0].ch_name), x[1], sv_list_filtered[0] in x[0].ch_name), reverse=True)
        print 'sorted_all_list:' + str(sorted_all_list)

        #分页
        items_per_page = general.try_int(request.COOKIES.get('page_num', 20), 20)
        pageObj = html_helper.PageInfo(page, len(c), items_per_page)
        try:
            paged_sorted_list = sorted_all_list[pageObj.start : pageObj.end]
        except IndexError:
            paged_sorted_list = []
        print 'paged_sorted_list: ' + str(paged_sorted_list)
        #print 'paged_sorted_list:' + str(paged_sorted_list)
        final_list = [x[0] for x in paged_sorted_list]
        print len(final_list)
        # 替换不存在海报
        #print 'final_list:' + str(final_list)
        for item in final_list:
            if not path.exists(BASE_DIR+item.poster):
                item.poster = '/static/images/default/poster/p_200x284.png'
        filter_url = '/search/result/?category=%s&focus=%s&type=%s&region=%s&keyword=%s&p='%(u_category,u_focus,u_type,u_region,u_sv_str)  #r_cate为返回分类名，默认为movie（若movie搜索不为空）
        page_list = html_helper.Pager(page, pageObj.total_page_counts, filter_url)
        if pageObj.total_page_counts == 1:
            ret['page_list'] = ''
        else:
            ret['page_list'] = page_list
        # 最终结果
        ret['show'] = final_list
        ret['pages'] = pageObj.total_page_counts
        if pageObj.total_page_counts == 1:
            ret['page_list'] = ''
        elif pageObj.total_page_counts == 0:
            ret['no_result'] = True
        else:
            ret['page_list'] = page_list
    

    # 推荐电影，根据搜索结果的类型&地区来推荐
    r_count = 5 #推荐显示个数
    if final_list:
        t_list = []
        r_list = []
        for item in final_list:
            for t in item.types.split('/'):
                t_list.append(t.strip())
            for r in item.region.split('/'):
                r_list.append(r.strip())
        ct = Counter(t_list)
        del ct[u'剧情']  #去掉剧情，╮(╯_╰)╭
        cr = Counter(r_list)
        common_t = ct.most_common(1)[0][0]
        common_r = cr.most_common(1)[0][0]
        if u_category == 'all':
            rec_movie = models.Movie.objects.filter(types__contains=common_t, region__contains=common_r, score__gt=7)
            rec_tv = models.Tv.objects.filter(types__contains=common_t, region__contains=common_r, score__gt=7)
            rec_aniem = models.Anime.objects.filter(types__contains=common_t, region__contains=common_r, score__gt=7)
            rec_show = models.Show.objects.filter(types__contains=common_t, region__contains=common_r, score__gt=7)
            temp_list = [rec_movie, rec_tv, rec_aniem, rec_show]
            rec_list = [x for j in temp_list for x in j if j]
            rec_result = sorted(rec_list, key=attrgetter('release_date'), reverse=True)[:r_count]
        elif u_category == 'movie':
            rec_result = models.Movie.objects.filter(types__contains=common_t, region__contains=common_r, score__gt=7).order_by('-release_date')[:r_count]
        elif u_category == 'tv':
            rec_result = models.Tv.objects.filter(types__contains=common_t, region__contains=common_r, score__gt=7).order_by('-release_date')[:r_count]
        elif u_category == 'anime':
            rec_result = models.Anime.objects.filter(types__contains=common_t, region__contains=common_r, score__gt=7).order_by('-release_date')[:r_count]
        elif u_category == 'show':
            rec_result = models.Show.objects.filter(types__contains=common_t, region__contains=common_r, score__gt=7).order_by('-release_date')[:r_count]
        ret['rec_result'] = movie_helper.replaceWrongImg(rec_result, img_type='p')
    else:  #若搜索无结果，从推荐表里取
        rec_res = models.Movie_Recommend.objects.all().order_by('-create_date')
        rec_list = []
        for item in rec_res:
            if item.cate == 1:
                try:
                    m_obj = models.Movie.objects.get(id=item.media_id)
                    rec_list.append(m_obj)
                except ObjectDoesNotExist:
                    pass
            elif item.cate == 2:
                try:
                    m_obj = models.Tv.objects.get(id=item.media_id)
                    rec_list.append(m_obj)
                except ObjectDoesNotExist:
                    pass
            elif item.cate == 3:
                try:
                    m_obj = models.Anime.objects.get(id=item.media_id)
                    rec_list.append(m_obj)
                except ObjectDoesNotExist:
                    pass
            elif item.cate == 4:
                try:
                    m_obj = models.Show.objects.get(id=item.media_id)
                    rec_list.append(m_obj)
                except ObjectDoesNotExist:
                    pass
            if len(rec_list) == r_count:
                break
        ret['rec_result'] = rec_list
        
    # 用户选择分类的中文
    cate_dict = {'movie':'电影','tv':'电视剧','anime':'动漫','show':'综艺'}
    for k,v in cate_dict.items():
        if k == u_category:
            ret['cate_name'] = v
            
    r_base_url = '/search/result/?category=%s&focus=%s&type=%s&region=%s&keyword='%(u_category,u_focus,u_type,u_region)
    ret['cur_url'] = r_base_url + u_sv_str
    ret['u_sv_str'] = u_sv_str
    thumb_switch = request.COOKIES.get('switch', 't1')

    if thumb_switch == 't1' or not thumb_switch:
        response = render_to_response('search/search_result.html', ret, context_instance=RequestContext(request))
    elif thumb_switch == 't2':
        response = render_to_response('search/search_result_t2.html', ret, context_instance=RequestContext(request))
    elif thumb_switch == 't3':
        response = render_to_response('search/search_result_t3.html', ret, context_instance=RequestContext(request))
        
    response.set_cookie('page_num', items_per_page) 
    return response
