#_*_coding:UTF-8_*_
from collections import Counter
from random import randint, sample
from MovieSite.settings import BASE_DIR
from os import path

def tagsCloud(tags_obj, cate):
    da_list = [] #导演演员列表
    for tag in tags_obj:
        director_str = tag['director']
        actor_str = tag['actor']
        if director_str:
            tmp_list = director_str.split('/')
            for d in tmp_list:
                da_list.append(d.strip())
        if actor_str:
            tmp_list = actor_str.split('/')
            for a in tmp_list:
                da_list.append(a.strip())      
    c = Counter(da_list)
    tmp_l = c.most_common(8)
    da_dict = {}
    for item in tmp_l:
        da_dict[item[0]] = item[1]
    
    mn_list = []  #电影名等的列表
    m1_5 = sample(tags_obj[:5],3)
    m6_15 = sample(tags_obj[6:15],4)
    m16_30 = sample(tags_obj[16:30],5)
    m31_50 = sample(tags_obj[31:50],10)
    for item in m1_5:
        tmp_d = {}
        tmp_d['text'] = item['ch_name']
        tmp_d['weight'] = randint(8,10)
        tmp_d['link'] = '/%s/'%cate + str(item['id']) + '/'
        tmp_d['html'] = {'title':item['ch_name']}
        mn_list.append(tmp_d)
    for item in m6_15:
        tmp_d = {}
        tmp_d['text'] = item['ch_name']
        tmp_d['weight'] = randint(5,7)
        tmp_d['link'] = '/%s/'%cate + str(item['id']) + '/'
        tmp_d['html'] = {'title':item['ch_name']}
        mn_list.append(tmp_d)
    for item in m16_30:
        tmp_d = {}
        tmp_d['text'] = item['ch_name']
        tmp_d['weight'] = 4
        tmp_d['link'] = '/%s/'%cate + str(item['id']) + '/'
        tmp_d['html'] = {'title':item['ch_name']}
        mn_list.append(tmp_d)
    for item in m31_50:
        tmp_d = {}
        tmp_d['text'] = item['ch_name']
        tmp_d['weight'] = randint(1,3)
        tmp_d['link'] = '/%s/'%cate + str(item['id']) + '/'
        tmp_d['html'] = {'title':item['ch_name']}
        mn_list.append(tmp_d)
    return da_dict, mn_list

def relatedMovies(obj, all_obj):
    typestr = obj.types
    type_list = typestr.split('/')
    region_str = obj.region
    region_list = region_str.split('/')

    related_obj = all_obj
    for item in type_list:
        type_item = item.strip()
        related_temp_obj = related_obj.filter(types__contains=type_item)
        if related_temp_obj.count() > 6:  #大于6个结果时才继续
            related_obj = related_temp_obj
            continue
        else:
            break
    for item in region_list:
        region_item = item.strip()
        related_temp_obj = related_obj.filter(region__contains=region_item)
        if related_temp_obj.count() > 6:
            related_obj = related_temp_obj
            continue
        else:
            break
    
    related_obj = related_obj.order_by('-release_date')
    related_counts = related_obj.count()
    step = related_counts - 6
    num = randint(0,step)  #随机挑选
    related_obj = related_obj[num:num+6]
    return related_obj

def replaceWrongImg(obj, img_type='ps'):  #ps: poster, screenshoot
    for item in obj:
        if img_type == 'ps' or img_type == 'p':
            if item.poster:
                if not path.exists(BASE_DIR + item.poster):
                    item.poster = '/static/images/default/poster/p_200x284.png'
        if img_type == 'ps':
            if item.ss1:
                if not path.exists(BASE_DIR + item.ss1):
                    item.ss1 = ''
            if item.ss2:
                if not path.exists(BASE_DIR + item.ss2):
                    item.ss2 = ''
            if item.ss3:
                if not path.exists(BASE_DIR + item.ss3):
                    item.ss3 = ''
            if item.ss4:
                if not path.exists(BASE_DIR + item.ss4):
                    item.ss4 = ''
    return obj
 

    