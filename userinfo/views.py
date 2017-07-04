#_*_coding:UTF-8_*_
from django.shortcuts import render_to_response, Http404
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.db.models import Q
from movie import models
#from pip._vendor.requests.models import json_dumps
#from userinfo import forms
from django.template.context import RequestContext
import json,re,os,datetime
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
from itertools import chain
from operator import attrgetter
from packages import user_helper, html_helper, images_helper, general
from packages.general import loginCheck, loginInfo, getFromUrl, htmlContentFilter, try_int, CJsonEncoder
from packages.user_helper import getUserLevel, getUserExpPercent
from MovieSite.settings import BASE_DIR
#from django.core.exceptions import FieldDoesNotExist

default_avatar_s = '/static/images/default/avatar/avatar_default_40x40.jpg'

def loginPage(request):
    ret={}
    #from_url = getFromUrl(request)
    url_from = request.GET.get('url_from')
    request.session['login_from'] = url_from
    return render_to_response('userinfo/pwd/login.html', ret, context_instance=RequestContext(request))

"""
def modalLogin(request):
    ret = {}
    if request.method == 'POST':
        username = request.POST.get('username', None).strip()
        password = request.POST.get('password', None)
        checkbox = request.POST.get('checkbox', None)
    else:
        raise Http404
"""
def loginSubmit(request):
    ret = {}
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password', None)
        checkbox = request.POST.get('checkbox', None)
        check_result = False
        if email:
            if not user_helper.verifyEmailPat(email):
                ret['msg'] = '22'  #邮箱格式错误
                return HttpResponse(json.dumps(ret))
        else:
            ret['msg'] = '21'  #邮箱不能为空
            return HttpResponse(json.dumps(ret))

        if password:
            if len(password) < 8:
                ret['msg'] = '12'  #密码长度最少为8位
                return HttpResponse(json.dumps(ret))
            elif len(password) > 32:
                ret['msg'] = '13'
                return HttpResponse(json.dumps(ret))
            else:  #密码长度正确
                space_match = re.search('\s', password)
                digital_match = re.search('\d', password)
                letter_match = re.search('[a-zA-Z]', password)
                if space_match:
                    ret['msg'] = '14'  #密码不能有空格等字符
                    return HttpResponse(json.dumps(ret))
                else:   #若合法
                    if digital_match and letter_match:
                        check_result = True
                    else:
                        ret['msg'] = '15'  #密码至少含有一位字母和数字
                        return HttpResponse(json.dumps(ret))
        else:
            ret['msg'] = '11'  #密码为空
            return HttpResponse(json.dumps(ret))

        #若用户名密码合法，判断用户是否存在
        if check_result:
            userObj = models.User.objects.filter(email = email) #先判断用户是否存在
            if len(userObj) == 0:
                ret['msg'] = '24'  #邮箱账号不存在
                return HttpResponse(json.dumps(ret))
            elif len(userObj) > 1:
                ret['msg'] = '102'  #数据库有重复的邮箱
                return HttpResponse(json.dumps(ret))
            else:  #账号存在且唯一
                counts = models.User.objects.filter(email = email, password = password).count()
                #登录成功
                if counts == 1:
                    if userObj[0].privilege == 1:  #此账号尚未激活
                        ret['msg'] = '25'
                        return HttpResponse(json.dumps(ret))
                    elif userObj[0].privilege == 0:  #账号被封
                        ret['msg'] = '26'
                        return HttpResponse(json.dumps(ret))
                    else:  #账号正常
                        if not checkbox:
                            request.session.set_expiry(0) #关闭浏览器失效
                        request.session['login_user_id'] = userObj[0].id  #记录登录session
                        #ret['logined'] = True
                        #检查recvpush
                        ret['recvpush'] = userObj[0].h_recvpush
                        ret['msg'] = 'success'
                        ret['login_from'] = request.session['login_from']
                        return HttpResponse(json.dumps(ret))
                elif counts == 0:
                    ret['msg'] = '18'  #密码错误
                    return HttpResponse(json.dumps(ret))
                else:  #数据库用户条目重复
                    ret['msg'] = '102'  #重复
                    return HttpResponse(json.dumps(ret))


def quickLogin(request):
    ret = {}
    email = request.POST.get('username').strip()
    password = request.POST.get('password', None)
    checkbox = request.POST.get('checkbox', None)
    check_result = False
    #若提交类型为POST，判断用户名和密码合法性
    if request.method == 'POST':
        if email:
            if not user_helper.verifyEmailPat(email):
                ret['msg'] = '22'  #邮箱格式错误
                return HttpResponse(json.dumps(ret))
        else:
            ret['msg'] = '21'  #邮箱不能为空
            return HttpResponse(json.dumps(ret))
        
        if password:
            if len(password) < 8:
                ret['msg'] = '12'  #密码长度最少为8位
                return HttpResponse(json.dumps(ret))
            elif len(password) > 32:
                ret['msg'] = '13'
                return HttpResponse(json.dumps(ret))
            else:
                space_match = re.search('\s', password)
                digital_match = re.search('\d', password)
                letter_match = re.search('[a-zA-Z]', password)
                if space_match:
                    ret['msg'] = '14'  #密码不能有空格等字符
                    return HttpResponse(json.dumps(ret))
                else:   #若合法
                    if digital_match and letter_match:
                        check_result = True
                    else:
                        ret['msg'] = '15'  #密码至少含有一位字母和数字
                        return HttpResponse(json.dumps(ret))
        else:
            ret['msg'] = '11'  #密码为空
            return HttpResponse(json.dumps(ret))

        #若用户名密码合法，判断用户是否存在
        if check_result:
            userObj = models.User.objects.filter(email = email) #先判断用户是否存在
            if len(userObj) == 0:
                ret['msg'] = '24'  #邮箱账号不存在
                return HttpResponse(json.dumps(ret))
            elif len(userObj) > 1:
                ret['msg'] = '102'  #数据库有重复的邮箱
                return HttpResponse(json.dumps(ret))
            else:  #用户存在且唯一
                counts = models.User.objects.filter(email = email, password = password).count()
                #登录成功
                if counts == 1:
                    if userObj[0].privilege == 1:  #此账号尚未激活
                        ret['msg'] = '25'
                        return HttpResponse(json.dumps(ret))
                    elif userObj[0].privilege == 0:  #账号被封
                        ret['msg'] = '26'
                        return HttpResponse(json.dumps(ret))
                    request.session['login_user_id'] = userObj[0].id

                    ret['recvpush'] = userObj[0].h_recvpush
                    if not checkbox:
                        request.session.set_expiry(0) #关闭浏览器失效
                    ret['msg'] = 'success'
                    ret['logined'] = True
                    return HttpResponse(json.dumps(ret))
                elif counts == 0:
                    ret['msg'] = '18'  #密码错误
                    return HttpResponse(json.dumps(ret))
                else:  #数据库用户条目重复
                    pass

    
def logout(request):
    ret = {'logined':''}
    prev_url = request.META.get('HTTP_REFERER', '/')
    #request.session['logout_from'] = prev_url  #记录当前所在地址，在退出登录后返回
    
    try:
        del request.session['login_user_id']
        ret['logined'] = False
    except KeyError:
        return HttpResponseRedirect('/', ret)
    
    return HttpResponseRedirect(prev_url, ret)


def registerPage(request):
    ret = {}
    from_url = getFromUrl(request)
    request.session['register_from'] = from_url
    code_text, code_img_path = images_helper.generate_code()
    #图片路径
    ret['reg_code'] = code_img_path
    #验证码存入session
    request.session['reg_code'] = code_text
    return render_to_response('userinfo/pwd/register.html', ret, context_instance=RequestContext(request))

def registerSubmit(request):
    ret = {'logined': False, 'msg': ''}
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('pass', '')
        password_confirm = request.POST.get('pass_confirm', '')
        nickname = request.POST.get('nickname', '').strip()
        reg_code = request.POST.get('reg_code', '').upper()
        if not all([email, password, password_confirm, nickname, reg_code]):
            if not email:
                ret['msg'] = '21'
                return HttpResponse(json.dumps(ret))
            if not password:
                ret['msg'] = '11'
                return HttpResponse(json.dumps(ret))
            if not password_confirm:
                ret['msg'] = '17'
                return HttpResponse(json.dumps(ret))
            if not nickname:
                ret['msg'] = '41'
                return HttpResponse(json.dumps(ret))
            if not reg_code:
                ret['msg'] = '31'
                return HttpResponse(json.dumps(ret))
        #全部非空
        else:
            if not user_helper.verifyEmailPat(email):
                ret['msg'] = '22'  #邮箱格式错误
                return HttpResponse(json.dumps(ret))
            #只判断密码格式与正确性
            space_match = re.search('\s', password)
            digital_match = re.search('\d', password)
            letter_match = re.search('[a-zA-Z]', password)
            space_match2 = re.search('\s', password_confirm)
            digital_match2 = re.search('\d', password_confirm)
            letter_match2 = re.search('[a-zA-Z]', password_confirm)
            if len(password) < 8:
                ret['msg'] = '12'  #密码长度最少为8位
                return HttpResponse(json.dumps(ret))
            elif len(password) > 32:
                ret['msg'] = '13'  #密码长度过长
                return HttpResponse(json.dumps(ret))
            if space_match:
                ret['msg'] = '14'  #密码不能有空格等字符
                return HttpResponse(json.dumps(ret))
            if not digital_match or not letter_match:
                ret['msg'] = '15'  #密码至少含有一位字母和数字
                return HttpResponse(json.dumps(ret))
            if space_match2:
                ret['msg'] = '19'
                return HttpResponse(json.dumps(ret))
            if not digital_match2 or not letter_match2:
                ret['msg'] = '1a'  #密码至少含有一位字母和数字
                return HttpResponse(json.dumps(ret))
            if not password_confirm == password:
                ret['msg'] = '16'  #两次密码输入不一致
                return HttpResponse(json.dumps(ret))

            email_counts = models.User.objects.filter(email=email).count()
            if email_counts > 0:
                ret['msg'] = '23'  #邮箱已被注册
                return HttpResponse(json.dumps(ret))
    
            nickname_counts = models.User.objects.filter(username=nickname).count()
            if nickname_counts > 0:
                ret['msg'] = '43'  #昵称已被抢占
                return HttpResponse(json.dumps(ret))
            else:
                if len(nickname.encode('gbk')) > 16:
                    ret['msg'] = '42'  #昵称长度超过16个英文字符
                    return HttpResponse(json.dumps(ret))
            
            #验证码正确
            if reg_code == request.session['reg_code']:
                #生成的token，记入数据库
                token = user_helper.genRandomToken()
                if not sendActiveMail(email, nickname, token): #发送激活邮件失败
                    ret['msg'] = '301'
                    return HttpResponse(json.dumps(ret))
                try:
                    new_user_obj = models.User.objects.create(email = email, username = nickname, password = password, pwd_token=token)
                    models.User_Notification_Check.objects.create(target_user=new_user_obj) #建立轮询检查条目
                except Exception:
                    ret['msg'] = '101'
                    return HttpResponse(json.dumps(ret))
                #记录session
                request.session['login_user_id'] = new_user_obj.id
                #初始化关注
                official_accounts = models.User.objects.filter(privilege=5)

                for item in official_accounts:
                    try:
                        models.UserFocus.objects.create(target_user=item, origin_user_of_focus=new_user_obj)
                    except Exception:
                        ret['msg'] = '101'
                        return HttpResponse(json.dumps(ret))
                ret['msg'] = 'success'
                return HttpResponse(json.dumps(ret))
            else:
                ret['msg'] = '32'  #验证码错误
                return HttpResponse(json.dumps(ret))
    else:
        raise Http404
    
def registerActive(request):
    ret = {}
    email = request.GET.get('email', None)
    token = request.GET.get('token', None)
    user_obj = models.User.objects.filter(email=email)
    if len(user_obj) == 1:
        if token == user_obj[0].pwd_token:
            try:
                user_obj.update(privilege=4, pwd_token='')
                ret['success'] = 'success'
                ret['username'] = user_obj[0].username
                
                
            except Exception:
                ret['error'] = '101'  #更新数据库失败
        else:
            ret['error'] = '51'  #token不匹配
    elif len(user_obj) == 0:
        ret['error'] = '24'  #email不存在
    else: #邮箱重复
        pass
    response = render_to_response('userinfo/pwd/register_active.html', ret, context_instance=RequestContext(request))
    response.set_cookie('logined', 'yes')
    return response
    
def changeCode(request):
    ret = {}
    action = request.POST.get('action')
    code_text, code_img_path = images_helper.generate_code()
    if action == 'register':
        request.session['reg_code'] = code_text
    elif action == 'forget_pwd':
        request.session['forget_pwd_code'] = code_text
    ret['code_path'] = code_img_path
    return HttpResponse(json.dumps(ret))

def forgetPwdPage(request):
    ret = {}
    code_text, code_img_path = images_helper.generate_code()
    #图片路径
    ret['forget_pwd_code'] = code_img_path
    #验证码存入session
    request.session['forget_pwd_code'] = code_text
    return render_to_response('userinfo/pwd/forget_pwd.html', ret, context_instance=RequestContext(request))

def forgetPwdSubmit(request):
    ret = {}
    if request.method == 'POST':
        email = request.POST.get('email', None).strip()
        code_input = request.POST.get('code', None).upper()
        if all([email, code_input]):
            if user_helper.verifyEmailPat(email):  #邮箱格式正确
                #生成的token，记入数据库
                token = user_helper.genRandomToken()
                user_obj = models.User.objects.filter(email=email)
                user_obj.update(pwd_token=token)
                if len(user_obj) == 1:  #邮箱存在
                    if code_input == request.session['forget_pwd_code']:  #验证码正确
                        if not sendVerifyMail(email, user_obj[0].username, token):
                            ret['msg'] = '301'  #发送邮件错误
                        else:  #邮件发送成功
                            pass
                    else:
                        ret['msg'] = '32'  #验证码错误
                        
                else:
                    ret['msg'] = '24'  #用户邮箱不存在
            else:
                ret['msg'] = '22' #邮箱格式错误
            
        else:
            if not email:
                ret['msg'] = '21'  #邮箱为空
            elif not code_input:
                ret['msg'] = '31'  #验证码为空
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404
        
def sendActiveMail(email, nickname, token):
    try:
        subject = '账号激活'
        text_content = 'content here'
        user_link = 'http://www.bigedianying.com/user/register/active/?email='+email+'&token='+token
        content = '<p>Hi~ 亲爱的 %s，欢迎加入比格电影！请点击下面的按钮激活你的账号：</p>'%nickname.encode('utf8')
        html_content = open(BASE_DIR + '/templates/userinfo/mail/general_mail.html').read()\
            .replace('subject_default',subject).replace('content_default',content).replace('link_default',user_link)
        
        from_email = '比格电影 <no-reply@bigedianying.com>'
        #from_email = 'bigedianying@gmail.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except Exception:
        return False
    
def sendVerifyMail(email, username, token):
    try:
        subject = '密码找回'
        text_content = 'content here'
        user_link = 'http://www.bigedianying.com/user/forget_pwd/verify/?email='+email+'&token='+token
        content = '<p>Hi~ 亲爱的 %s，</p>'%username.encode('utf8') + '<p>我们收到了你的密码重置请求，请点击下面的按钮找回密码：</p>'
        html_content = open(BASE_DIR + '/templates/userinfo/mail/general_mail.html').read()\
            .replace('subject_default',subject).replace('content_default',content).replace('link_default',user_link)\
        
        from_email = '比格电影 <no-reply@bigedianying.com>'
        #from_email = 'bigedianying@gmail.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except Exception,e:
        print e
        return False

#验证找回密码链接，返回不同（修改密码或找回密码）页面
def forgetPwdverify(request):
    email = request.GET.get('email')
    token = request.GET.get('token')
    #ret = {}
    userObj = models.User.objects.filter(email=email)
    if len(userObj) == 0:
        #ret['msg'] = '101'  #邮箱不存在
        return render_to_response('userinfo/pwd/forget_pwd_verify_failed.html', context_instance=RequestContext(request))
    elif len(userObj) == 1:  #邮箱存在
        if token == userObj[0].pwd_token:  #token正确
            request.session['pwd_token'] = token  #记录session，更改密码页面需验证
            return render_to_response('userinfo/pwd/forget_pwd_changepwd.html', context_instance=RequestContext(request))
        else:
            #ret['status'] = '102'  #无效链接，token不对
            return render_to_response('userinfo/pwd/forget_pwd_verify_failed.html', context_instance=RequestContext(request))
    else:  #邮箱有重复
        return render_to_response('userinfo/pwd/forget_pwd_verify_failed.html', context_instance=RequestContext(request))


def forgetPwdChange(request):
    ret = {}
    if request.method == 'POST':
        user_Obj = models.User.objects.filter(pwd_token=request.session['pwd_token'])
        if len(user_Obj) == 0:
            ret['msg'] = '101'  #token错误
            return render_to_response('userinfo/pwd/forget_pwd_verify_failed.html', ret, context_instance=RequestContext(request))
        elif len(user_Obj) == 1:
            password = request.POST.get('pass')
            password_confirm = request.POST.get('pass_confirm')
            if all([password, password_confirm]):
                #密码格式与正确性
                pass_result = user_helper.verifyPassPat(password, password_confirm, ret)
                if not pass_result == 'ok':  #若不等于ok，则返回新的ret
                    ret = pass_result
                else:
                    user_Obj.update(password=password, pwd_token='')
                    ret['msg'] = 'success'
                return HttpResponse(json.dumps(ret))
            else:
                if not password:
                    ret['msg'] = '11'
                    return HttpResponse(json.dumps(ret))
                if not password_confirm:
                    ret['msg'] = '17'
                    return HttpResponse(json.dumps(ret))
                
        else:  #重复的token
            pass
    else:
        raise Http404
    

@loginCheck
def homePage(request):
    ret = {}
    ret, user_obj = loginInfo(request, ret)  #logined, user_info
    if not user_obj:  #session存在，用户不存在，直接返回首页
        del request.session['login_user_id']
        return HttpResponseRedirect('/')
    ret['user_info'] = user_obj
    uid = user_obj.id
    #speak
    my_speak_obj = models.UserSpeak.objects.filter(user__id=uid)
    speak_result = []
    for item in my_speak_obj:
        speak_result.append(item)  #我的说说全部加入列表
    focused_user_obj = models.UserFocus.objects.filter(origin_user_of_focus__id=uid, origin_user_of_focus__h_myspeak__gt=0)  #我关注的人且权限为好友可见或所有人可见
    if focused_user_obj:
        ret['my_focused'] = focused_user_obj.order_by('-create_date')
        for item in focused_user_obj:  #循环每个我关注的人
            speak_obj = models.UserSpeak.objects.filter(user__id=item.target_user.id)
            for s in speak_obj:  #循环每个人的每条说说
                speak_result.append(s)
    speak_result = sorted(chain(speak_result), key=attrgetter('create_date'), reverse=True)#[:10] ,key=attrgetter('create_date'))
    
    #分页
    page = try_int(request.GET.get('page', 1), 1)
    speak_counts = len(speak_result)
    #ret['speak_counts'] = speak_counts
    page_obj = html_helper.PageInfo(page, speak_counts, 10)
    try:
        speak_result = speak_result[page_obj.start : page_obj.end]
    except Exception:
        speak_result = ''
    ret['speak_result'] = speak_result
    filter_url = '/user/home/?page='
    page_list = html_helper.ajaxScrollPager(page, page_obj.total_page_counts, filter_url)
    ret['page_list'] = page_list
    
    #上传图片前先检查临时表有无历史残留
    temp_photos = models.UserSpeakTemp.objects.filter(user__id=uid)
    if temp_photos:  #存在的话需要清理
        for photo_obj in temp_photos:
            photo_path = str(photo_obj.speak_photo)
            thumb_path = re.sub(r'(^/media/speak/\d+/)(.*)$', r'\1thumbs/\2', photo_path)
            try:
                os.remove(os.path.join(BASE_DIR + photo_path))
                os.remove(os.path.join(BASE_DIR + thumb_path))
                models.UserSpeakTemp.objects.filter(user__id=uid, speak_photo=photo_path).delete()
            except Exception:
                pass
    
    #我的粉丝
    fans_obj = models.UserFocus.objects.filter(target_user__id=uid).order_by('-create_date')
    if fans_obj:
        for u in fans_obj:  #循环每个粉丝对象
            u.i_focused = False
            for item in focused_user_obj:  #对每个我关注的人和粉丝比较，是否已关注
                if item.target_user.id == u.origin_user_of_focus.id:  #ID相同
                    u.i_focused = True
                    break
        ret['my_fans'] = fans_obj

    ret = user_helper.myState(user_obj, ret)
    ret = user_helper.myAchievement(user_obj, ret)
    ret = user_helper.activeUser(ret)
    ret = user_helper.movieRecommend(ret)
    ret = user_helper.visitHistory(ret, uid, 15)
    return render_to_response('userinfo/home/home_index.html', ret, context_instance=RequestContext(request)) #/user/USER_NAME/ 进入个人中心

@loginCheck
def userMessages(request):
    ret = {}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    uid = user_obj.id
    
    msg_obj = models.User_Message.objects.filter(Q(receiver__id=uid)|Q(sender__id=uid)).order_by('-update_date')[:10]
    if msg_obj.count():
        for item in msg_obj:
            if item.read:
                msg_read = 0
            else:
                msg_read = 1
            if item.user_message.all().count():  #查找回复
                unread_counts = item.user_message.filter(read=0).count()  #未读的回复，还需加上消息本身（若非自己所发）
                item.unread_counts = unread_counts + msg_read
                newest_reply = item.user_message.all().order_by('-create_date')[0]
                item.newest_reply = newest_reply
            else:
                item.newest_reply = None
        ret['messages'] = msg_obj
    else:
        ret['messages'] = None
    
    #边栏
    ret = user_helper.myState(user_obj, ret)
    ret = user_helper.myAchievement(user_obj, ret)
    ret = user_helper.activeUser(ret)
    ret = user_helper.movieRecommend(ret)
    ret = user_helper.visitHistory(ret, uid, 15)
    
    #清除check表，但不清除unread
    models.User_Notification_Check.objects.filter(target_user__id=uid).update(msg=0)
    return render_to_response('userinfo/home/home_messages.html', ret, context_instance=RequestContext(request)) 

def removeBadge(request):
    if request.method == 'POST':
        msg_id = request.POST.get('msg_id', None)
        msg_objs = models.User_Message.objects.filter(id=msg_id)
        if msg_objs.count():
            msg_objs.update(read=1)
        msg_reply_objs = models.User_Message_Reply.objects.filter(message__id=msg_id)
        if msg_reply_objs.count():
            msg_reply_objs.update(read=1)
        return HttpResponse(True)
    else:
        raise Http404

@loginCheck
def sendMessage(request):
    if request.method == 'POST':
        ret= {}
        content = request.POST.get('content', None)

        if not content.strip():
            ret['msg'] = '901'
            return HttpResponse(json.dumps(ret))
        content = htmlContentFilter(content, 'static')
        receiver_id = request.POST.get('receiver_id', None)
        msg_id = request.POST.get('msg_id', None)
        if receiver_id:  #模态框所发
            if receiver_id.isdigit():
                try:
                    uid = request.session['login_user_id']
                except Exception:
                    ret['msg'] = '401'
                    return HttpResponse(json.dumps(ret))
                result = models.User_Message.objects.filter(Q(sender__id=uid,receiver__id=receiver_id)|
                                                            Q(sender__id=receiver_id,receiver__id=uid))
                receiver_obj = models.User.objects.get(id=receiver_id)
                sender_obj = models.User.objects.get(id=uid)
    
                if result.count() == 1:  #发送过私信
                    msg_obj = result[0]
                    models.User_Message_Reply.objects.create(content=content, message=msg_obj,
                                                            receiver=receiver_obj, sender=sender_obj)
                    ret['msg'] = 'success'
                elif result.count() == 0:  #还没有发送过
                    models.User_Message.objects.create(content=content, receiver=receiver_obj, sender=sender_obj)
                    ret['msg'] = 'success'
                else:
                    ret['msg'] = '103'
                    return HttpResponse(json.dumps(ret))
            else:
                ret['msg'] = '302'  #前端数据错误
            return HttpResponse(json.dumps(ret))
        elif msg_id:  #在message页面所发
            if msg_id.isdigit():
                uid = request.session['login_user_id']

                try:
                    msg_obj = models.User_Message.objects.get(id=msg_id)
                except Exception:
                    ret['msg'] = '103'

                if msg_obj.sender.id == uid:
                    receiver_id = msg_obj.receiver.id
                elif msg_obj.receiver.id == uid:
                    receiver_id = msg_obj.sender.id
                else:
                    ret['msg'] = '912'  #请求的message的发送者和接受者均不为当前用户
                    
                try:
                    receiver_obj = models.User.objects.get(id=receiver_id)
                    sender_obj = models.User.objects.get(id=uid)
                except Exception:
                    ret['msg'] = '103'
                    
                try:
                    new_reply = models.User_Message_Reply.objects.create(content=content, message=msg_obj,
                                                                         receiver=receiver_obj, sender=sender_obj)
    
                    models.User_Message.objects.filter(id=msg_id).update(update_date=new_reply.create_date)
                    ret['thumb_s'] = str(sender_obj.thumb_s)
                    ret['receiver_id'] = receiver_id
                    ret['reply_date'] = new_reply.create_date
                    ret['msg'] = 'success'
                    
                except Exception:
                    ret['msg'] = '101'
    
                return HttpResponse(json.dumps(ret, cls=general.CJsonEncoder))
            else:
                ret['msg'] = '302' #前端数据错误
                return HttpResponse(json.dumps(ret))

    else:
        raise Http404

def getMoreMsg(request):
    if request.method == 'POST':
        onetime_load_counts = 10
        msg_id = request.POST.get('msg_id')
        illegal_id = re.search('^\d+$', msg_id)
        if illegal_id:
            cur_uid = request.session['login_user_id']
            loaded_counts = int(request.POST.get('loaded_counts'))

            total_counts = models.User_Message_Reply.objects.filter(message__id=msg_id).count()

            if total_counts < 10:  #等于9个或小于9个回复时，loaded_counts包括message本身
                loaded_counts -= 1

            remainder_counts = total_counts - loaded_counts - 10
            if remainder_counts < 0:  #reply不足10个时加上message
                try:
                    msg_obj = models.User_Message.objects.filter(id=msg_id).values('content','create_date', 'sender_id', 'receiver_id')[0]
                    msg_obj['sender_thumb_s'] = str(models.User.objects.get(id=msg_obj['sender_id']).thumb_s)
                    msg_obj['receiver_thumb_s'] = str(models.User.objects.get(id=msg_obj['receiver_id']).thumb_s)
                    msg_obj['cur_uid'] = cur_uid
                except Exception:
                    pass

            result_list = [remainder_counts]
            result = models.User_Message_Reply.objects.filter(message__id=msg_id).order_by('-create_date').values('content','create_date', 'sender_id', 'receiver_id')[loaded_counts:loaded_counts+onetime_load_counts]
            for item in result:
                item['sender_thumb_s'] = str(models.User.objects.get(id=item['sender_id']).thumb_s)
                item['receiver_thumb_s'] = str(models.User.objects.get(id=item['receiver_id']).thumb_s)
                item['cur_uid'] = cur_uid
                result_list.append(item)
            result_list.append(msg_obj)
            return HttpResponse(json.dumps(result_list, cls=general.CJsonEncoder))
        else:
            pass
    else:
        raise Http404


@loginCheck
def userNotification(request):
    ret = {}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    uid = user_obj.id
    cate = request.GET.get('c', None)
    if not cate:
        ur = 0
        html_template = 'userinfo/home/home_notification.html'
        notice_filter_url = '/user/home/notification/?page='
    elif cate == 'history':
        ur = 1
        html_template = 'userinfo/home/home_notification_history.html'
        notice_filter_url = '/user/home/notification/?c=history&page='
    
    #focus
    focus_obj = models.UserFocus.objects.filter(target_user__id=uid, read=ur)
    #post reply
    post_reply_obj = models.PostReply.objects.filter(post__user__id=uid, read=ur).exclude(user__id=uid)
    post_lr_obj = models.PostLayerReply.objects.filter(post_reply__user__id=uid, read=ur).exclude(user__id=uid)
    #speak_reply
    
    #comment
    movie_rr_obj = models.MovieReplyReply.objects.filter(movie_reply__user__id=uid, read=ur).exclude(user__id=uid)
    movie_like_obj = models.MovieReplyLike.objects.filter(movie_reply_like__user__id=uid, read=ur).exclude(user__id=uid)
    tv_rr_obj = models.TvReplyReply.objects.filter(tv_reply__user__id=uid, read=ur).exclude(user__id=uid)
    tv_like_obj = models.TvReplyLike.objects.filter(tv_reply_like__user__id=uid, read=ur).exclude(user__id=uid)
    anime_rr_obj = models.AnimeReplyReply.objects.filter(anime_reply__user__id=uid, read=ur).exclude(user__id=uid)
    anime_like_obj = models.AnimeReplyLike.objects.filter(anime_reply_like__user__id=uid, read=ur).exclude(user__id=uid)
    show_rr_obj = models.ShowReplyReply.objects.filter(show_reply__user__id=uid, read=ur).exclude(user__id=uid)
    show_like_obj = models.ShowReplyLike.objects.filter(show_reply_like__user__id=uid, read=ur).exclude(user__id=uid)
    news_rr_obj = models.NewsReplyReply.objects.filter(news_reply__user__id=uid, read=ur).exclude(user__id=uid)
    news_like_obj = models.NewsReplyLike.objects.filter(news_reply_like__user__id=uid, read=ur).exclude(user__id=uid)

    temp_list = [focus_obj, post_reply_obj, post_lr_obj, movie_like_obj, movie_rr_obj,
                    tv_rr_obj, tv_like_obj, anime_like_obj, anime_rr_obj, show_rr_obj, show_like_obj,
                    news_like_obj, news_rr_obj]


    if temp_list:
        result_list = [x for j in temp_list for x in j if j]
        result = sorted(chain(result_list), key=attrgetter('create_date'), reverse=True)
        notice_page = try_int(request.GET.get('page', 1), 1)
        notice_counts = len(result)
        notice_page_obj = html_helper.PageInfo(notice_page, notice_counts, 20)
        try:
            notice_result = result[notice_page_obj.start : notice_page_obj.end]
        except Exception:
            notice_result = ''
        ret['notice_result'] = notice_result
        ret['page_list'] = html_helper.ajaxScrollPager(notice_page, notice_page_obj.total_page_counts, notice_filter_url)

        #清除数据
        if not cate:
            models.User_Notification_Check.objects.filter(target_user__id=uid).update(movie_r_like=0, movie_rr=0, focus=0, bbs_r=0, speak_r=0)
            for item in temp_list:
                try:
                    item.update(read=1)
                except Exception:
                    pass
        elif cate == 'history':
            pass
    
    #边栏信息
    ret = user_helper.myState(user_obj, ret)
    ret = user_helper.myAchievement(user_obj, ret)
    ret = user_helper.activeUser(ret)
    ret = user_helper.movieRecommend(ret)
    ret = user_helper.visitHistory(ret, uid, 15)
    
    return render_to_response(html_template, ret, context_instance=RequestContext(request)) 


@loginCheck
def userSettings(request, *args, **kwargs):
    ret = {}
    #个人资料
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    
    
    #边栏信息
    ret = user_helper.myState(user_obj, ret)
    ret = user_helper.myAchievement(user_obj, ret)
    ret = user_helper.activeUser(ret)
    ret = user_helper.movieRecommend(ret)
    ret = user_helper.visitHistory(ret, user_obj.id, 15)
    
    return render_to_response('userinfo/home/home_settings.html', ret, context_instance=RequestContext(request))

def userProfile(request, uid, uname):
    ret = {'is_owner':False}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    profile_user_obj = models.User.objects.filter(id=uid)
    if len(profile_user_obj) == 1:
        true_uname = profile_user_obj[0].username
        if not uname or not uname == true_uname:
            return HttpResponsePermanentRedirect('/user/profile/%s/%s/'%(uid,true_uname))
        #profile基本信息
        ret['profile_user_info'] = profile_user_obj[0]
        ret = user_helper.myAchievement(profile_user_obj[0], ret)
        ret = user_helper.visitHistory(ret, uid, 14)
        total_exp = profile_user_obj[0].exp
        ret['user_level'] = getUserLevel(total_exp)
        ret['exp_percent'] = getUserExpPercent(ret['user_level'], total_exp)
        fans_obj = models.UserFocus.objects.filter(target_user__id=uid)  #空间主人的粉丝
        my_focus_obj = None
        if fans_obj: 
            ret['focused'] = False
            if user_obj:
                for u in fans_obj:
                    if u.origin_user_of_focus.id == user_obj.id:
                        ret['focused'] = True
                        break
                my_focus_obj = models.UserFocus.objects.filter(origin_user_of_focus__id=user_obj.id)
                for u in fans_obj:
                    u.i_focused = False
                    for mu in my_focus_obj:
                        if mu.target_user.id == u.origin_user_of_focus.id:  #我关注的人的ID与关注空间主人的人的ID相同
                            u.i_focused = True
                            break
            ret['his_fans'] = fans_obj
        #判断权限相关
        focused_user_obj = models.UserFocus.objects.filter(origin_user_of_focus__id=uid)  #Ta关注的人
        if focused_user_obj:
            is_focused = False
            if user_obj:
                for u in focused_user_obj:  #当前用户是否被空间主人关注
                    if u.target_user.id == user_obj.id:
                        is_focused = True
                        break
                for u in focused_user_obj:
                    if my_focus_obj:
                        for mu in my_focus_obj:
                            if mu.target_user.id == u.target_user.id:
                                u.i_focused = True
                                break
            ret['his_focused'] = focused_user_obj
        else:
            is_focused = False
            ret['his_focused'] = None
        if user_obj:
            if uid == str(user_obj.id):
                is_owner = True
                ret['is_owner'] = True
                ret['address'] = '我'
            else:
                is_owner = False
                ret['address'] = '空间主人'
                
                #更新访客记录
                visitor_his = models.UserVisitHistory.objects.filter(host__id=uid, visitor=user_obj.id)
                if not visitor_his.count():
                    try:
                        models.UserVisitHistory.objects.create(host=profile_user_obj[0], visitor=user_obj)
                    except Exception:
                        pass
                else:
                    org_times = visitor_his[0].times
                    new_times = org_times + 1
                    try:
                        visitor_his.update(times=new_times, update_date=datetime.datetime.now())
                    except Exception:
                        pass
                
        else:
            is_owner = False
            ret['address'] = '空间主人'
        
        collection_auth = profile_user_obj[0].h_mycollect
        speak_auth = profile_user_obj[0].h_myspeak
        comment_auth = profile_user_obj[0].h_mycomment
        post_auth = profile_user_obj[0].h_mypost
        ret['collection_auth'] = collection_auth
        ret['speak_auth'] = speak_auth
        ret['comment_auth'] = comment_auth
        ret['post_auth'] = post_auth

        #收藏
        movie_col_obj = models.Collect_Movie.objects.filter(user__id=uid).order_by('-create_date')  #Ta收藏的电影
        ret['mc_counts'] = movie_col_obj.count()
        ret['tc_counts'] = models.Collect_Tv.objects.filter(user__id=uid).count()
        ret['ac_counts'] = models.Collect_Anime.objects.filter(user__id=uid).count()
        ret['sc_counts'] = models.Collect_Show.objects.filter(user__id=uid).count()
        if collection_auth == 1 or is_owner:  #判断是否有权限查看
            ret['collection_show'] = True
        elif collection_auth == 2 and is_focused:
            ret['collection_show'] = True
        else:
            ret['collection_show'] = False
        if ret['collection_show']:
            ret['movie_collections'] = movie_col_obj
        else:
            ret['movie_collections'] = None

        #说说
        if speak_auth == 1 or is_owner:  #判断是否有权限查看
            ret['speak_show'] = True
        elif speak_auth == 2 and is_focused:
            ret['speak_show'] = True
        else:
            ret['speak_show'] = False
        if ret['speak_show']:
            his_speak_obj = models.UserSpeak.objects.filter(user__id=uid)  #Ta的说说
            speak_page = try_int(request.GET.get('speak_page', 1), 1)
            speak_counts = his_speak_obj.count()
            #ret['speak_counts'] = speak_counts
            speak_page_obj = html_helper.PageInfo(speak_page, speak_counts, 10)
            try:
                speak_result = his_speak_obj[speak_page_obj.start : speak_page_obj.end]
            except Exception:
                speak_result = ''
            ret['speak_result'] = speak_result
            speak_filter_url = '/user/profile/%s/%s/?speak_page=' %(uid,true_uname)
            ret['speak_page_list'] = html_helper.ajaxScrollPager(speak_page, speak_page_obj.total_page_counts, speak_filter_url)

        #评论
        if comment_auth == 1 or is_owner:  #判断是否有权限查看
            ret['comment_show'] = True
        elif comment_auth == 2 and is_focused:
            ret['comment_show'] = True
        else:
            ret['comment_show'] = False
        if ret['comment_show']:
            comment_result = []
            movie_comment_obj = models.MovieReply.objects.filter(user__id=uid)
            tv_comment_obj = models.TvReply.objects.filter(user__id=uid)
            anime_comment_obj = models.AnimeReply.objects.filter(user__id=uid)
            show_comment_obj = models.ShowReply.objects.filter(user__id=uid)
            news_comment_obj = models.NewsReply.objects.filter(user__id=uid)
            comment_tmp_list = [movie_comment_obj,tv_comment_obj,anime_comment_obj,
                                show_comment_obj,news_comment_obj]
            for obj in comment_tmp_list:
                if obj:
                    for item in obj:
                        comment_result.append(item)
            comment_result = sorted(chain(comment_result), key=attrgetter('create_date'), reverse=True)
            comment_page = try_int(request.GET.get('comment_page', 1), 1)
            comment_counts = len(comment_result)
            comment_page_obj = html_helper.PageInfo(comment_page, comment_counts, 10)
            try:
                comment_result = comment_result[comment_page_obj.start : comment_page_obj.end]
            except Exception:
                comment_result = ''
            ret['comment_result'] = comment_result
            comment_filter_url = '/user/profile/%s/%s/?comment_page=' %(uid,true_uname)
            ret['comment_page_list'] = html_helper.ajaxScrollPager(comment_page, comment_page_obj.total_page_counts, comment_filter_url)
        
        
        #帖子
        if post_auth == 1 or is_owner:  #判断是否有权限查看
            ret['post_show'] = True
        elif post_auth == 2 and is_focused:
            ret['post_show'] = True
        else:
            ret['post_show'] = False
        if ret['post_show']:
            post_result = []
            post_obj = models.Post.objects.filter(user__id=uid)
            post_reply_obj = models.PostReply.objects.filter(user__id=uid)
            post_layer_reply_obj = models.PostLayerReply.objects.filter(user__id=uid)
            post_all_list = [post_obj,post_reply_obj,post_layer_reply_obj]
            for obj in post_all_list:
                if obj:
                    for item in obj:
                        post_result.append(item)
            post_result = sorted(chain(post_result), key=attrgetter('create_date'), reverse=True)
            post_page = try_int(request.GET.get('post_page', 1), 1)
            post_counts = len(post_result)
            post_page_obj = html_helper.PageInfo(post_page, post_counts, 10)
            try:
                post_result = post_result[post_page_obj.start : post_page_obj.end]
            except Exception:
                post_result = ''
            ret['post_result'] = post_result
            post_filter_url = '/user/profile/%s/%s/?post_page=' %(uid,true_uname)
            ret['post_page_list'] = html_helper.ajaxScrollPager(post_page, post_page_obj.total_page_counts, post_filter_url)
        
    elif len(profile_user_obj) == 0:
        raise Http404
    else:
        pass
    return render_to_response('userinfo/profile/profile.html', ret, context_instance=RequestContext(request)) #/user/USER_NAME/profile/ 用户详情页


def c_show(uid,cate,is_owner):
    result_list = [is_owner]
    if cate == 'movie':
        result_obj = models.Collect_Movie.objects.filter(user__id=uid).values('movie_id', 'create_date')
        if result_obj.count():
            for item in result_obj:
                c_obj = models.Movie.objects.filter(id=item['movie_id']).values('id','ch_name','year','intro','poster','score')
                list(c_obj)[0]['c_date'] = item['create_date'].strftime('%Y-%m-%d %H:%M')
                if is_owner:
                    list(c_obj)[0]['is_owner'] = True
                result_list.append(list(c_obj)[0])
    elif cate == 'tv':
        result_obj = models.Collect_Tv.objects.filter(user__id=uid).values('tv_id', 'create_date')
        if result_obj.count():
            for item in result_obj:
                c_obj = models.Tv.objects.filter(id=item['tv_id']).values('id','ch_name','year','intro','poster','score')
                list(c_obj)[0]['c_date'] = item['create_date'].strftime('%Y-%m-%d %H:%M')
                if is_owner:
                    list(c_obj)[0]['is_owner'] = True
                result_list.append(list(c_obj)[0])
    elif cate == 'anime':
        result_obj = models.Collect_Anime.objects.filter(user__id=uid).values('anime_id', 'create_date')
        if result_obj.count():
            for item in result_obj:
                c_obj = models.Anime.objects.filter(id=item['anime_id']).values('id','ch_name','year','intro','poster','score')
                list(c_obj)[0]['c_date'] = item['create_date'].strftime('%Y-%m-%d %H:%M')
                if is_owner:
                    list(c_obj)[0]['is_owner'] = True
                result_list.append(list(c_obj)[0])
    elif cate == 'show':
        result_obj = models.Collect_Show.objects.filter(user__id=uid).values('show_id', 'create_date')
        if result_obj.count():
            for item in result_obj:
                c_obj = models.Show.objects.filter(id=item['show_id']).values('id','ch_name','year','intro','poster','score')
                list(c_obj)[0]['c_date'] = item['create_date'].strftime('%Y-%m-%d %H:%M')
                if is_owner:
                    list(c_obj)[0]['is_owner'] = True
                result_list.append(list(c_obj)[0])
    return result_list            
    

def userCollection(request, uname,uid, cate):  #uid为当前查看的profile的uid
    if request.method == 'POST':
        cate_list = ['movie', 'tv', 'anime', 'show']
        if cate in cate_list and uid.isdigit():
            ret = {}
            profile_user_obj = models.User.objects.filter(id=uid)
            if profile_user_obj.count() == 1:
                try:
                    session_uid = request.session['login_user_id']
                except Exception:
                    session_uid = None
                #is_owner
                if session_uid:
                    if uid == str(session_uid):
                        is_owner = 1
                    else:
                        is_owner = False
                else:
                    is_owner = False
                #auth
                c_auth = profile_user_obj[0].h_mycollect
                if c_auth == 1:  #直接显示
                    result_list = c_show(uid, cate, is_owner)
                    result_list = json.dumps(result_list, cls=CJsonEncoder)
                    return HttpResponse(result_list)
                else:
                    if session_uid:
                        #is_focused
                        focused_user_obj = models.UserFocus.objects.filter(origin_user_of_focus__id=uid)
                        if focused_user_obj:
                            is_focused = False
                            for item in focused_user_obj:  #当前用户是否被空间主人关注
                                if session_uid:
                                    if item.target_user.id == session_uid:
                                        is_focused = True
                                        break
                        else:
                            is_focused = False
                        #show
                        if is_owner or c_auth == 2 and is_focused:
                            result_list = c_show(uid, cate, is_owner)
                            result_list = json.dumps(result_list, cls=CJsonEncoder)

                            return HttpResponse(result_list)
                        else:  #is not owner , c_auth =2 and is not focused, c_auth =0
                            if c_auth == 2 and not is_focused:
                                ret['msg'] = '502'
                            elif c_auth == 0:
                                ret['msg'] = '501'
                        return HttpResponse(json.dumps(ret))    

                    else:
                        ret['msg'] = '401'  #设置了权限，且未登录
                        return HttpResponse(json.dumps(ret))
            else:
                #ret['msg'] = '24'  #该用户账号不存在
                raise Http404
        else:
            ret['msg'] = '302'  #前端数据错误

        return HttpResponse(json.dumps(ret))
    else:
        raise Http404
        

def collect(request):
    ret = {}
    if request.method == 'POST':
        xid = request.POST.get('xid', None)
        cate = request.POST.get('cate', None)

        #获取user id
        try:
            uid = request.session['login_user_id']
        except Exception:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        #获取user对象
        try:
            user_obj = models.User.objects.get(id=uid)
        except Exception:
            ret['msg'] = '24'
            return HttpResponse(json.dumps(ret))

        if xid and xid.isdigit():
            if cate == 'movie':
                try:
                    #判断是否存在
                    collected_movies = models.Collect_Movie.objects.filter(movie__id=xid, user__id=uid)
                    if collected_movies.count() > 0:
                        ret['msg'] = '104'  #已存在
                        return HttpResponse(json.dumps(ret))
                    #存入数据库
                    collecting_obj = models.Movie.objects.get(id=xid)
                    #user_obj.collect_movie.add(collecting_obj)
                    models.Collect_Movie.objects.create(user=user_obj, movie=collecting_obj)
                    ret['msg'] = 'success'
            
                except Exception:
                    ret['msg'] = '101'
                    return HttpResponse(json.dumps(ret))
            elif cate == 'tv':
                try:
                    collected_tvs = models.Collect_Tv.objects.filter(tv__id=xid, user__id=uid)
                    if collected_tvs.count() > 0:
                        ret['msg'] = '104'  #已存在
                        return HttpResponse(json.dumps(ret))
                    #存入数据库
                    collecting_obj = models.Tv.objects.get(id=xid)
                    models.Collect_Tv.objects.create(user=user_obj, tv=collecting_obj)
                    ret['msg'] = 'success'
                except Exception:
                    ret['msg'] = '101'
                    return HttpResponse(json.dumps(ret))
            elif cate == 'anime':
                try:
                    collected_animes = models.Collect_Anime.objects.filter(anime__id=xid, user__id=uid)
                    if collected_animes.count() > 0:
                        ret['msg'] = '104'  #已存在
                        return HttpResponse(json.dumps(ret))
                    #存入数据库
                    collecting_obj = models.Anime.objects.get(id=xid)
                    models.Collect_Anime.objects.create(user=user_obj, anime=collecting_obj)
                    ret['msg'] = 'success'
                except Exception:
                    ret['msg'] = '101'
                    return HttpResponse(json.dumps(ret))
            elif cate == 'show':
                try:
                    collected_shows = models.Collect_Show.objects.filter(show__id=xid, user__id=uid)
                    if collected_shows.count() > 0:
                        ret['msg'] = '104'  #已存在
                        return HttpResponse(json.dumps(ret))
                    #存入数据库
                    collecting_obj = models.Show.objects.get(id=xid)
                    models.Collect_Show.objects.create(user=user_obj, show=collecting_obj)
                    ret['msg'] = 'success'
                except Exception:
                    ret['msg'] = '101'
                    return HttpResponse(json.dumps(ret))
            else:
                ret['msg'] = '302'
        else:
            ret['msg'] = '302'  #前端数据错误
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404

def cancelCollect(request):
    ret = {}
    if request.method == 'POST':
        cate = request.POST.get('cate', None)
        xid = request.POST.get('xid', None)
        mid = tid = aid = sid = None

        if cate == 'movie':
            mid = xid
        elif cate == 'tv':
            tid = xid
        elif cate == 'anime':
            aid = xid
        elif cate == 'show':
            sid = xid
        #获取user id

        try:
            uid = request.session['login_user_id']
        except Exception:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        #获取user对象
        try:
            user_obj = models.User.objects.get(id=uid)
        except Exception:
            ret['msg'] = '24'
            return HttpResponse(json.dumps(ret))
        
        if mid and mid.isdigit():
            try:
                #判断是否存在
                collected_movies = models.Collect_Movie.objects.filter(movie__id=mid, user__id=uid)  #该用户收藏的所有电影
                if len(collected_movies) > 0:
                    collected_movies.delete()  #删除条目
                    ret['cur_counts'] = models.Collect_Movie.objects.filter(user__id=uid).count()
                    ret['msg'] = 'success'
                else:
                    ret['msg'] = '103'  #不存在不能删除
            except Exception:
                ret['msg'] = '101'
            return HttpResponse(json.dumps(ret))
        elif tid and tid.isdigit():
            try:
                tv_collect_obj = models.Collect_Tv.objects.filter(tv__id=tid, user__id=uid)
                if len(tv_collect_obj) > 0:
                    tv_collect_obj.delete()  #删除条目
                    ret['msg'] = 'success'
                    ret['cur_counts'] = models.Collect_Tv.objects.filter(user__id=uid).count()
                else:
                    ret['msg'] = '103'  #不存在不能删除
            except Exception:
                ret['msg'] = '101'
            return HttpResponse(json.dumps(ret))
        elif aid and aid.isdigit():
            try:
                anime_collect_obj = models.Collect_Anime.objects.filter(anime__id=aid, user__id=uid)
                if len(anime_collect_obj) > 0:
                    anime_collect_obj.delete()  #删除条目
                    ret['msg'] = 'success'
                    ret['cur_counts'] = models.Collect_Anime.objects.filter(user__id=uid).count()
                else:
                    ret['msg'] = '103'  #不存在不能删除
            except Exception:
                ret['msg'] = '101'
            return HttpResponse(json.dumps(ret))
        elif sid and sid.isdigit():
            try:
                show_collect_obj = models.Collect_Show.objects.filter(show__id=aid, user__id=uid)
                if len(show_collect_obj) > 0:
                    show_collect_obj.delete()  #删除条目
                    ret['msg'] = 'success'
                    ret['cur_counts'] = models.Collect_Show.objects.filter(user__id=uid).count()
                else:
                    ret['msg'] = '103'  #不存在不能删除
            except Exception:
                ret['msg'] = '101'
            return HttpResponse(json.dumps(ret))
        else:
            ret['msg'] = '302'  #前端数据错误
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404

def focus(request):
    ret = {}
    if request.method == 'POST':
        target_uid = request.POST.get('target_uid', '')
        uid = request.session.get('login_user_id', '')

        if not uid:
            ret['msg'] = '401'  #用户未登录
            return HttpResponse(json.dumps(ret))
        
        if target_uid.isdigit():
            target_user_obj = models.User.objects.filter(id=target_uid)
            if not target_user_obj:
                ret['msg'] = '902'  #用户不存在
                return HttpResponse(json.dumps(ret))
        else:
            ret['msg'] = '302'  #前端传入数据类型错误
            return HttpResponse(json.dumps(ret))

        if not target_user_obj[0].h_focusme:
            ret['msg'] = '402'  #用户不允许他人关注
            return HttpResponse(json.dumps(ret))
        
        if uid == target_uid:
            ret['msg'] = '911'  #自己不能关注自己
            return HttpResponse(json.dumps(ret))
        
        result = models.UserFocus.objects.filter(origin_user_of_focus__id=uid, target_user__id=target_uid)
        if result.count() == 1:  #已关注即取消
            if not result[0].read:  #消息未读，通知数需要减1
                notice_obj = models.User_Notification_Check.objects.filter(target_user__id=target_uid)
                if notice_obj.count():
                    notice_obj.update(focus = notice_obj[0].focus - 1)
            result.delete()
            ret['msg'] = 'cancel_success'  
            return HttpResponse(json.dumps(ret))
        elif result.count() == 0:
            user_obj = models.User.objects.filter(id=uid)
            if not user_obj.count():
                ret['msg'] = '902'  #用户不存在(target_user)
                return HttpResponse(json.dumps(ret))
            #1,首先创建Focus条目
            try:
                models.UserFocus.objects.create(origin_user_of_focus=user_obj[0], target_user=target_user_obj[0])
            except Exception:
                ret['msg'] = '101'  #数据库写入错误
                return HttpResponse(json.dumps(ret))
            #2,通知的Check表查询
            check_obj = models.User_Notification_Check.objects.filter(target_user__id=target_uid)
            if check_obj.count() == 1:  #check表条目应该在注册时就被创建
                try:
                    #存在即更新
                    check_obj.update(focus=check_obj[0].focus + 1)
                    ret['msg'] = 'success'
                except Exception:
                    ret['msg'] = '101'
                return HttpResponse(json.dumps(ret))
            elif check_obj.count() == 0:  #以防万一
                try:
                    models.User_Notification_Check.objects.create(target_user=target_user_obj[0], focus=1)
                    #创建focus细节条目
                    ret['msg'] = 'success'
                except Exception:
                    ret['msg'] = '101'
                return HttpResponse(json.dumps(ret))
            else:  #重复数据
                ret['msg'] = '102'
  
        else:
            ret['msg'] = '102'  #数据重复


        return HttpResponse(json.dumps(ret))
    else:
        raise Http404
    

def modifySettings(request):
    if request.method == 'POST':
        ret = {'msg':'false'}
        gender = request.POST.get('gender', None)
        #new_sign = request.POST.get('sign', None)
        #new_location = request.POST.get('location', None)
        #new_birthday = request.POST.get('birthday', None)
        user_id = request.session.get('login_user_id', None)
        new_val = request.POST.get('new_val', None)
        tag = request.POST.get('tag', None)
        if not user_id:
            ret['msg'] = '请重新登录'
            return HttpResponse(json.dumps(ret))
        else:
            user_obj = models.User.objects.filter(id=user_id)
            if user_obj.count() == 1:
                if gender:
                    if gender == 'male':
                        user_obj.update(gender=0)
                        ret['msg'] = 'success'
                    elif gender == 'female':
                        user_obj.update(gender=1)
                        ret['msg'] = 'success'
                    else:
                        ret['msg'] = '302'
                elif tag == 'sign':
                    if len(new_val.encode('gbk'))>32:
                        ret['msg'] = '长度不能超过32个中文'  #内容过长
                    else:
                        user_obj.update(mysign=new_val)
                        ret['msg'] = 'success'
                elif tag == 'location':
                    if len(new_val.encode('gbk'))>32:
                        ret['msg'] = '长度不能超过32个中文'  #内容过长
                    else:
                        user_obj.update(location=new_val)
                        ret['msg'] = 'success'
                elif tag == 'birthday':
                    try:
                        date_val = datetime.datetime.strptime(new_val, '%Y-%m-%d').date()
                    except Exception:
                        ret['msg'] = '302'
                        return HttpResponse(json.dumps(ret))
                    user_obj.update(birthday=date_val)
                    ret['msg'] = 'success'
                elif tag == 'h_recvpush':
                    user_obj.update(h_recvpush=int(new_val))
                elif tag == 'h_focusme':
                    user_obj.update(h_focusme=int(new_val))
                elif tag == 'h_mycollect':
                    user_obj.update(h_mycollect=int(new_val))
                elif tag == 'h_mycomment':
                    user_obj.update(h_mycomment=int(new_val))
                elif tag == 'h_myspeak':
                    user_obj.update(h_myspeak=int(new_val))
                elif tag == 'h_mypost':
                    user_obj.update(h_mypost=int(new_val))
            else:
                ret['msg'] = '101'
            return HttpResponse(json.dumps(ret))
    else:
        raise Http404

@csrf_exempt  
def upload_bg(request):
    if request.method == 'POST':
        ret = {}
        uid = request.session['login_user_id']
        photo = request.FILES.getlist('qqfile', '')
        photo_name = request.POST.get('qqfilename')
        #图片处理及保存

        photo_suffix = re.findall('.*(\.[a-zA-Z]{3,4}$)', photo_name)[0]
        try:
            profile_bg,info_bg,usercard_bg = images_helper.userBgProccess(photo[0], photo_suffix, uid)
        except Exception:
            ret['error'] = '图片处理出错'
            return HttpResponse(json.dumps(ret))

        user_obj = models.User.objects.filter(id=uid)
        print user_obj
        old_bgs = (str(user_obj[0].profile_bg), str(user_obj[0].usercard_bg), str(user_obj[0].info_bg))
        #更新数据库
        user_obj.update(profile_bg=profile_bg, usercard_bg=usercard_bg, info_bg=info_bg)
        #删除旧的背景
        for item in old_bgs:
            if item:
                try:
                    os.remove(os.path.join(BASE_DIR+item))
                except Exception,e:
                    print e
                    #pass
        ret['success'] = True
        return HttpResponse(json.dumps(ret))

    else:
        raise Http404

@csrf_exempt
def upload_speak_img(request):
    if request.method == 'POST':
        ret = {}
        user_id = request.session['login_user_id']
        photo = request.FILES.getlist('qqfile', '')
        qquuid = request.POST.get('qquuid').replace('-','')

        if len(photo)==1:
            #临时表中同一用户条目不超过20
            photo_tmp_obj = models.UserSpeakTemp.objects.filter(user__id=user_id)
            if len(photo_tmp_obj) > 9:
                ret['error'] = '配图最多为9张'
                return HttpResponse(json.dumps(ret))
            #获取文件名，并重命名
            org_photo_name = request.POST.get('qqfilename')
            photo_path = '/media/speak/%s/'%(user_id)
            name_result = images_helper.genSPName(org_photo_name, qquuid)

            #图片处理及保存
            try:
                msg = images_helper.photoProccess(photo[0], photo_path, name_result)

                if msg == 'makedirwrong':
                    ret['error'] = '服务器错误'#'创建相册出错'
                    return HttpResponse(json.dumps(ret))
            except Exception:
                ret['error'] = '图片处理出错'
                return HttpResponse(json.dumps(ret))
            
            #记录临时表
            try:
                user_obj = models.User.objects.get(id = user_id)
                models.UserSpeakTemp.objects.create(user = user_obj, speak_photo = photo_path+name_result, qquuid=qquuid)
                ret['success'] = True
            except Exception:
                ret['success'] = False
            return HttpResponse(json.dumps(ret))
        else:
            ret['error'] = '未添加图片'
            return HttpResponse(json.dumps(ret))

    else:
        raise Http404

@csrf_exempt
def deleteSpeakImg(request):
    if request.method == 'POST':
        uid = request.session['login_user_id']
        qquuid = request.POST.get('qquuid').replace('-','')
        temp_images = models.UserSpeakTemp.objects.filter(user__id=uid)
        for item in temp_images:
            photo_path = str(item.speak_photo)
            if qquuid in photo_path:
                thumb_path = re.sub(r'(^/media/speak/\d+/)(.*)$', r'\1thumbs/\2', photo_path)
                #删除图片及缩略图
                try:
                    os.remove(os.path.join(BASE_DIR + photo_path))
                    os.remove(os.path.join(BASE_DIR + thumb_path))
                    models.UserSpeakTemp.objects.filter(user__id=uid, speak_photo=photo_path).delete()
                    return HttpResponse('ok')
                except Exception:
                    pass
                #删除临时表条目
                
    else:
        raise Http404
    
def publishSpeak(request):
    ret = {}
    if request.method == 'POST':
        try:
            user_id = request.session['login_user_id']
        except Exception:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        ret, user_obj = loginInfo(request, ret)
        speak_content = request.POST.get('content', '')
        if not speak_content:
            ret['msg'] = '901'
            return HttpResponse(json.dumps(ret))
        #拿到相关图片数据
        speak_content = htmlContentFilter(speak_content, 'media')
        photo_tmp_obj = models.UserSpeakTemp.objects.filter(user__id=user_id)
        photo_str = ''
        if photo_tmp_obj > 0: #临时表中有图片
            for item in photo_tmp_obj:
                photo_str += (str(item.speak_photo) + ' ')  #整合图片地址
            try:
                models.UserSpeak.objects.create(content = speak_content, user = user_obj, 
                                            speak_photo = photo_str)
            except Exception:
                ret['msg'] = '101'  #数据库写入错误
                return HttpResponse(json.dumps(ret))
            #写入数据库完成后，删除临时表相关条目
            photo_tmp_obj.delete()
        else:  #只有文本内容
            try:
                models.UserSpeak.objects.create(content = speak_content, user = user_obj)
            except Exception:
                ret['msg'] = '101'  #数据库写入错误
                return HttpResponse(json.dumps(ret))
        ret['msg'] = 'success'
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404

def likeSpeak(request):
    if request.method == 'POST':
        ret = {}
        try:
            uid = request.session['login_user_id']
        except Exception:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        
        sid = request.POST.get('sid')
        if sid.isdigit():
            like_obj = models.User_Speak_Like.objects.filter(speak_of_like__id=sid, user__id=uid)
            if not like_obj.count():
                try:
                    speak_obj = models.UserSpeak.objects.get(id=sid)
                    user_obj = models.User.objects.get(id=uid)
                except Exception:
                    ret['msg'] = '103'
                    return HttpResponse(json.dumps(ret))
                try:
                    models.User_Speak_Like.objects.create(speak_of_like=speak_obj, user=user_obj)
                    ret['msg'] = 'success'
                    
                    ret['counts'] = models.User_Speak_Like.objects.filter(speak_of_like__id=sid).count()
                except Exception:
                    ret['msg'] = '101'
            else:
                ret['msg'] = '910'  #已点赞
        else:
            ret['msg'] = '302'
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404

def submitSpeakReply(request):
    if request.method == 'POST':
        ret = {}
        content = request.POST.get('content')
        content = htmlContentFilter(content, 'static')
        sid = request.POST.get('sid')
        ret, user_obj = loginInfo(request, ret)
        if not sid.isdigit():
            ret['msg'] = '302'
            return HttpResponse(json.dumps(ret))
        try:
            speak_obj = models.UserSpeak.objects.get(id=sid)
        except Exception:
            speak_obj = None
        if speak_obj:
            new_speak_reply = models.UserSpeakReply.objects.create(content=content, speak_of_reply=speak_obj, user=user_obj)
            ret['msg'] = 'success'
            ret['uid'] = user_obj.id
            ret['uname'] = user_obj.username
            ret['uthumb'] = str(user_obj.thumb_s)
            ret['ucontent'] = new_speak_reply.content
            ret['rid'] = new_speak_reply.id
        else:
            ret['msg'] = '103'  #记录不存在
        return HttpResponse(json.dumps(ret))

    else:
        raise Http404

def submitSpeakRR(request):
    if request.method =='POST':
        ret = {}
        content = request.POST.get('content', None)
        content = htmlContentFilter(content, 'static')
        rid = request.POST.get('rid', None)
        target_uid = request.POST.get('target_uid', None)
        if rid.isdigit() and target_uid.isdigit():
            try:
                reply_obj = models.UserSpeakReply.objects.get(id=rid)
                target_user_obj = models.User.objects.get(id=target_uid)
            except Exception:
                ret['msg'] = '103'
                return HttpResponse(json.dumps(ret))
            ret, user_obj = loginInfo(request, ret)
            if user_obj:
                pass
            else:
                ret['msg'] = '401'
                return HttpResponse(json.dumps(ret))
            try:
                rr_obj = models.User_Speak_RR.objects.create(content=content, speak_reply=reply_obj,
                                                user=user_obj, target_user=target_user_obj )
                ret['uid'] = user_obj.id
                ret['uname'] = user_obj.username
                ret['uthumb'] = str(user_obj.thumb_s)
                ret['rr_content'] = content
                ret['target_uname'] = target_user_obj.username
                ret['rrid'] = rr_obj.id
                ret['msg'] = 'success'
            except Exception:
                ret['msg'] = '101'
        else:
            ret['msg'] = '302'
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404
    
def deleteSpeak(request):
    if request.method == 'POST':
        ret = {}
        sid = request.POST.get('sid', None)
        if sid.isdigit():
            try:
                uid = str(request.session['login_user_id'])
            except Exception:
                ret['msg'] = '401'
                return HttpResponse(json.dumps(ret))
            speak_to_del_obj = models.UserSpeak.objects.filter(id=sid, user__id=uid)
            try:
                if speak_to_del_obj.count():
                    
                    photo_str = speak_to_del_obj[0].speak_photo
                    if photo_str:
                        photo_list = photo_str.split()
                        for photo_path in photo_list:
                            thumb_path = re.sub(r'(^/media/speak/\d+/)(.*)$', r'\1thumbs/\2', photo_path)
                            try:
                                os.remove(os.path.join(BASE_DIR + photo_path))
                                os.remove(os.path.join(BASE_DIR + thumb_path))
                            except Exception:
                                pass

                    try:
                        speak_to_del_obj.delete()
                    except Exception:
                        ret['msg'] = '101'
                        return HttpResponse(json.dumps(ret))
                    ret['msg'] = 'success'

            except Exception:
                pass
            
        else:
            ret['msg'] = '302'
        return HttpResponse(json.dumps(ret))
            
    else:
        raise Http404
    
def deleteSpeakReply(request):
    if request.method == 'POST':
        ret = {}
        rid = request.POST.get('rid', None)
        if rid.isdigit():
            try:
                uid = str(request.session['login_user_id'])
            except Exception:
                ret['msg'] = '401'
                return HttpResponse(json.dumps(ret))
            try:
                reply_to_del_obj = models.UserSpeakReply.objects.filter(id=rid, user__id=uid)
                if reply_to_del_obj.count():
                    reply_to_del_obj.delete()
                    ret['msg'] = 'success'
                else:
                    ret['msg'] = '103'
            except Exception:
                ret['msg'] = '301'
        else:
            ret['msg'] = '302'
        return HttpResponse(json.dumps(ret))
            
    else:
        raise Http404

def deleteSpeakRR(request):
    if request.method == 'POST':
        ret = {}
        rrid = request.POST.get('rrid', None)
        if rrid.isdigit():
            try:
                uid = str(request.session['login_user_id'])
            except Exception:
                ret['msg'] = '401'
                return HttpResponse(json.dumps(ret))
            try:
                rr_to_del_obj = models.User_Speak_RR.objects.filter(id=rrid, user__id=uid)
                if rr_to_del_obj.count():
                    rr_to_del_obj.delete()
                    ret['msg'] = 'success'
                else:
                    ret['msg'] = '103'
            except Exception:
                ret['msg'] = '301'
        else:
            ret['msg'] = '302'
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404  

def uploadAvatar(request):
    if request.method == 'POST':
        ret = {'error':'', 'success':False}
        ret, user_obj = loginInfo(request, ret)
        try:
            user_id = str(request.session['login_user_id'])
        except Exception:
            ret['error'] = '请登录'
        
        avatar_dir = '/media/avatar/' + user_id + '/'
        
        avatar_dataurl = request.POST.get('avatar')
        #avatar_base64 = re.findall('^data\:image.*?base64\,(.*)$', avatar_dataurl, re.S)[0]
        result = images_helper.avatarProcess(avatar_dataurl, user_id)
        if 'avatar_' in result:
            ret['success'] = True
            
            if not str(user_obj.thumb_s) == default_avatar_s:
                for item in (str(user_obj.thumb_s), str(user_obj.thumb_m), str(user_obj.thumb_l)):
                    try:
                        os.remove(os.path.join(BASE_DIR + item))
                    except Exception:
                        pass
            la = avatar_dir + result.replace('40x40', '100x100')
            ma = avatar_dir + result.replace('40x40', '60x60')
            sa = avatar_dir + result
            ret['avatar_l'] = la
            ret['avatar_s'] = sa
            user_obj.thumb_l = la
            user_obj.thumb_m = ma
            user_obj.thumb_s = sa
            user_obj.save()
        elif result == 'makedirwrong':
            ret['error'] = '创建相册出错'
        elif result == 'IOerror':
            ret['error'] = 'IO错误'
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404

def uploadPhoto(request):
    ret = {}
    if request.method == 'POST':
        try:
            user_id = request.session['login_user_id']
        except Exception:
            ret['error'] = '请登录'
            return HttpResponse(json.dumps(ret))
        #获取对象集合
        photos = request.FILES.getlist('qqfile')
        if photos:
            for photo in photos:
                #photo_name = photo.name #原始文件名
                photo_name = request.POST.get('qqfilename') #用户改过后的文件名
                photo_path = '/media/photo/%s/'%(user_id)
                #查询该用户图片数
                #user_count = models.UserPhoto.objects.filter(owner__id=user_id).count()
                
                #判断数据库中文件名是否重复
                try:
                    user_obj = models.User.objects.get(id=user_id)
                    photo_counts = models.UserPhoto.objects.filter(photo=photo_path+photo_name).count()
                    if photo_counts > 0:  #判断文件名重复
                        ret['error'] = '文件名已存在'
                        return HttpResponse(json.dumps(ret))
                except Exception:
                    pass
                #图片处理及保存
                try:
                    msg = images_helper.photoProccess(photo, photo_path, photo_name)
                    if msg == 'makedirwrong':
                        ret['error'] = '创建相册出错'
                        return HttpResponse(json.dumps(ret))
                except Exception:
                    ret['error'] = '图片处理出错'
                    return HttpResponse(json.dumps(ret))
                
                #写入数据库
                try:
                    user_obj = models.User.objects.get(id=user_id)
                    models.UserPhoto.objects.create(photo=photo_path+photo_name, name=photo_name, \
                                                    thumb=photo_path+'thumbs/'+photo_name, owner=user_obj, desc=photo_name)
                    ret['success'] = True
                except Exception:
                    ret['success'] = False
            return HttpResponse(json.dumps(ret))
        
def managePhoto(request):
    pass


def userPolling(request):
    if request.method == 'POST':
        ret = {}
        try:
            uid = request.session['login_user_id']
        except Exception:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        
        user_objs = models.User.objects.filter(id=uid)
        if not user_objs.count():
            ret['msg'] = '103'
            return HttpResponse(json.dumps(ret))
        
        user_obj = user_objs[0]
        if not user_obj.h_recvpush:  #设置不接收推送
            ret['msg'] = '402'
            return HttpResponse(json.dumps(ret))
        
        #新消息通知
        p_res = models.User_Notification_Check.objects.filter(target_user__id=uid)
        if len(p_res) == 1:  #条目存在
            p_res = p_res[0]
            item_dict = {'movie_r_like':p_res.movie_r_like, 'movie_rr':p_res.movie_rr, 
                         'focus':p_res.focus, 'new_msg':p_res.msg, 'bbs_r':p_res.bbs_r}
            for k,v in item_dict.items():
                if v > 0:
                    #if k == 'movie_r_like':
                        #result = models.User_MovieRR_Notification.objects.filter(target_user__id=uid)
                        #if result.count() > 0:
                            #ret[k] = 
                    ret[k] = v
                else:
                    ret[k] = 0
                        
        elif len(p_res) == 0:
            try:
                models.User_Notification_Check.objects.create(target_user=user_obj)
            except Exception:
                ret['msg'] = '101'

        else: #条目大于1，异常
            ret['msg'] = '102'

        return HttpResponse(json.dumps(ret))

    else:
        raise Http404

def replyCheckLogin(request):
    ret = {'logined':False}
    uid = request.session.get('login_user_id', None)
    if uid:
        ret['logined'] = True
    return HttpResponse(json.dumps(ret))

