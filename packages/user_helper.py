#_*_coding:UTF-8_*_
from __future__ import division
from movie import models
import re
from itertools import chain
from operator import attrgetter
from datetime import datetime
from random import sample

max_exp_aday = 100
levels = {1: 0, 2: 60, 3: 140, 4: 240, 5: 360, 6: 500, 7: 660, 8: 840, 9: 1040, 10: 1260, 11: 1500, 12: 1760, 13: 2040, 14: 2340, 15: 2660, 16: 3000, 17: 3360, 18: 3740, 19: 4140, 20: 4560, 21: 5000, 22: 5460, 23: 5940, 24: 6440, 25: 6960, 26: 7500, 27: 8060, 28: 8640, 29: 9240, 30: 9860, 31: 10500, 32: 11160, 33: 11840, 34: 12540, 35: 13260, 36: 14000, 37: 14760, 38: 15540, 39: 16340, 40: 17160, 41: 18000, 42: 18860, 43: 19740, 44: 20640, 45: 21560, 46: 22500, 47: 23460, 48: 24440, 49: 25440, 50: 26460, 51: 27500, 52: 28560, 53: 29640, 54: 30740, 55: 31860, 56: 33000, 57: 34160, 58: 35340, 59: 36540, 60: 37760, 61: 39000, 62: 40260, 63: 41540, 64: 42840, 65: 44160, 66: 45500, 67: 46860, 68: 48240, 69: 49640, 70: 51060, 71: 52500, 72: 53960, 73: 55440, 74: 56940, 75: 58460, 76: 60000, 77: 61560, 78: 63140, 79: 64740, 80: 66360, 81: 68000, 82: 69660, 83: 71340, 84: 73040, 85: 74760, 86: 76500, 87: 78260, 88: 80040, 89: 81840, 90: 83660, 91: 85500, 92: 87360, 93: 89240, 94: 91140, 95: 93060, 96: 95000, 97: 96960, 98: 98940, 99: 100940, 100: 102960}

def expAdd(user_action, uid):
    #，，，，
    actions = {'speak':10, #说说，
               'speak_reply':5, #说说回复
               'comment':10, #影片评论
               'like':2, #评论点赞
               'comment_r':5, #评论回复
               'post':10, #发帖
               'post_reply':5, #回帖
               'post_layer_reply':5 #楼层回复
               }
    user_obj = models.User.objects.filter(id=uid)
    for action, weight in actions.items():
        if action == user_action:
            total_exp = user_obj[0].exp
            today_exp = user_obj[0].today_exp
            if today_exp == max_exp_aday: #经验已满
                pass
            else:  #经验未满
                if today_exp <= max_exp_aday - weight:  #本次增加经验不会超出
                    new_today_exp = today_exp + weight
                    new_total_exp = total_exp + weight
                else:  #增加后经验会超出max
                    actual_add = max_exp_aday - today_exp
                    new_today_exp = max_exp_aday
                    new_total_exp = total_exp + actual_add
                user_obj.update(today_exp=new_today_exp, exp=new_total_exp)
            break


        
def getUserLevel(user_exp):
    #exp_obj = models.UserExp.objects.filter(user=user_obj)
    #user_exp = exp_obj.exp_total
    for lv,exp in levels.items():
        if user_exp >= exp:
            continue
        else:
            user_level = lv - 1
            return user_level
    return None  #超过最大经验值
        
def getUserExpPercent(level, total_exp):
    dval = levels[level+1] - levels[level]  #当前等级共需要经验值
    beyond_level_exp = total_exp - levels[level] #总经验值超出当前等级起始经验值多少
    l_percent = (beyond_level_exp / dval)*100
    return l_percent
        
def genRandomToken(randomlength=24):
    import random
    token = ''
    chars = '0123456789_AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789_'
    random_length=randomlength
    for i in range(random_length):
        token += random.choice(chars)
    return token

def verifyEmailPat(email):
    email_pat = '^[a-zA-Z0-9_-]+\@{1}[a-zA-Z0-9_-]+\.{1}[a-zA-Z0-9]{2,4}$'
    if re.search(email_pat, email):
        return True
    else:
        return False

#只判断密码格式与正确性
def verifyPassPat(password, password_confirm, ret):
    space_match = re.search('\s', password)
    digital_match = re.search('\d', password)
    letter_match = re.search('[a-zA-Z]', password)
    if len(password) < 8:
        ret['msg'] = '12'  #密码长度最少为8位
        return ret
    elif len(password) > 32:
        ret['msg'] = '13'  #密码长度过长
        return ret
    if space_match:
        ret['msg'] = '14'  #密码不能有空格等字符
        return ret
    if not digital_match and letter_match:
        ret['msg'] = '15'  #密码至少含有一位字母和数字
        return ret
    if not password_confirm == password:
        ret['msg'] = '16'  #两次密码输入不一致
        return ret
    return 'ok'
    
def myState(user_obj, ret):
    uid = user_obj.id
    #边栏信息
    collect_m = models.Collect_Movie.objects.filter(user__id=uid)
    collect_t = models.Collect_Tv.objects.filter(user__id=uid)
    collect_a = models.Collect_Anime.objects.filter(user__id=uid)
    collect_s = models.Collect_Show.objects.filter(user__id=uid)
    collect_all_list = list(collect_m) + list(collect_t) + list(collect_a) + list(collect_s)
    collect_all_list = sorted(chain(collect_all_list), key=attrgetter('create_date'), reverse=True)
    if len(collect_all_list) > 0:
        latest_coll = collect_all_list[0]
        while True:
            try:
                ret['latest_collection'] = latest_coll.movie
                ret['latest_collection_cate'] = 'movie'
                ret['latest_collection_cate_ch'] = '电影'
                break
            except Exception:
                pass
            try:
                ret['latest_collection'] = latest_coll.tv
                ret['latest_collection_cate'] = 'tv'
                ret['latest_collection_cate_ch'] = '电视剧'
                break
            except Exception:
                pass
            try:
                ret['latest_collection'] = latest_coll.anime
                ret['latest_collection_cate'] = 'anime'
                ret['latest_collection_cate_ch'] = '动漫'
                break
            except Exception:
                pass
            try:
                ret['latest_collection'] = latest_coll.show
                ret['latest_collection_cate'] = 'show'
                ret['latest_collection_cate_ch'] = '综艺'
                break
            except Exception:
                pass
            
            break
    else:
        ret['latest_collection'] = None
    
    #看过（评分过）
    movie_rating_obj = models.MovieReply.objects.filter(rating__gt=0, user__id=uid)
    tv_rating_obj = models.TvReply.objects.filter(rating__gt=0, user__id=uid)
    anime_rating_obj = models.AnimeReply.objects.filter(rating__gt=0, user__id=uid)
    show_rating_obj = models.ShowReply.objects.filter(rating__gt=0, user__id=uid)
    rating_all_list = list(movie_rating_obj) + list(tv_rating_obj) + list(anime_rating_obj) + list(show_rating_obj)
    rating_all_list = sorted(chain(rating_all_list), key=attrgetter('create_date'), reverse=True)
    if len(rating_all_list) > 0:
        latest_rating = rating_all_list[0]
        while True:
            try:
                ret['latest_rating'] = latest_rating.movie
                ret['latest_rating_cate'] = 'movie'
                ret['latest_rating_cate_ch'] = '电影'
                break
            except Exception:
                pass
            try:
                ret['latest_rating'] = latest_rating.tv
                ret['latest_rating_cate'] = 'tv'
                ret['latest_rating_cate_ch'] = '电视剧'
                break
            except Exception:
                pass
            try:
                ret['latest_rating'] = latest_rating.anime
                ret['latest_rating_cate'] = 'anime'
                ret['latest_rating_cate_ch'] = '动漫'
                break
            except Exception:
                pass
            try:
                ret['latest_rating'] = latest_rating.show
                ret['latest_rating_cate'] = 'show'
                ret['latest_rating_cate_ch'] = '综艺'
                break
            except Exception:
                pass
            break
    else:
        ret['latest_rating'] = None
    
    #关注与被粉丝
    focus_obj = models.UserFocus.objects.filter(origin_user_of_focus__id=uid)
    if focus_obj:
        ret['latest_focus'] = focus_obj.order_by('-create_date')[0]
    else:
        ret['latest_focus'] = None
    fans_obj = models.UserFocus.objects.filter(target_user__id=uid)
    if fans_obj:
        ret['latest_fans'] = fans_obj.order_by('-create_date')[0]
    else:
        ret['latest_fans'] = None
        
    return ret

def myAchievement(user_obj, ret):
    uid = user_obj.id
    total_exp = user_obj.exp
    ret['my_level'] = getUserLevel(total_exp)
    post_counts = models.Post.objects.filter(user__id=uid).count()
    post_r_counts = models.PostReply.objects.filter(user__id=uid).count()
    ret['post_counts'] = post_counts + post_r_counts
    m_obj = models.MovieReply.objects.filter(user__id=uid)
    t_obj = models.TvReply.objects.filter(user__id=uid)
    a_obj = models.AnimeReply.objects.filter(user__id=uid)
    s_obj = models.ShowReply.objects.filter(user__id=uid)
    media_list = [m_obj, t_obj, a_obj, s_obj]
    comment_counts = 0
    rating_counts = 0
    for item in media_list:
        comment_counts += item.count()
        rating_counts += item.filter(rating__gt=0).count()
    ret['comment_counts'] = comment_counts
    ret['rating_counts'] = rating_counts
    mc = models.Collect_Movie.objects.filter(user__id=uid).count()
    tc = models.Collect_Tv.objects.filter(user__id=uid).count()
    ac = models.Collect_Anime.objects.filter(user__id=uid).count()
    sc = models.Collect_Show.objects.filter(user__id=uid).count()
    ret['collect_counts'] = mc + tc + ac + sc
    ret['reg_days'] = getRegisterDays(uid)
    
    return ret

def activeUser(ret):
    show_counts = 3
    max_exp_user_obj = models.User.objects.filter(today_exp__gt=100)
    max_exp_user_counts = max_exp_user_obj.count()  #达到日经验满值的用户数
    if max_exp_user_counts > show_counts:
        show_users = sample(max_exp_user_obj, show_counts)
    else:
        show_users = models.User.objects.all().order_by('-today_exp')[:show_counts]
    for item in show_users:
        ulevel = getUserLevel(item.exp)
        item.ulevel = ulevel
    ret['active_users'] = show_users
    return ret

def movieRecommend(ret):
    show_counts = 3
    mr_obj = models.Movie_Recommend.objects.filter(cate=1).order_by('-create_date')[:show_counts]
    result = []
    for item in mr_obj:
        try:
            obj = models.Movie.objects.get(id=item.media_id)
            obj.cate = 'movie'
            obj.reason = item.reason
            result.append(obj)
        except Exception:
            pass
    ret['movie_recommend'] = result
    return ret

def visitHistory(ret, uid, show_counts):
    recent_visitors = models.UserVisitHistory.objects.filter(host__id=uid).order_by('-update_date')[:show_counts]
    ret['recent_visitors'] = recent_visitors

    return ret

def getRegisterDays(uid):
    try:
        user_obj = models.User.objects.get(id=uid)
    except Exception:
        return False
    reg_date = user_obj.create_date
    reg_days = (datetime.now() - reg_date).days
    return reg_days

def updateNotification(target_user_obj, item):
    target_uid = target_user_obj.id
    notice_obj = models.User_Notification_Check.objects.filter(target_user__id=target_uid)
    if notice_obj.count() == 1:
        notice_obj = notice_obj[0]
    else:  #创建通知条目
        notice_obj = models.User_Notification_Check.objects.create(target_user=target_user_obj)
    if item == 'bbs_r':
        notice_obj.bbs_r += 1
        notice_obj.save()