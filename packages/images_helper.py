#_*_coding:UTF-8_*_
from __future__ import division
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from MovieSite.settings import BASE_DIR, FONT
import random, re
import os
from StringIO import StringIO
import urllib
#import time
from datetime import datetime
from uuid import uuid4
from django.core.files.storage import default_storage
from math import floor

def rndChar():
    return chr(random.randint(65, 90))
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
def generate_code():
    """
    "生成验证码
    """
    code_width = 40 * 4
    code_height = 40
    code_image = Image.new('RGB', (code_width, code_height), (255, 255, 255))
    #random_char = random.randint(65, 90)
    #random_color = random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)
    #random_color2 = (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
    # 创建Font对象:
    font = ImageFont.truetype(FONT, 26)
    # 创建Draw对象:
    draw = ImageDraw.Draw(code_image)
    # 填充每个像素:
    for x in range(code_width):
        for y in range(code_height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    code_text = ''
    for t in range(4):
        tmp_char = rndChar()
        code_text += tmp_char
        draw.text((40 * t + 10, 10), tmp_char, font=font, fill=rndColor2())
    # 模糊:
    code_image = code_image.filter(ImageFilter.BLUR)
    code_num = str(random.randint(1,99999999))
    code_name = 'code_' + code_num + '.jpg'
    code_save_path = '/media/reg_code/'#'/static/images/userinfo/code/'
    code_image.save(BASE_DIR + code_save_path + code_name, 'jpeg')
    return code_text, code_save_path + code_name

def genSPName(org_photo_name, qquuid):  #speak photo name
    photo_suffix = re.findall('.*(\.\w{3,4}$)', org_photo_name)[0]
    photo_name = qquuid + photo_suffix
    return photo_name

def genBPName(photo_name):  #bbs photo name
    photo_suffix = re.findall('.*(\.[a-zA-Z]{3,4}$)', photo_name)[0]
    photo_new_name = str(uuid4()).replace('-','') + photo_suffix
    return photo_new_name, photo_suffix

def photoProccess(photo,path,name):
    img = Image.open(photo)
    path = BASE_DIR + path
    thumb_path = path+'thumbs/'
    #建立用户图片目录
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception:
            return 'makedirwrong'
    if not os.path.exists(thumb_path):
        try:
            os.makedirs(thumb_path)
        except Exception:
            return 'makedirwrong'
    
    img.save(path+name, 'JPEG')
    
    """
    create thumbnails
    """
    dest_h = 140
    dest_w = 140
    orig_w, orig_h = img.size
    orig_ratio = orig_w / orig_h
    dest_ratio = 1
    if orig_ratio < dest_ratio:  #过高，先缩放，再裁剪。两种情况：1.宽度小于预定高度，2宽度大于等于
        scaled_h = int(orig_h/(orig_w/dest_w))
        print 'scaled_h: '+ str(scaled_h)
        size = dest_w, scaled_h
        print 'size: ' + str(size)
        img = img.resize(size, Image.ANTIALIAS)  #将宽缩放到dest_w

        x = 0
        y = (scaled_h / 2) - (dest_h / 2)
        box = (x, y, x+dest_w, y+dest_h)

        new_img = img.crop(box)
    elif orig_ratio > dest_ratio:  #宽了
        scaled_w = int(orig_w/(orig_h/dest_h))
        size = scaled_w, dest_h
        img = img.resize(size, Image.ANTIALIAS)
        y = 0
        x = (scaled_w / 2) - (dest_w / 2)
        box = (x, y, x+dest_w, y+dest_h)
        new_img = img.crop(box)
    else:
        new_img = img.resize((dest_w, dest_h), Image.ANTIALIAS)

    #size = w/(h/160), 160
    
    #img.thumbnail(size)
    new_img.save(thumb_path+name, 'JPEG')
    
    return 'success'

def userBgProccess(photo, photo_suffix, uid):

    img = Image.open(photo)
    rel_profile_path = '/media/userhome/profile/'+ str(uid) + '/'
    rel_info_path = '/media/userhome/info/'+ str(uid) + '/'
    rel_usercard_path = '/media/userhome/usercard/'+ str(uid) + '/'
    profile_path = os.path.join(BASE_DIR + '/media/userhome/profile/'+ str(uid) + '/')
    info_path = os.path.join(BASE_DIR + '/media/userhome/info/'+ str(uid) + '/')
    usercard_path = os.path.join(BASE_DIR + '/media/userhome/usercard/'+ str(uid) + '/')
    
    salt = datetime.now().strftime('%y%m%d%H%M%S%f')
    profile_name = 'profile_bg_' + salt + photo_suffix
    info_name = 'info_bg_' + salt + photo_suffix
    usercard_name = 'usercard_bg_' + salt + photo_suffix

    #img.save(path+name, 'JPEG')
    orig_w, orig_h = img.size
    orig_ratio = orig_w / orig_h
    size_dict = {'profile_bg':((profile_path, profile_name), (1920,400)),
                 'info_bg':((info_path, info_name), (261,150)), 
                 'usercard_bg':((usercard_path, usercard_name), (350,90))
                 }
    #profile_bg
    for item in size_dict.items():
        path = item[1][0][0]
        name = item[1][0][1]
        size = item[1][1]
        #print 'path: '+ path
        #print 'name: ' +name
        dest_w = size[0]
        dest_h = size[1]
        dest_ratio = dest_w / dest_h
        #print 'dest_w: ' + str(dest_w)
        #print 'dest_h: ' + str(dest_h)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception:
                return 'makedirwrong'
        if orig_ratio < dest_ratio:  #宽了
            scaled_h = int(orig_h/(orig_w/dest_w))
            size = dest_w, scaled_h
            img_temp = img
            img_temp = img_temp.resize(size, Image.ANTIALIAS)  #将宽缩放到dest_w
            x = 0
            y = (scaled_h / 2) - (dest_h / 2)
            box = (x, y, x+dest_w, y+dest_h)
            box = tuple([int(floor(x)) for x in box])
            new_img = img_temp.crop(box)
        elif orig_ratio > dest_ratio:  #宽了
            scaled_w = int(orig_w/(orig_h/dest_h))
            size = scaled_w, dest_h
            img_temp = img
            img_temp = img_temp.resize(size, Image.ANTIALIAS)
            y = 0
            x = (scaled_w / 2) - (dest_w / 2)
            box = (x, y, x+dest_w, y+dest_h)
            box = tuple([int(floor(x)) for x in box])
            new_img = img_temp.crop(box)
        else:
            img_temp = img
            new_img = img_temp.resize((dest_w, dest_h), Image.ANTIALIAS)
            
        new_img.save(path+name, 'JPEG')

    return rel_profile_path+profile_name, rel_info_path+info_name, rel_usercard_path+usercard_name


def bbsImgProccess(photo, path, name, photo_suffix):
    
    path = BASE_DIR + path
    #建立用户图片目录
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception:
            return 'makedirwrong'
    if photo_suffix.lower() == '.gif':
        try:
            with default_storage.open(path+name, 'wb+') as destination:
                for chunk in photo.chunks():
                    destination.write(chunk)
            return 'success'
        except Exception,e:
            print e
            return 'fail'
    img = Image.open(photo)
    #resize image
    dest_w = 706
    orig_w, orig_h = img.size
    if orig_w > 706:
        dest_h = int((dest_w * orig_h) / orig_w)
        region = img.resize((dest_w, dest_h), Image.ANTIALIAS)
        region.save(path+name, 'JPEG')
    else:
        try:
            img.save(path+name, 'JPEG')
        except Exception:
            return 'fail'
    
    return 'success'

    
def avatarProcess(url, user_id, sizes=(100,60,40)):
    avatar_path = BASE_DIR + '/media/avatar/' + user_id + '/'
    #读取图像
    try:
        img_file = StringIO(urllib.urlopen(url).read())
        im = Image.open(img_file)
    except Exception:
        return 'IOerror'
    
    #建立目录
    if not os.path.exists(avatar_path):
        try:
            os.makedirs(avatar_path)
        except Exception:
            return 'makedirwrong'
    #转换PNG->RGB
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255,255,255), None, bgmask)
        else:
            im = im.convert('RGB')
            
    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            delta = (width - height)/2
            box = (delta, 0, delta+height, height)
        else:
            delta = (height - width)/2
            box = (0, delta, width, delta+width)            
        region = im.crop(box)

    salt = datetime.now().strftime('%y%m%d%H%M%S%f')
    
    for size in sizes: #三种大小的头像缩略图
        filename = 'avatar_' + "%sx%s_%s" % (str(size), str(size), salt) + '.jpg'
        thumb = region.resize((size,size), Image.ANTIALIAS)  #抗锯齿
        thumb.save(avatar_path + filename, quality=100) # 默认JPEG保存质量是 75, 可选值(0~100)

    return filename

def genPostImgThumb(img, uid):
    size = (60, 60)
    target_path = os.path.join(BASE_DIR + '/media/bbs/post_thumbs/' + str(uid) + '/')
    print target_path
    if not os.path.exists(target_path):
        try:
            os.makedirs(target_path)
        except Exception:
            return 'makedirwrong'
    new_name, photo_suffix = genBPName(img)

    im = Image.open(os.path.join(BASE_DIR+img))
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255-x)
            im = im.convert('RGB')
            # paste(color, box, mask)
            im.paste((255,255,255), None, bgmask)
        else:
            im = im.convert('RGB')

    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            delta = (width - height)/2
            box = (delta, 0, delta+height, height)
        else:
            delta = (height - width)/2
            box = (0, delta, width, delta+width)
        box = tuple([int(floor(x)) for x in box])
        region = im.crop(box)

    full_path = target_path + new_name
    print full_path
    thumb = region.resize(size, Image.ANTIALIAS)  #抗锯齿
    thumb.save(full_path, quality=100)
    
    result_path = os.path.join('/media/bbs/post_thumbs/' + str(uid) + '/' + new_name)
    return result_path