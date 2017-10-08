#_*_coding:UTF-8_*_
from django.shortcuts import render_to_response
from movie import models
from django.http.response import HttpResponse, Http404
import json
from django.template.context import RequestContext
#from movie import forms
from packages import html_helper, html_helper_search
from packages.user_helper import expAdd
from packages.general import try_int,loginInfo, htmlContentFilter, CJsonEncoder
from packages.images_helper import genBPName, bbsImgProccess, genPostImgThumb
import re,os
from MovieSite.settings import BASE_DIR
from packages.templatetags import my_tags

# Create your views here.

def deleteImg(rel_path):
    try:
        os.remove(os.path.join(BASE_DIR + rel_path))
    except Exception:
        pass
    
def getHotPost():
    hot_list = []
    hot_posts_obj = models.Post.objects.all().order_by('-create_date')#.values('id','title','user','board')
    for item in hot_posts_obj:
        if item.post_reply.all().count() >= 5:
            hot_list.append(item)
            if len(hot_list) == 5:
                break
    return hot_list

def bbsIndex(request):
    ret = {'login_status':False}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    
    #hot
    ret['hot_posts'] = getHotPost()
    
    #posts statistics
    board_dict = {'movie':('mp','mpr'), 'tv':('tp','tpr'), 'anime':('ap','apr'), 'show':('sp','spr'),
                 'notification':('np','npr'), 'relaxing':('rp','rpr'), 'feedback':('fp','fpr')}
    for board,item in board_dict.items():
        post_count = models.Post.objects.filter(board=board).count()
        reply_count = models.PostReply.objects.filter(post__board=board).count()
        ret[item[0]] = post_count
        ret[item[1]] = post_count + reply_count

    return render_to_response('bbs/bbs_index.html', ret, context_instance=RequestContext(request))
    

def boardIndex(request):
    ret = {'login_status':False}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    b = request.GET.get('b', None)
    page = try_int(request.GET.get('p', 1), 1)
    #board
    b_list = ['movie','tv','anime','show','notification','feedback','relaxing']
    if not b in b_list:
        raise Http404
        #return render_to_response('404.html')
    else:
        ret['board'] = b
        
    # 计数，排序
    posts_obj = models.Post.objects.filter(board=b).order_by('-last_replied_date')
    post_counts = posts_obj.count()
    ret['post_counts'] = post_counts

    #分页
    pageObj = html_helper.PageInfo(page, post_counts, 20)
    try:
        posts_obj = posts_obj[pageObj.start : pageObj.end]
    except Exception:
        posts_obj = ''
     
    ret['posts'] = posts_obj
    
    filter_url = '/bbs/board/?b=%s&p='%b
    page_list = html_helper.Pager(page, pageObj.total_page_counts, filter_url)
    ret['page_list'] = page_list

    #hot
    ret['hot_posts'] = getHotPost()
    
    
    
    
    
    return render_to_response('bbs/bbs_board_index.html', ret, context_instance=RequestContext(request))

def postDetail(request, pid):
    ret = {'login_status':False, 'post':None}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    #post
    post_obj = models.Post.objects.filter(id=pid)
    if not post_obj.count():
        raise Http404
    else:
        old_visit_counts = post_obj[0].visit_counts
        post_obj.update(visit_counts=old_visit_counts + 1)
        
    ret['post'] = post_obj[0]
    ret['board'] = post_obj[0].board

    #post reply
    post_replies_obj = models.PostReply.objects.filter(post__id=pid).order_by('create_date')
    reply_counts = post_replies_obj.count()
    if reply_counts <=9:
        ret['cur_page'] = 1
    else:
        #分页
        page = try_int(request.GET.get('p', 1), 1)
        ret['cur_page'] = page
        ret['layer_start'] = (page-1)*10 + 1  #需在模板中用forloop.counter0 
        ret['post_counts'] = reply_counts
        pageObj = html_helper_search.PageInfo(page, reply_counts, 10, 9)  #加1为了使分页加上1楼计算
        print pageObj.start, pageObj.end
        try:
            post_replies_obj = post_replies_obj[pageObj.start : pageObj.end]
        except Exception:
            post_replies_obj = ''
        filter_url = '/bbs/post/%s/?p='%pid
        page_list = html_helper_search.Pager(page, pageObj.total_page_counts, filter_url)
        ret['page_list'] = page_list
    
    #for item in post_replies_obj:
        #item.content = htmlContentFilter(item.content)
    ret['post_replies'] = post_replies_obj
    focused_user_list = []
    if user_obj:
        uid = user_obj.id
        focused_obj = models.UserFocus.objects.filter(origin_user_of_focus__id=uid)  #我关注的
        for item in focused_obj:
            focused_user_list.append(item.target_user.id)
        #print focused_user_list
        ret['focused_user_list'] = focused_user_list
    #hot 
    ret['hot_posts'] = getHotPost()
    
    return render_to_response('bbs/bbs_post_detail.html', ret, context_instance=RequestContext(request))


def uploadImg(request):
    if request.method == 'POST':
        ret = {}
        try:
            uid = request.session['login_user_id']
        except Exception:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        
        img = request.FILES.get('file')
        new_name, photo_suffix = genBPName(img.name)
        img_path = '/media/bbs/img/%s/'%(uid)
        print new_name
        print photo_suffix
        #图片处理及保存
        try:
            msg = bbsImgProccess(img, img_path, new_name, photo_suffix)
            if msg == 'makedirwrong':
                ret['msg'] = '201'  #创建相册出错
                return HttpResponse(json.dumps(ret))
        except Exception:
            ret['msg'] = '203'
            return HttpResponse(json.dumps(ret))
        
        new_url = img_path + new_name
        user_obj = models.User.objects.filter(id=uid)
        #图片记录到临时表

        models.Post_Temp_Images.objects.create(user=user_obj[0], img=new_url)
        return HttpResponse(new_url)
    else:
        raise Http404

def submitReply(request):
    if request.method == 'POST':
        ret = {}
        try:
            uid = request.session['login_user_id']
        except Exception:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        html_content = request.POST.get('html_content', None)
        pid = request.POST.get('pid', None)
        
        if not pid.isdigit():
            ret['msg'] = '302'  #前端数据格式错误
            return HttpResponse(json.dumps(ret))
        
        content_imgs = re.findall(r'<img.*?src="(/media.*?)".*?>', html_content, re.S)
        uploaded_imgs = models.Post_Temp_Images.objects.filter(user__id=uid)
        #print 'uploaded_imgs: '+ str(uploaded_imgs.count())
        if uploaded_imgs.count() > 0:  #临时表中存在图片
            if len(content_imgs) == 0:  #用户清空了内容中的图片
                for i in uploaded_imgs:  #删除每个图片
                    deleteImg(str(i.img))

            else:
                for i in uploaded_imgs:  #循环临时表中该用户的每个图片
                    img_exist = False
                    temp_img = str(i.img)
                    for j in content_imgs:  #与content中每个img_url比较
                        #print 'temp_Img:' + temp_img
                        #print 'j:' + j
                        if temp_img == j:
                            img_exist = True
                            break
                    if not img_exist:
                        deleteImg(temp_img)

            uploaded_imgs.delete()  #清空该用户在临时表中条目

        #存入PostReply表
        try:
            post_obj = models.Post.objects.get(id=pid)
            user_obj = models.User.objects.get(id=uid)
        except Exception:
            ret['msg'] = '103'  #记录不存在
            return HttpResponse(json.dumps(ret))
        try:
            new_post_obj = models.PostReply.objects.create(content=html_content, user=user_obj, post=post_obj)
        except Exception:
            ret['msg'] = '101'  #写入错误

        #更新帖子最后回复时间/回帖人
        models.Post.objects.filter(id=pid).update(last_replied_date=new_post_obj.create_date,
                                                  last_replied_user=user_obj)

        #增加经验值
        expAdd('post_reply', uid)
        ret['msg'] = 'success'
        
        #若楼主不是自己，通知楼主
        target_uid = post_obj.user.id
        if not target_uid == uid:
            check_obj = models.User_Notification_Check.objects.filter(target_user__id=target_uid)
            if check_obj.count() == 1:
                try:
                    #存在即更新
                    check_obj.update(bbs_r=check_obj[0].bbs_r + 1)
                except Exception:
                    ret['msg'] = '101'
                    return HttpResponse(json.dumps(ret))
            elif check_obj.count() == 0:  #以防万一
                try:
                    models.User_Notification_Check.objects.create(target_user=post_obj.user, bbs_r=1)
                except Exception:
                    ret['msg'] = '103'  #用户不存在
                    return HttpResponse(json.dumps(ret))
            else:  #重复数据
                ret['msg'] = '102'
                return HttpResponse(json.dumps(ret))
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404


def submitPost(request):
    if request.method == 'POST':
        ret = {}
        try:
            uid = request.session['login_user_id']
        except Exception:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        board = request.POST.get('board', None)
        title = request.POST.get('title', None).strip()
        html_content = request.POST.get('html_content', None)
        html_content = htmlContentFilter(html_content, 'rich')
        #处理内容中的图片
        content_imgs = re.findall(r'<img.*?src="(/media.*?)".*?>', html_content, re.S)
        uploaded_imgs = models.Post_Temp_Images.objects.filter(user__id=uid)
        #print 'uploaded_imgs_counts: '+ str(uploaded_imgs.count())
        #print 'uploaded_imgs: '+ str(uploaded_imgs)
        first_exist_img = True  #只生成第一张图片缩略图，用于通知等quote
        if uploaded_imgs.count() > 0:  #临时表中存在图片
            if len(content_imgs) == 0:  #用户清空了内容中的图片
                for i in uploaded_imgs:  #删除每个图片
                    deleteImg(str(i.img))

            else:
                for i in uploaded_imgs:  #循环临时表中该用户的每个图片
                    temp_img = str(i.img)
                    
                    img_exist = False  #临时表中每个图片初始化为不存在
                    for j in content_imgs:  #与content中每个img_url比较
                        if temp_img == j:
                            img_exist = True

                    if img_exist:
                        is_gif = re.search('.*(\.gif$)', temp_img.lower())

                        if first_exist_img and not is_gif:
                            #存在且为第一张图片，生成缩略图和路径

                            result_path = genPostImgThumb(temp_img, uid)
                            first_exist_img = False

                    else:
                        deleteImg(temp_img)

            uploaded_imgs.delete()  #清空该用户在临时表中条目

        #存入Post表
        try:
            user_obj = models.User.objects.get(id=uid)
        except Exception:
            ret['msg'] = '103'  #记录不存在
            return HttpResponse(json.dumps(ret))
        try:
            if 'result_path' in dir():  #如果生成了缩略图
                models.Post.objects.create(board=board, title=title, content=html_content,
                    user=user_obj, img_thumb=result_path, last_replied_user=user_obj)
            else:
                models.Post.objects.create(board=board, title=title, content=html_content,
                    user=user_obj, last_replied_user=user_obj)
        except Exception:
            ret['msg'] = '101'  #写入错误

        #增加经验值
        expAdd('post', uid)
        ret['msg'] = 'success'

        return HttpResponse(json.dumps(ret))
    else:
        raise Http404

def submitLayerReply(request):
    if request.method == 'POST':
        ret = {}
        prid = request.POST.get('prid', '')
        html_content = request.POST.get('content', None)
        html_content = htmlContentFilter(html_content, 'static')
        target_uid = request.POST.get('target_uid', '')

        if  target_uid.isdigit():
            target_uid = int(target_uid)
            target_user_obj = models.User.objects.filter(id=target_uid)
            print target_user_obj
            if not target_user_obj.count():
                ret['msg'] = '103'
                return HttpResponse(json.dumps(ret))
        else:
            ret['msg'] = '302'
            return HttpResponse(json.dumps(ret))

            
        try:
            uid = request.session['login_user_id']
        except Exception:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))

        user_obj = models.User.objects.filter(id=uid)

        if prid.isdigit():
            post_reply_obj = models.PostReply.objects.filter(id=prid)
            if not post_reply_obj.count():
                ret['msg'] = '103'
                return HttpResponse(json.dumps(ret))
        else:
            ret['msg'] = '302'
            return HttpResponse(json.dumps(ret))

        try:
            new_post_lr = models.PostLayerReply.objects.create(user=user_obj[0], 
                    content=html_content, post_reply=post_reply_obj[0], target_user=target_user_obj[0])
        except Exception:
            ret['msg'] = '101'
            
        #增加经验值
        expAdd('post_layer_reply', uid)
        ret['msg'] = 'success'
        
        #更新帖子最后回复时间
        post_obj = models.Post.objects.filter(id=post_reply_obj[0].post.id)
        post_obj.update(last_replied_date=new_post_lr.create_date,
                                                                        last_replied_user=user_obj[0])
        #若target_user不是自己
        if not target_uid == uid:
            models.User_Notification_Check.objects.create(target_user=target_user_obj[0], bbs_r=1)
        #若层主不是自己，通知层主
        if not post_reply_obj[0].user.id == uid:
            models.User_Notification_Check.objects.create(target_user=post_reply_obj[0].user, bbs_r=1)
        #若楼主不是自己，通知楼主
        if not post_obj[0].user.id == uid:
            models.User_Notification_Check.objects.create(target_user=post_obj[0].user, bbs_r=1)
        
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404

def deleteReply(request):
    if request.method == 'POST':
        ret = {}
        rid = request.POST.get('rid', None)
        uid = request.session.get('login_user_id', None)
        if not uid:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        
        if rid and rid.isdigit():
            reply_obj = models.PostReply.objects.filter(id=rid)
            if not reply_obj.count():
                ret['msg'] = '103'  #不存在
                return HttpResponse(json.dumps(ret))
            
            try:
                user_obj = models.User.objects.get(id=uid)
            except Exception:
                ret['msg'] = '103'
                return HttpResponse(json.dumps(ret))
            
            if reply_obj[0].user.id == uid or user_obj.privilege==6 or user_obj.privilege==8:
                #1 删除该层中的图片（如果有）
                reply_content = reply_obj[0].content
                content_imgs = re.findall(r'<img.*?src="(/media.*?)".*?>', reply_content, re.S)
                if content_imgs:
                    for img in content_imgs:
                        try:
                            os.remove(os.path.join(BASE_DIR + img))
                        except Exception:
                            pass
                try:
                    #2 删除楼层
                    reply_obj.delete()
                    ret['msg'] = 'success'
                except Exception:
                    ret['msg'] = '101'  #操作失败
            else:
                ret['msg'] = '921'  #无权限
        else:
            ret['msg'] = '302'
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404

def deleteLR(request):
    if request.method == 'POST':
        ret = {}
        lrid = request.POST.get('lrid', '')

        uid = request.session.get('login_user_id', None)
        if not uid:
            ret['msg'] = '401'
            return HttpResponse(json.dumps(ret))
        
        if lrid and lrid.isdigit():
            lr_obj = models.PostLayerReply.objects.filter(id=lrid)
            if not lr_obj.count():
                ret['msg'] = '103'  #不存在
                return HttpResponse(json.dumps(ret))
            
            try:
                user_obj = models.User.objects.get(id=uid)
            except Exception:
                ret['msg'] = '103'
                return HttpResponse(json.dumps(ret))
                
            if lr_obj[0].user.id == uid or user_obj.privilege==6 or user_obj.privilege==8:
                try:
                    lr_obj.delete()
                    ret['msg'] = 'success'
                except Exception:
                    ret['msg'] = '101'  #操作失败

            else:
                ret['msg'] = '921'  #无权限
                
        else:
            ret['msg'] = '302'
        return HttpResponse(json.dumps(ret))
    else:
        raise Http404
    

    
def deletePost(request):
    if request.method == 'POST':
        ret = {}
        pid = request.POST.get('pid', '')
        if pid.isdigit():
            uid = request.session.get('login_user_id', None)
            
            if not uid:
                ret['msg'] = '401'
                return HttpResponse(json.dumps(ret))
            
            user_obj = models.User.objects.filter(id=uid)
            
            if user_obj.count():
                try:
                    post_obj = models.Post.objects.get(id=pid)
                except Exception:
                    ret['msg'] = '103'
                    return HttpResponse(json.dumps(ret))
                user_pr = user_obj[0].privilege
                if  post_obj.user.id==uid or user_pr==6 or user_pr==8:
                    #1 删除每个回复里的图片
                    post_reply_obj = models.PostReply.objects.filter(post__id=pid)
                    for r in post_reply_obj:
                        reply_content_imgs = re.findall(r'<img.*?src="(/media.*?)".*?>', r.content, re.S)
                        for img in reply_content_imgs:
                            deleteImg(img)
                    #2 删除帖子中的图片
                    post_content_imgs = re.findall(r'<img.*?src="(/media.*?)".*?>', post_obj.content, re.S)
                    for img in post_content_imgs:
                        deleteImg(img)
                    #3 删除缩略图
                    deleteImg(str(post_obj.img_thumb))
                    
                    #4 删除帖子
                    try:
                        post_obj.delete()
                        ret['msg'] = 'success'
                    except Exception:
                        ret['msg'] = '101'
                else:
                    ret['msg'] = '921'  #无权限
                return HttpResponse(json.dumps(ret))
    else:
        raise Http404


def getLayerReplyItems(request):
    if request.method == 'POST':
        ret = {}
        page = request.POST.get('page')
        items_per_page = request.POST.get('items_per_page')
        prid = request.POST.get('prid')
        args_l = [page,items_per_page,prid]
        try:

            if all(args_l):
                for a in args_l:
                    if not a.isdigit():
                        ret['msg'] = '302'
                        return HttpResponse(json.dumps(ret))
                page = int(page)
                items_per_page = int(items_per_page)
            else:
                ret['msg'] = '302'
                return HttpResponse(json.dumps(ret))
    
            items_obj = models.PostLayerReply.objects.filter(post_reply__id=prid).values('id',
                                'content','user_id','target_user_id','create_date')[(page-1)*items_per_page:page*items_per_page]
            
            for item in items_obj:
                origin_user_id = item['user_id']
                try:
                    target_user_obj = models.User.objects.get(id=item['target_user_id'])
                    user_obj = models.User.objects.get(id=origin_user_id)
                except Exception:
    
                    pass
                item['target_uname'] = target_user_obj.username
                item['create_date'] = my_tags.my_datetrans(item['create_date'])
                item['ulevel'] = my_tags.my_getUserLevel(user_obj.exp)
                item['posted_counts'] = my_tags.my_getPostedCounts(origin_user_id)
                item['fans_counts'] = my_tags.my_getFansCounts(origin_user_id)
                
    
                focused_list = []
                focused_obj = models.UserFocus.objects.filter(origin_user_of_focus__id=origin_user_id)  #回复主人关注的
                for focus_item in focused_obj:
                    focused_list.append(focus_item.target_user.id)
                focused_res = my_tags.my_focused(origin_user_id, focused_list)
                
                uid = request.session.get('login_user_id', None)
                if item['user_id'] == uid:
                    item['focused'] = 2  #是自己
                else:
                    if focused_res:
                        item['focused'] = 1
                    else:
                        item['focused'] = 0
    
                if user_obj.usercard_bg:
                    item['ubg'] = str(user_obj.usercard_bg)
                else:
                    item['ubg'] = ''

                item['usign'] = user_obj.mysign
                item['uname'] = user_obj.username
                item['uthumb_l'] = str(user_obj.thumb_l)
                item['uthumb_s'] = str(user_obj.thumb_s)
    
            res_list = list(items_obj)
            return HttpResponse(json.dumps(res_list))
        except Exception,e:
            print e

    else:
        raise Http404
