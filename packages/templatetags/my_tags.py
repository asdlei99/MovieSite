#_*_coding:UTF-8_*_
from __future__ import division
import datetime
import re
from django import template
from movie import models
register=template.Library()

@register.filter(expects_localtime=True, is_safe=True)
def my_datetrans(origin_date):
    cur_day = datetime.date.today()
    origin_day = origin_date.date()
    past_days = (cur_day - origin_day).days
    if 0<= past_days <= 2:
        if past_days == 0:
            prefix = ''
        elif past_days == 1: 
            prefix = '昨天 '
        else:
            prefix = '前天 '
        result = prefix + origin_date.strftime('%H:%M')
    else: #大于3天
        this_year = cur_day.year
        origin_year = origin_day.year
        if this_year == origin_year:
            result = origin_date.strftime('%m-%d %H:%M')
        else:
            result = origin_date.strftime('%Y-%m-%d %H:%M')
    return result

@register.filter
def my_boardName(s):
    d = {'notification':'通知区', 'movie':'电影专区', 'tv':'电视剧专区', 
         'anime':'动漫专区', 'show':'综艺专区', 'relaxing':'综合区', 'feedback':'意见反馈区'}  #与数据库board字段对应
    for k,v in d.items():
        if s == k:
            return v
        
@register.filter
def my_resolvePhotoUrl(url_str):
    url_list = url_str.strip().split()
    html_str = ''
    if url_list[0]:
        photo_counts = len(url_list)
        for index, url in enumerate(url_list):
            url_thumb = re.sub('(.*\/)(.*)', r'\1thumbs/\2', url)
            if photo_counts == 4 and index == 1:
                html_str += '<a class="gallery-img" style="margin-right:32%%" href="%s" data-toggle="lightbox" data-gallery="multiimages" data-parent="div.msg-img-wrap"><img class="img-responsive" src="%s" alt=""></a>'%(url,url_thumb)
            else:
                html_str += '<a class="gallery-img" href="%s" data-toggle="lightbox" data-gallery="multiimages" data-parent="div.msg-img-wrap"><img class="img-responsive" src="%s" alt=""></a>'%(url,url_thumb)
        return html_str
    else:
        return ''

@register.filter
def my_getUserLevel(user_exp):
    #经验值转等级
    levels = {1: 0, 2: 60, 3: 140, 4: 240, 5: 360, 6: 500, 7: 660, 8: 840, 9: 1040, 10: 1260, 11: 1500, 12: 1760, 13: 2040, 14: 2340, 15: 2660, 16: 3000, 17: 3360, 18: 3740, 19: 4140, 20: 4560, 21: 5000, 22: 5460, 23: 5940, 24: 6440, 25: 6960, 26: 7500, 27: 8060, 28: 8640, 29: 9240, 30: 9860, 31: 10500, 32: 11160, 33: 11840, 34: 12540, 35: 13260, 36: 14000, 37: 14760, 38: 15540, 39: 16340, 40: 17160, 41: 18000, 42: 18860, 43: 19740, 44: 20640, 45: 21560, 46: 22500, 47: 23460, 48: 24440, 49: 25440, 50: 26460, 51: 27500, 52: 28560, 53: 29640, 54: 30740, 55: 31860, 56: 33000, 57: 34160, 58: 35340, 59: 36540, 60: 37760, 61: 39000, 62: 40260, 63: 41540, 64: 42840, 65: 44160, 66: 45500, 67: 46860, 68: 48240, 69: 49640, 70: 51060, 71: 52500, 72: 53960, 73: 55440, 74: 56940, 75: 58460, 76: 60000, 77: 61560, 78: 63140, 79: 64740, 80: 66360, 81: 68000, 82: 69660, 83: 71340, 84: 73040, 85: 74760, 86: 76500, 87: 78260, 88: 80040, 89: 81840, 90: 83660, 91: 85500, 92: 87360, 93: 89240, 94: 91140, 95: 93060, 96: 95000, 97: 96960, 98: 98940, 99: 100940, 100: 102960}
    #print user_exp
    for lv,exp in levels.items():
        if user_exp >= exp:
            continue
        else:
            user_level = lv - 1
            return user_level
    return None  #超过最大经验值

@register.filter
def my_focused(uid, focused_list):
    found = False
    for item in focused_list:
        if item == uid:
            found = True
    if found:
        return True
    else:
        return False

@register.filter
def my_getPostedCounts(uid):
    post_obj = models.Post.objects.filter(user__id=uid)
    post_reply_obj = models.PostReply.objects.filter(user__id=uid)
    counts = len(post_obj) + len(post_reply_obj)
    return counts

@register.filter
def my_getFansCounts(uid):
    fans_obj = models.UserFocus.objects.filter(target_user__id=uid)
    return len(fans_obj)

@register.filter
def my_transMonthToCH(month):

    result = ''
    tmp_dict = {'01':'一月', '02':'二月', '03':'三月', '04':'四月', '05':'五月', '06':'六月',
                '07':'七月', '08':'八月','09':'九月', '10':'十月', '11':'十一月', '12':'十二月'}
    for k,v in tmp_dict.items():
        if k == month:
            result = v
            break
    return result

@register.filter
def my_removeMedia(content):
    new_content = re.sub('<img.*?>', '[图片]', content)
    new_content = re.sub(r'<iframe.*?>.*?<\/iframe>', '[视频]', new_content)
    return new_content

@register.filter
def my_getLastMsgContent(qs):
    content = qs.order_by('-create_date')[0].content
    return content

@register.filter
def my_getLastMsgReplyList(qs):
    result = qs.order_by('-create_date')[:10]
    return result

@register.filter
def my_slice(s, num):
    l = s.split('/')[:num]
    result = '/'.join(l).strip()
    return result

