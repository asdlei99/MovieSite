#coding:UTF-8
from __future__ import unicode_literals
from django.db import models

class Index_Slider(models.Model):
    cate_choice = (('movie','电影'),('tv','电视剧'),('anime','动漫'),('show','综艺'))
    img_url = models.CharField(max_length=64, verbose_name='横版海报图片地址', default='/static/images/sliders/index/')
    media_name = models.CharField(max_length=32, verbose_name='影片名', blank=True)
    media_id = models.IntegerField(verbose_name='影片ID')
    cate = models.CharField(choices=cate_choice, max_length=16, default='movie', verbose_name='分类')
    desc = models.CharField(max_length=64, verbose_name='短评描述')
    def __unicode__(self):
        return self.media_name 

class Movie(models.Model):
    ch_name = models.CharField(max_length=50, verbose_name='中文电影名')
    foreign_name = models.CharField(max_length=100, verbose_name='外文电影名', blank=True)
    year = models.CharField(max_length=10, verbose_name='年代')
    director = models.CharField(max_length=256, verbose_name='导演', blank=True)
    screenwriter = models.CharField(max_length=256, verbose_name='编剧', blank=True)
    actor = models.CharField(max_length=512, verbose_name='主演', blank=True)
    types = models.CharField(max_length=128, verbose_name='类型')
    region = models.CharField(max_length=128, verbose_name='国家地区')
    release_date = models.CharField(max_length=20, verbose_name='上映时间', blank=True)
    release_date_show = models.CharField(max_length=256, verbose_name='上映时间显示', blank=True)
    running_time = models.CharField(max_length=256, verbose_name='片长', blank=True)
    other_name = models.CharField(max_length=256, verbose_name='又名', blank=True)
    score = models.FloatField(verbose_name='评分')
    intro = models.TextField(max_length=1024, verbose_name='简介')
    poster = models.CharField(max_length=128, verbose_name='海报', default='/static/images/movie/p/1603/', blank=True)
    ss1 = models.CharField(max_length=512, verbose_name='影片截图-1', default='/static/images/movie/s/1603/', blank=True)
    ss2 = models.CharField(max_length=512, verbose_name='影片截图-2', default='/static/images/movie/s/1603/', blank=True)
    ss3 = models.CharField(max_length=512, verbose_name='影片截图-3', default='/static/images/movie/s/1603/', blank=True)
    ss4 = models.CharField(max_length=512, verbose_name='影片截图-4', default='/static/images/movie/s/1603/', blank=True)
    down_name = models.CharField(max_length=256, verbose_name='下载显示文件名', default='N/A')
    down_url = models.TextField(max_length=2048, verbose_name='下载链接', default='无下载')
    down_name2 = models.CharField(max_length=256, verbose_name='下载显示文件名2', default='N/A', blank=True)
    down_url2 = models.TextField(max_length=2048, verbose_name='下载链接2', default='无下载', blank=True)
    video_type = models.CharField(max_length=10, verbose_name='视频类型', default='正式片', blank=True)
    video = models.TextField(max_length=2048, verbose_name='PC视频', default='无视频', blank=True)
    video2 = models.TextField(max_length=2048, verbose_name='移动视频', default='无视频', blank=True)

    link_addr = models.CharField(max_length=128, verbose_name='lol地址', default='N/A')
    douban_sn = models.CharField(max_length=16, verbose_name='豆瓣编号', blank=True)
    imdb_sn = models.CharField(max_length=16, verbose_name='IMDB地址', blank=True)
    compare_way = models.CharField(max_length=16, verbose_name='添加匹配方式', blank=True)
    visit_count = models.IntegerField(verbose_name='页面访问量', default=0)
    week_visit_count = models.IntegerField(verbose_name='周访问量', default=0)
    month_visit_count = models.IntegerField(verbose_name = '月访问量', default=0)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    cate = models.CharField(default='movie', max_length=16)
    def __unicode__(self):
        return '%s %s' %(self.ch_name, self.types)
    
class Movie_Recommend(models.Model):
    cate_choice = ((1,'电影'),(2,'电视剧'),(3,'动漫'),(4,'综艺'))
    media_id = models.IntegerField()
    cate = models.IntegerField(choices=cate_choice, default=1, verbose_name='分类')
    reason = models.CharField(max_length=128, verbose_name='推荐理由')
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        if self.cate == 1:
            self.c = '电影'
        elif self.cate == 2:
            self.c = '电视剧'
        elif self.cate == 3:
            self.c = '动漫'
        elif self.cate == 4:
            self.c = '综艺'
        return '%s %s' %(self.c, self.media_id)
    
#影评
class MovieReply(models.Model):
    content = models.TextField(max_length=512)
    movie = models.ForeignKey('Movie', related_name='movie_r')
    rating = models.IntegerField(default=0)
    user = models.ForeignKey('User', related_name='movie_r_user')
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content
    
class MovieReplyReply(models.Model):
    user = models.ForeignKey('User', related_name='movie_rr_user')
    movie_reply = models.ForeignKey('MovieReply', related_name='movie_rr')
    content = models.TextField(max_length=256)
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content
    
class MovieReplyLike(models.Model):
    user = models.ForeignKey('User', related_name='movie_r_like_user')
    movie_reply_like = models.ForeignKey('MovieReply', related_name='movie_r_like')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.movie_reply_like)

class Tv(models.Model):
    ch_name = models.CharField(max_length=50, verbose_name='中文电视剧名')
    foreign_name = models.CharField(max_length=100, verbose_name='外文电视剧名', blank=True)
    year = models.CharField(max_length=10, verbose_name='年代')
    director = models.CharField(max_length=256, verbose_name='导演', blank=True)
    screenwriter = models.CharField(max_length=256, verbose_name='编剧', blank=True)
    actor = models.CharField(max_length=512, verbose_name='主演', blank=True)
    types = models.CharField(max_length=128, verbose_name='类型')
    region = models.CharField(max_length=50, verbose_name='国家地区')
    release_date = models.CharField(max_length=20, verbose_name='首播时间', blank=True)
    release_date_show = models.CharField(max_length=128, verbose_name='首播时间显示', blank=True)
    eps = models.IntegerField(default=0, verbose_name='集数')
    running_time = models.CharField(max_length=128, verbose_name='单集片长', blank=True)
    other_name = models.CharField(max_length=256, verbose_name='又名', blank=True)
    score = models.FloatField(verbose_name='评分')
    intro = models.TextField(max_length=1024, verbose_name='简介')
    poster = models.CharField(max_length=128, verbose_name='海报', default='/static/images/tv/p/1604/', blank=True)
    ss1 = models.CharField(max_length=512, verbose_name='影片截图-1', default='/static/images/tv/s/1604/', blank=True)
    ss2 = models.CharField(max_length=512, verbose_name='影片截图-2', default='/static/images/tv/s/1604/', blank=True)
    ss3 = models.CharField(max_length=512, verbose_name='影片截图-3', default='/static/images/tv/s/1604/', blank=True)
    ss4 = models.CharField(max_length=512, verbose_name='影片截图-4', default='/static/images/tv/s/1604/', blank=True)
    updated_eps = models.IntegerField(default=0, verbose_name='更新至')
    down_names = models.TextField(max_length=12800, verbose_name='文件名')
    down_urls = models.TextField(max_length=65534, verbose_name='下载链接')
    link_addr = models.CharField(max_length=128, verbose_name='lol地址', default='http://')
    douban_sn = models.CharField(max_length=16, verbose_name='豆瓣编号', blank=True)
    imdb_sn = models.CharField(max_length=16, verbose_name='IMDB地址', blank=True)
    compare_way = models.CharField(max_length=16, verbose_name='添加匹配方式', blank=True)
    seq = models.IntegerField(verbose_name='第几段地址', default=1)

    visit_count = models.IntegerField(verbose_name='页面访问量', default=0)
    week_visit_count = models.IntegerField(verbose_name='每周页面访问量', default=0)
    month_visit_count = models.IntegerField(verbose_name='每月页面访问量', default=0)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    cate = models.CharField(default='tv', max_length=16)
    def __unicode__(self):
        return '%s %s' %(self.ch_name, self.types)

#影评
class TvReply(models.Model):
    content = models.TextField(max_length=512)
    tv = models.ForeignKey('Tv', related_name='tv_r')
    rating = models.IntegerField(default=0)
    user = models.ForeignKey('User', related_name='tv_r_user')
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content
    
class TvReplyReply(models.Model):
    user = models.ForeignKey('User')
    tv_reply = models.ForeignKey('TvReply', related_name='tv_rr')
    content = models.TextField(max_length=256)
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content

class TvReplyLike(models.Model):
    user = models.ForeignKey('User', related_name='tv_r_like_user')
    tv_reply_like = models.ForeignKey('TvReply', related_name='tv_r_like')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content

class News(models.Model):
    title = models.CharField(max_length=128, verbose_name='主标题')
    subtitle = models.CharField(max_length=128, verbose_name='副标题', blank=True)
    recommended = models.BooleanField(default=False, verbose_name='是否推荐')  #推荐内容
    news_content = models.TextField(max_length=40960, verbose_name='内容')
    source = models.CharField(max_length=128, verbose_name='新闻来源')
    keywords =  models.CharField(max_length=128, verbose_name='关键词', blank=True)
    news_image = models.CharField(max_length=256, verbose_name='配图', default='/static/images/news/1603/')
    ga_content = models.TextField(max_length=5120, verbose_name='图集内容', blank=True)
    title_bg = models.CharField(max_length=128, verbose_name='标题背景图', blank=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    visit_count = models.IntegerField(default=0, verbose_name='页面访问量')
    day_visit_count = models.IntegerField(default=0, verbose_name='日访问量')
    week_visit_count = models.IntegerField(default=0, verbose_name='周访问量')
    def __unicode__(self):
        return self.title
    
class NewsReply(models.Model):
    user = models.ForeignKey('User', related_name='news_r_user')
    content = models.CharField(max_length=512)
    news = models.ForeignKey('News', related_name='news_r')
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content
    
class NewsReplyReply(models.Model):
    user = models.ForeignKey('User', related_name='news_rr_user')
    news_reply = models.ForeignKey('NewsReply', related_name='news_rr')
    content = models.TextField(max_length=256)
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content
    
class NewsReplyLike(models.Model):
    user = models.ForeignKey('User', related_name='news_r_like_user')
    news_reply_like = models.ForeignKey('NewsReply', related_name='news_r_like')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content
    
class News_Index_Slider(models.Model):
    img_url = models.CharField(max_length=64, verbose_name='新闻图片地址', default='/static/images/sliders/news_index/')
    news_id = models.IntegerField(default=0, verbose_name='新闻ID')
    desc = models.CharField(max_length=64, verbose_name='短评描述')
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.desc + 'slider'

class Anime(models.Model):
    ch_name = models.CharField(max_length=50, verbose_name='中文动漫名')
    foreign_name = models.CharField(max_length=100, verbose_name='外文动漫名', blank=True)
    year = models.CharField(max_length=10, verbose_name='年代')
    director = models.CharField(max_length=256, verbose_name='导演', blank=True)
    screenwriter = models.CharField(max_length=256, verbose_name='编剧', blank=True)
    actor = models.CharField(max_length=512, verbose_name='主演', blank=True)
    types = models.CharField(max_length=128, verbose_name='类型')
    region = models.CharField(max_length=50, verbose_name='国家地区')
    release_date = models.CharField(max_length=20, verbose_name='首播时间', blank=True)
    release_date_show = models.CharField(max_length=128, verbose_name='首播时间显示', blank=True)
    eps = models.IntegerField(default=0, verbose_name='集数')
    running_time = models.CharField(max_length=128, verbose_name='单集片长', blank=True)
    other_name = models.CharField(max_length=256, verbose_name='又名', blank=True)
    score = models.FloatField(verbose_name='评分')
    intro = models.TextField(max_length=1024, verbose_name='简介')
    poster = models.CharField(max_length=128, verbose_name='海报', default='/static/images/anime/p/1604/', blank=True)
    ss1 = models.CharField(max_length=512, verbose_name='影片截图-1', default='/static/images/anime/s/1604/', blank=True)
    ss2 = models.CharField(max_length=512, verbose_name='影片截图-2', default='/static/images/anime/s/1604/', blank=True)
    ss3 = models.CharField(max_length=512, verbose_name='影片截图-3', default='/static/images/anime/s/1604/', blank=True)
    ss4 = models.CharField(max_length=512, verbose_name='影片截图-4', default='/static/images/anime/s/1604/', blank=True)
    updated_eps = models.IntegerField(default=0, verbose_name='更新至')
    down_names = models.TextField(max_length=12800, verbose_name='文件名')
    down_urls = models.TextField(max_length=65534, verbose_name='下载链接')
    link_addr = models.CharField(max_length=128, verbose_name='lol地址', default='N/A')
    douban_sn = models.CharField(max_length=16, verbose_name='豆瓣编号', blank=True)
    imdb_sn = models.CharField(max_length=16, verbose_name='IMDB地址', blank=True)
    compare_way = models.CharField(max_length=16, verbose_name='添加匹配方式', blank=True)
    seq = models.IntegerField(verbose_name='第几段地址', default=1)

    visit_count = models.IntegerField(verbose_name='页面访问量', default=0)
    week_visit_count = models.IntegerField(verbose_name='每周页面访问量', default=0)
    month_visit_count = models.IntegerField(verbose_name='每月页面访问量', default=0)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    cate = models.CharField(default='anime', max_length=16)
    def __unicode__(self):
        return '%s %s' %(self.ch_name, self.types)

class AnimeReply(models.Model):
    content = models.TextField(max_length=512)
    anime = models.ForeignKey('Anime', related_name='anime_r')
    rating = models.IntegerField(default=0)
    user = models.ForeignKey('User', related_name='anime_r_user')
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content
    
class AnimeReplyReply(models.Model):
    user = models.ForeignKey('User')
    anime_reply = models.ForeignKey('AnimeReply', related_name='anime_rr')
    content = models.TextField(max_length=256)
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content

class AnimeReplyLike(models.Model):
    user = models.ForeignKey('User', related_name='anime_r_like_user')
    anime_reply_like = models.ForeignKey('AnimeReply', related_name='anime_r_like')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content

class Show(models.Model):
    ch_name = models.CharField(max_length=50, verbose_name='中文综艺名')
    foreign_name = models.CharField(max_length=100, verbose_name='外文综艺名', blank=True)
    year = models.CharField(max_length=10, verbose_name='年代')
    director = models.CharField(max_length=256, verbose_name='导演', blank=True)
    screenwriter = models.CharField(max_length=256, verbose_name='编剧', blank=True)
    actor = models.CharField(max_length=512, verbose_name='主演', blank=True)
    types = models.CharField(max_length=128, verbose_name='类型')
    region = models.CharField(max_length=50, verbose_name='国家地区')
    release_date = models.CharField(max_length=20, verbose_name='首播时间', blank=True)
    release_date_show = models.CharField(max_length=128, verbose_name='首播时间显示', blank=True)
    eps = models.IntegerField(default=0, verbose_name='集数')
    running_time = models.CharField(max_length=128, verbose_name='单集片长', blank=True)
    other_name = models.CharField(max_length=256, verbose_name='又名', blank=True)
    score = models.FloatField(verbose_name='评分')
    intro = models.TextField(max_length=1024, verbose_name='简介')
    poster = models.CharField(max_length=128, verbose_name='海报', default='/static/images/show/p/1604/', blank=True)
    ss1 = models.CharField(max_length=512, verbose_name='影片截图-1', default='/static/images/show/s/1604/', blank=True)
    ss2 = models.CharField(max_length=512, verbose_name='影片截图-2', default='/static/images/show/s/1604/', blank=True)
    ss3 = models.CharField(max_length=512, verbose_name='影片截图-3', default='/static/images/show/s/1604/', blank=True)
    ss4 = models.CharField(max_length=512, verbose_name='影片截图-4', default='/static/images/show/s/1604/', blank=True)
    updated_eps = models.IntegerField(default=0, verbose_name='更新至')
    down_names = models.TextField(max_length=12800, verbose_name='文件名')
    down_urls = models.TextField(max_length=65534, verbose_name='下载链接')
    link_addr = models.CharField(max_length=128, verbose_name='lol地址', default='N/A')
    douban_sn = models.CharField(max_length=16, verbose_name='豆瓣编号', blank=True)
    imdb_sn = models.CharField(max_length=16, verbose_name='IMDB地址', blank=True)
    compare_way = models.CharField(max_length=16, verbose_name='添加匹配方式', blank=True)
    seq = models.IntegerField(verbose_name='第几段地址', default=1)

    visit_count = models.IntegerField(verbose_name='页面访问量', default=0)
    week_visit_count = models.IntegerField(verbose_name='每周页面访问量', default=0)
    month_visit_count = models.IntegerField(verbose_name='每月页面访问量', default=0)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    cate = models.CharField(default='show', max_length=16)
    def __unicode__(self):
        return '%s %s' %(self.ch_name, self.types)

class ShowReply(models.Model):
    content = models.TextField(max_length=512)
    show = models.ForeignKey('Show', related_name='show_r')
    rating = models.IntegerField(default=0)
    user = models.ForeignKey('User')
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content
    
class ShowReplyReply(models.Model):
    user = models.ForeignKey('User')
    show_reply = models.ForeignKey('ShowReply', related_name='show_rr')
    content = models.TextField(max_length=256)
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content

class ShowReplyLike(models.Model):
    user = models.ForeignKey('User', related_name='show_r_like_user')
    show_reply_like = models.ForeignKey('ShowReply', related_name='show_r_like')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content

#######  User  ######

class User(models.Model):
    gender_choice = ((0,'男'), (1,'女'))
    email = models.EmailField(max_length=64)
    username = models.CharField(max_length=30, blank=True) #昵称
    password = models.CharField(max_length=64)
    mysign = models.CharField(max_length=64, default='这位同学还没有改过签名~')
    gender = models.IntegerField(choices=gender_choice, default=0)
    location = models.CharField(max_length=64, default='未填写')
    birthday = models.DateField(auto_now_add=True)
    thumb_s = models.ImageField(default='/static/images/default/avatar/avatar_default_40x40.jpg')
    thumb_m = models.ImageField(default='/static/images/default/avatar/avatar_default_60x60.jpg')
    thumb_l = models.ImageField(default='/static/images/default/avatar/avatar_default_100x100.jpg')
    profile_bg = models.ImageField(blank=True)  #自定义背景
    info_bg = models.ImageField(blank=True)
    usercard_bg = models.ImageField(blank=True)
    h_focusme = models.BooleanField(default=True)  #关注我
    h_recvpush = models.BooleanField(default=True) #消息通知
    auth_choice = ((0,'仅自己'),(1,'所有人'),(2,'我关注的人'))
    h_mycollect = models.IntegerField(choices=auth_choice, default=1)
    h_myspeak = models.IntegerField(choices=auth_choice, default=1)
    h_mycomment = models.IntegerField(choices=auth_choice, default=1)
    h_mypost = models.IntegerField(choices=auth_choice, default=1)
    #last_logout_date = models.DateTimeField(auto_now_add=True, verbose_name="上次退出登录时间")
    privilege = models.IntegerField(default=1)  #权限0表示被封号，1表示未激活，4为普通用户，6为管理员，8为超级管理员
    exp = models.IntegerField(default=0)  #经验值
    today_exp = models.IntegerField(default=0)
    pwd_token = models.CharField(max_length=30, blank=True)
    last_login_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.username



"""
class UserAvatar(models.Model):
    user = models.ForeignKey('User', related_name='user_avatar')
    thumb_s = models.ImageField(default='/media/avatar/avatar_default_40x40.jpg')
    thumb_m = models.ImageField(default='/media/avatar/avatar_default_60x60.jpg')
    thumb_l = models.ImageField(default='/media/avatar/avatar_default_100x100.jpg')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='头像创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='头像更新时间')
    def __unicode__(self):
        return self.user + '的头像'

""" 
class UserPhoto(models.Model):
    photo = models.ImageField()
    name = models.CharField(max_length=128)
    thumb = models.ImageField()
    desc = models.CharField(max_length=128, default=name, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.photo)

class User_Message(models.Model):
    #msg_title = models.CharField(max_length=32)
    content = models.CharField(max_length=512)
    read = models.BooleanField(default=False)  #在发送时如果是自己所发，直接将read置为1
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)  #回复时更新，用于显示
    sender = models.ForeignKey('User', related_name='msg_sender')
    receiver = models.ForeignKey('User', related_name='msg_receiver')
    def __unicode__(self):
        return self.content

class User_Message_Reply(models.Model):
    content = models.CharField(max_length=512)
    message = models.ForeignKey('User_Message', related_name='user_message')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey('User', related_name='msg_reply_sender')
    receiver = models.ForeignKey('User', related_name='msg_reply_receiver')
    def __unicode__(self):
        return self.content

class UserExp(models.Model):
    user = models.ForeignKey('User', related_name='user_exp_user')
    exp_today = models.SmallIntegerField(default=0)  #每日清空
    exp_total = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.user)

class User_Notification_Check(models.Model):  ##用于客户端通知轮询
    target_user = models.ForeignKey('User', related_name='user_notice_check_target_user')
    movie_r_like = models.IntegerField(default=0) #影评被点赞数，0表示无更新
    movie_rr = models.IntegerField(default=0)  #影评的回复
    bbs_r = models.IntegerField(default=0)  #论坛收到的回复，包括帖子的回复，楼层的回复，以及楼层@回复
    focus = models.IntegerField(default=0)  #被关注数
    msg = models.IntegerField(default=0)  #新收到私信数
    speak_r = models.IntegerField(default=0)  #说说回复数
    
class UserSpeak(models.Model):
    user = models.ForeignKey('User', related_name='user_speak')
    content = models.CharField(max_length=1024)
    speak_photo = models.CharField(max_length=1024, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s %s' %(self.user, self.content)
    
class UserSpeakTemp(models.Model):
    user = models.ForeignKey('User', related_name='user_speak_temp')
    qquuid = models.CharField(max_length=64)
    speak_photo = models.ImageField()
    create_date = models.DateTimeField(auto_now_add=True)

class UserSpeakReply(models.Model):
    speak_of_reply = models.ForeignKey('UserSpeak', related_name='user_speak_of_reply')
    user = models.ForeignKey('User')
    content = models.CharField(max_length=512)
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s %s' %(str(self.user), self.content)
    
class User_Speak_RR(models.Model):
    speak_reply = models.ForeignKey('UserSpeakReply', related_name='user_speak_reply')
    user = models.ForeignKey('User')
    target_user = models.ForeignKey('User', related_name='user_speak_rr_target_user')
    content = models.CharField(max_length=512)
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s %s' %(str(self.user), self.content)
    
class User_Speak_Like(models.Model):
    speak_of_like = models.ForeignKey('UserSpeak', related_name='user_speak_of_like')
    user = models.ForeignKey('User')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

#暂无
class User_Speak_Forward(models.Model):
    speak_of_forward = models.ForeignKey('UserSpeak')
    user = models.ForeignKey('User', related_name='user_speak_forward')
    content = models.CharField(max_length=512)
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    
class UserVisitHistory(models.Model):
    visitor = models.ForeignKey('User', related_name='visitor')
    host = models.ForeignKey('User', related_name='host')
    create_date = models.DateTimeField(auto_now_add=True)  #第一次访问时间
    update_date = models.DateTimeField(auto_now=True)  #最近一次访问时间
    times = models.IntegerField(default=1)  #累计访问次数（每条）
    def __unicode__(self):
        return '%s访问%s' %(self.visitor.username, self.host.username)

class UserFocus(models.Model):  #关注他人
    origin_user_of_focus = models.ForeignKey('User', related_name='user_focus_origin_user')
    target_user = models.ForeignKey('User', related_name='user_focus_target_user')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

class Collect_Movie(models.Model):
    user = models.ForeignKey('User', related_name='collect_movie_user')
    movie = models.ForeignKey('Movie', related_name='collect_movie')
    create_date = models.DateTimeField(auto_now_add=True)

class Collect_Tv(models.Model):
    user = models.ForeignKey('User', related_name='collect_tv_user')
    tv = models.ForeignKey('Tv')
    create_date = models.DateTimeField(auto_now_add=True)
    
class Collect_Anime(models.Model):
    user = models.ForeignKey('User', related_name='collect_anime_user')
    anime = models.ForeignKey('Anime')
    create_date = models.DateTimeField(auto_now_add=True)
    
class Collect_Show(models.Model):
    user = models.ForeignKey('User', related_name='collect_show_user')
    show = models.ForeignKey('Show')
    create_date = models.DateTimeField(auto_now_add=True)


    
#######  BBS ######

class Post(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=2048)
    board = models.CharField(max_length=8) #movie,tv,anime,show...
    img_thumb = models.ImageField(blank=True)
    user = models.ForeignKey('User', related_name='op')
    last_replied_date = models.DateTimeField(auto_now=True) #最后回复时间
    last_replied_user = models.ForeignKey('User', related_name='post_last_replier')
    visit_counts = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.title

class PostReply(models.Model):
    content = models.TextField(max_length=2048)
    user = models.ForeignKey('User', related_name='post_replier')
    post = models.ForeignKey('Post', related_name='post_reply')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content[:50]
    
class PostLayerReply(models.Model):
    content = models.CharField(max_length=512)
    user = models.ForeignKey('User', related_name='post_layer_reply_user')
    target_user = models.ForeignKey('User', related_name='post_layer_reply_target_user')  #回复中@某人
    post_reply = models.ForeignKey('PostReply', related_name='post_layer_reply')
    read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.content[:50]
    
#用于存储用户发帖时上传的临时图片
class Post_Temp_Images(models.Model):
    user = models.ForeignKey('User')
    img = models.ImageField()
