#_*_coding:UTF-8_*_
#from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect
#from django.template.context import RequestContext
from movie import models
import re
import json
from datetime import datetime, date

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

def try_int(arg, default):
    try:
        arg = int(arg)
    except Exception:
        arg = default
    return arg

def loginInfo(request, ret, sel=0):
    uid = request.session.get('login_user_id', None)
    if uid:
        ret['logined'] = True
        user_obj = models.User.objects.filter(id = uid)
        if len(user_obj) == 0:
            user_obj = None
        elif len(user_obj) == 1:
            user_obj = user_obj[0]
    else:  #未登录
        user_obj = None
    if sel == 0:
        return ret, user_obj
    else:
        return ret

def getFromUrl(request):
    from_url = request.META.get('HTTP_REFERER', '/')
    print from_url
    from_url_rel = re.sub('^http://.*?[^/]{1,}', '', from_url, re.S) #相对路径
    reg_path = '/user/register/'
    login_path = '/user/login/'
    if not from_url_rel == reg_path or not from_url_rel == login_path:
        return from_url_rel
    else:
        return "/"
    
#判断用户是否登录
def loginCheck(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('login_user_id', None):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/user/login/?url_from='+request.path)
    return wrapper

#富文本提交HTML过滤显示
def htmlContentFilter(html_content, cate='rich'):
    if cate == 'media':
        html_content = re.sub(r'<((?!img src="\/media|img src="\/static\/js\/plugs\/sinaEmotion|br).*?)>', r'&lt;\1&gt;', html_content)
    elif cate == 'static':
        html_content = re.sub(r'<((?!img src="\/static|br).*?)>', r'&lt;\1&gt;', html_content)
    else:
        html_content = re.sub(r'<((?!img|p|/p|br|a|/a|iframe|/iframe).*?)>', r'&lt;\1&gt;', html_content)
    #html_content = re.sub(r'<(p .*?)>', r'&lt;\1&gt;', html_content)
    #html_content = re.sub(r'<(/p)>', r'&lt;\1&gt;', html_content)
    #html_content = re.sub(r'<(br)>', r'&lt;\1&gt;', html_content)
    return html_content

#配合上面使用
def htmlCleaner(html_content):
    html_content = re.sub('(<p\s.*?>', '<p>', html_content)
    html_content = re.sub('(<a\s.*?>', '<a>', html_content)
    html_content = re.sub('(<br\s.*?>', '<br>', html_content)
    return html_content

def getTodayStr():
    today_str = date.today().strftime('%Y-%m-%d')
    return today_str