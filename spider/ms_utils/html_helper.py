# coding=utf-8
from __future__ import division

import base64
import os
import re
import time
import urllib
from random import uniform

from common import get_html_content, get_douban_sn, get_webdriver
from ms_constants import DOWNLOAD_IMAGE_PATH, WEB_IMAGE_PATH, MOVIE_NAME_ENG, \
    MOVIE_NAME_CH, NEW_LINE
from ms_exceptions import *
from ms_utils import log
from ms_utils.image_helper import ImageProcessor

LOG = log.Log()
IP = ImageProcessor()


class Douban(object):

    def __init__(self):
        self.pattern_tag = "<.*?>"
        self.h1_name_pat = '<h1>.*?<span.*?"v:itemreviewed">(.*?)</span>'
        self.text_handler = TextHandler()
        self.pattern_year = re.compile('<span.*?class="year">(.*?)</span>', re.S)
        self.pattern_director = re.compile('>导演.*?: (.*?)<br/>', re.S)
        self.pattern_screenwriter = re.compile('>编剧.*?: (.*?)<br/>', re.S)
        self.pattern_actor = re.compile('>主演.*?: (.*?)<br/>', re.S)
        self.pattern_type = re.compile('>类型.*?</span>(.*?)<br/>', re.S)
        self.pattern_region = re.compile('>制片国家.*?</span>(.*?)<br.*?>', re.S)
        self.pattern_shangying = re.compile('>上映日期.*?</span>(.*?)<br.*?>', re.S)
        self.pattern_shoubo = re.compile('>首播.*?</span>(.*?)<br.*?>',
                                         re.S)
        self.pattern_score = re.compile('<strong.*?rating_num.*?>(.*?)</strong>',
                                        re.S)
        self.pattern_othername = re.compile('>又名.*?</span>(.*?)<br.*?>', re.S)
        self.pattern_imdb = re.compile('>IMDb链接.*?</span>.*?<a.*?>(.*?)</a>.*?<br.*?>', re.S)
        self.pattern_intro = re.compile('<span.*?"v:summary".*?>(.*?)</span>',
                                        re.S)
        self.Lol = Lol()
        
        self.current_date = self.get_current_date()

    @staticmethod
    def get_current_date():
        return time.strftime('%y%m', time.localtime())

    def update_current_date(self):
        self.current_date = self.get_current_date()

    def _get_poster_url(self, cate_eng, filename):
        cur_date = self.current_date
        return '/static/images/%s/p/%s/%s' % (cate_eng, cur_date, filename)

    def _get_screenshot_url(self, cate_eng, filename):
        cur_date = self.current_date
        return '/static/images/%s/s/%s/%s' % (cate_eng, cur_date, filename)

    def get_douban_search_result(self, keyword, driver=None):
        """
        Search result based on movie name
        :param keyword: movie name
        :param driver: webdriver object
        :return: item url list
        """
        query = urllib.urlencode({'search_text': keyword, 'cat': '1002'})
        target = 'https://movie.douban.com/subject_search?' + query
        timer = 1
        while True:
            urls = []
            try:
                LOG.info('Querying Douban with %s' % keyword)
                driver.get(target)
                url_objs = driver.find_elements_by_css_selector(
                    '#root div.detail a[href^="https://movie.douban.com/subject"]')
                urls = [url.get_attribute('href') for url in url_objs]
            except WebDriverTimeOut:
                if timer >= 10:
                    return urls
                else:
                    continue
            except Exception as e:
                return urls
            else:
                return urls

    def _get_image_download_path(self, cate_eng, image_type):
        """

        :param cate_eng:
        :param image_type: p (poster) or s (screenshoot)
        :return:
        """
        assert image_type == 's' or image_type == 'p'
        cur_date = self.current_date
        download_path = os.path.join(DOWNLOAD_IMAGE_PATH, '%s_pic' % cate_eng,
                                     '%s_%s' % (cate_eng, image_type), cur_date)
        if not os.path.exists(download_path):
            LOG.info("Making directory %s ..." % download_path)
            os.makedirs(download_path)
        return download_path

    def _get_image_web_path(self, cate_eng, image_type):
        assert image_type == 's' or image_type == 'p'
        cur_date = self.current_date
        web_path = os.path.join(WEB_IMAGE_PATH, cate_eng, image_type, cur_date)
        if not os.path.exists(web_path):
            LOG.info("Making directory %s ..." % web_path)
            os.makedirs(web_path)
        return web_path

    @staticmethod
    def _save_poster(poster_url, download_path, filename):
        timer = 0
        while True:
            if timer >= 10:
                return False
            try:
                u = urllib.urlopen(poster_url)
                data = u.read()
                f = open(os.path.join(download_path, filename), 'wb')
                f.write(data)
                f.close()
                return True
            except IOError as e:
                timer += 1
                LOG.error('保存海报失败%d次: %s' % (timer, poster_url))
                time.sleep(2)
                continue

    def _get_poster(self, url, content, cate_eng):
        image_type = 'p'
        download_path = self._get_image_download_path(cate_eng, image_type)
        # 海报
        try:
            # 海报列表页内容
            posts_content = get_html_content("%sphotos?type=R" % url,
                                             url_log=False)
            # 拿到某海报页
            _p = ('<div.*?class="cover">.*?<a.*?"(.*?)".*?>.*?'
                  '<div.*?class="prop">\s*(.*?)\s*<')
            _p_item = re.compile(
                '<a.*?class="mainphoto".*?<img.*?"(.*?)".*?/>', re.S)
            poster_index = re.findall(_p, posts_content, re.S)
            poster_got = False
            poster_url = ''
            for p_url, px in poster_index:
                width, height = px.split('x')[0], px.split('x')[1]
                if int(height) / int(width) > 1.35 and int(height) / int(
                        width) < 1.49:
                    content2 = get_html_content(p_url, url_log=False)
                    item2 = re.findall(_p_item, content2)
                    poster_url = item2[0]
                    poster_got = True
                    break
            if not poster_got:
                for p_url, px in poster_index:
                    width, height = px.split('x')[0], px.split('x')[1]
                    if int(height) / int(width) > 1.22 and int(height) / int(
                            width) < 1.62:
                        content2 = get_html_content(p_url, url_log=False)
                        item2 = re.findall(_p_item, content2)
                        poster_url = item2[0]
                        poster_got = True
                        break
            if not poster_got:
                post_url = poster_index[0][0].strip()  # 第几张海报
                # print post_url
                content2 = get_html_content(post_url, url_log=False)
                item2 = re.findall(_p_item, content2)
                poster_url = item2[0]
        except IndexError:
            try:
                poster_pattern2 = '"nbgnbg".*?href.*?"(.*?)"'
                poster_url = re.findall(poster_pattern2, content)[0]
                filename = re.search(r'.*/(.*)', poster_url).group(1)
                # 数据库中海报的url
                poster = self._get_poster_url(cate_eng, filename)
                LOG.info('正在保存海报 ...')
                res = self._save_poster(poster_url, download_path, filename)
                if res:
                    LOG.info('保存海报成功')
                else:
                    LOG.info('保存海报失败')
                    poster = ''
            except Exception:
                LOG.info('保存海报失败')
                poster = ''
        else:
            # 海报图片名
            filename = re.search('.*\/(.*)', poster_url).group(1)
            # 数据库中海报的url
            poster = self._get_poster_url(cate_eng, filename)
            # 保存海报图片

            result = self._save_poster(poster_url, download_path, filename)

            # edit poster image
            if result:
                web_path = self._get_image_web_path(cate_eng, image_type)
                IP.edit_poster(download_path, filename, web_path)
                LOG.info('保存海报成功')
            else:
                poster = ''
                LOG.info('保存海报失败')
        return poster

    def _get_screenshot(self, url, cate_eng):
        image_type = 's'
        item_num = 0
        saved_num = 0
        ss_not_found = True
        ss_list = []
        ss_url = url + 'photos?type=S'
        ss_index_photo = get_html_content(ss_url, url_log=False)
        download_path = self._get_image_download_path(cate_eng, 's')

        capture_num_pattern = re.compile('<a.*?>.*?截图.*?\((.*?)\).*?<', re.S)
        photo_num_pattern = re.compile('<a.*?>.*?官方剧照.*?\((.*?)\).*?<', re.S)
        time.sleep(round(uniform(3, 5), 1))
        try:
            capture_num = re.findall(capture_num_pattern, ss_index_photo)[0]
            capture_num = str(
                capture_num).strip()  # .replace('(','').replace(')','')
            capture_num = int(capture_num)
            capture_page = int(round(capture_num / 40) + 1)  # 共有几页截图
        except Exception:
            capture_num = 0
            capture_page = 0

        try:
            photo_num = re.findall(photo_num_pattern, ss_index_photo)[0]
            photo_num = str(photo_num).strip()  # .replace('(','').replace(')','')
            photo_num = int(photo_num)
            photo_page = int(round(photo_num / 40) + 1)  # 共有几页官方剧照
        except Exception:
            photo_num = 0
            photo_page = 0
        LOG.info('截图共' + str(capture_page) + '页，剧照共' +
                 str(photo_page) + '页。')
        current_page = 0
        filename_list = []

        ss_pattern = re.compile(
            ('<div.*?class="cover">\s+<a.*?>\s+<img.*?src="(.*?)".*?>\s+</a>.*?'
             '<div.*?class="prop">\s*(.*?)\s*<'), re.S)
        ss_instance_pattern = r'^(http.*/)thumb(/.*.)(webp|jpg|jpeg)$'
        while ss_not_found:
            current_page += 1
            if current_page > capture_page:
                break
            LOG.info('正在匹配合适截图第' + str(current_page) + '页...')
            # "截图"页面的url
            ss_url = url + 'photos?type=S&start=' + str(
                item_num) + '&sortby=size&size=a&subtype=c'
            try:
                ss_index = get_html_content(ss_url, url_log=False)
            except Exception:
                break

            # 缩略图列表页的url和图片像素
            ss_page = re.findall(ss_pattern, ss_index)

            for ss_thumb_url, px in ss_page:
                try:
                    width = int(px.split('x')[0])
                    height = int(px.split('x')[1])
                except ValueError:
                    continue
                if 1.75 < width / height < 1.87:
                    # ss_content = get_html_content(ss_url, url_log=False)
                    # time.sleep(round(uniform(2, 4), 1))
                    # ss_pattern2 = re.compile(
                    #     '<a.*?class="mainphoto".*?<img.*?src="(.*?)".*?/>', re.S)
                    # try:
                    #     ss_instance_url = re.findall(ss_pattern2, ss_content)[0]
                    # except IndexError:
                    #     continue
                    # 根据thumb url得到大图url
                    ss_instance_url = re.sub(ss_instance_pattern,
                                             r'\1photo\2jpg', ss_thumb_url)
                    filename = re.search('.*\/(.*)', ss_instance_url).group(1)
                    if filename not in filename_list:
                        try:
                            u = urllib.urlopen(ss_instance_url)
                            data = u.read()
                        except Exception as e:
                            continue

                        filename_list.append(filename)
                        ss = self._get_screenshot_url(cate_eng, filename)
                        ss_list.append(ss)

                        LOG.info('正在保存第%d张截图...' % (saved_num + 1))
                        with open(os.path.join(download_path,
                                               filename), 'wb') as f:
                            f.write(data)

                        # edit image
                        web_path = self._get_image_web_path(cate_eng, image_type)
                        IP.edit_screenshot(download_path, filename, web_path)
                        saved_num += 1
                        time.sleep(1)
                        if saved_num == 4:
                            ss_not_found = False
                            break
            if item_num >= 320:
                break
            item_num += 40
            time.sleep(1)

        if saved_num < 4:
            item_num = 0
            current_page = 0
            # 保留剧照第一页内容，后面用
            while ss_not_found:
                current_page += 1
                if current_page > photo_page:
                    break
                LOG.info('正在匹配合适剧照第' + str(current_page) + '页...')
                ss_url = url + 'photos?type=S&start=' + str(
                    item_num) + '&sortby=size&size=a&subtype=o'

                try:
                    ss_index = get_html_content(ss_url, url_log=False)
                except Exception:
                    break

                ss_page = re.findall(ss_pattern, ss_index)
                for ss_thumb_url, px in ss_page:
                    try:
                        width = int(px.split('x')[0])
                        height = int(px.split('x')[1])
                    except ValueError:
                        continue
                    if 1.778 < width / height < 2.5:
                        # ss_content2 = get_html_content(ss_url, url_log=False)
                        # time.sleep(round(uniform(2, 4), 2))
                        # ss_pattern2 = re.compile(
                        #     '<a.*?class="mainphoto".*?<img.*?"(.*?)".*?/>', re.S)
                        # ss_instance_url = re.findall(ss_pattern2, ss_content2)[0]
                        # 根据thumb url得到大图url
                        ss_instance_url = re.sub(ss_instance_pattern,
                            r'\1photo\2jpg', ss_thumb_url)
                        filename = re.search('.*\/(.*)', ss_instance_url).group(1)
                        if filename not in filename_list:
                            try:
                                u = urllib.urlopen(ss_instance_url)
                                data = u.read()
                            except Exception as e:
                                continue

                            filename_list.append(filename)
                            ss = self._get_screenshot_url(cate_eng, filename)
                            ss_list.append(ss)
                            LOG.info('正在保存第%d张截图...' % (saved_num + 1))
                            with open(os.path.join(download_path, filename), 
                                      'wb') as f:
                                f.write(data)
                            web_path = self._get_image_web_path(cate_eng,
                                                                image_type)
                            IP.edit_screenshot(download_path, filename, web_path)
                            saved_num += 1
                            time.sleep(1)
                            if saved_num == 4:
                                ss_not_found = False
                                break

                if item_num >= 120:
                    break
                item_num += 40
                time.sleep(1)
        # 合适的剧照也没有，则按顺序保存图片
        if saved_num < 4:
            ss_page = re.findall(ss_pattern, ss_index_photo)
            if ss_page:
                LOG.info('只能随便选图了 ...')
            else:
                LOG.info('一张图也没有 ...')
            for ss_thumb_url, px in ss_page:
                try:
                    width = int(px.split('x')[0])
                    height = int(px.split('x')[1])
                except ValueError:
                    continue
                if 1.2 < width / height < 2.5:
                    # ss_content2 = get_html_content(ss_url, url_log=False)
                    # time.sleep(round(uniform(2, 4), 2))
                    # ss_pattern2 = re.compile(
                    #     '<a.*?class="mainphoto".*?<img.*?"(.*?)".*?/>', re.S)
                    # ss_instance_url = re.findall(ss_pattern2, ss_content2)
                    # if ss_instance_url:
                    #     ss_instance_url = ss_instance_url[0]
                    # else:
                    #     continue
                    ss_instance_url = re.sub(ss_instance_pattern,
                                             r'\1photo\2jpg', ss_thumb_url)
                    filename = re.search('.*\/(.*)', ss_instance_url).group(1)
                    if filename not in filename_list:
                        try:
                            u = urllib.urlopen(ss_instance_url)
                            data = u.read()
                        except Exception:
                            continue

                        filename_list.append(filename)
                        ss = self._get_screenshot_url(cate_eng, filename)
                        ss_list.append(ss)
                        LOG.info('正在保存第%d张截图...' % (saved_num + 1))
                        with open(os.path.join(
                                download_path, filename), 'wb') as f:
                            f.write(data)
                        web_path = self._get_image_web_path(cate_eng, image_type)
                        IP.edit_screenshot(download_path, filename, web_path)
                        saved_num += 1
                        time.sleep(1)
                        if saved_num == 4:
                            ss_not_found = False
                            break
        if saved_num < 4:
            pass
        screenshoot = ''
        try:
            ss1 = ss_list[0]
        except IndexError:
            ss1 = screenshoot
        try:
            ss2 = ss_list[1]
        except IndexError:
            ss2 = screenshoot
        try:
            ss3 = ss_list[2]
        except IndexError:
            ss3 = screenshoot
        try:
            ss4 = ss_list[3]
        except IndexError:
            ss4 = screenshoot

        return ss1, ss2, ss3, ss4

    def get_douban_name_info(self, content, cate_eng, cate_chn='',
                             enable_log=True):
        pattern_name = re.compile('<h1>.*?<span.*?"v:itemreviewed">(.*?)</span>',
                                  re.S)
        # 名字
        if cate_eng == MOVIE_NAME_ENG:
            names = re.findall(pattern_name, content)[0]
            if len(names.split()) == 2:
                name1 = names.split()[0]
                name2 = names.split()[1]
                name2 = name2.replace("&#39;", "'").replace("&amp;", "&").replace(
                    "&#34", '"')
            else:
                name1 = names.split()[0]
                name2 = ' '.join(names.split()[1:])
                name2 = name2.replace("&#39;", "'").replace("&amp;", "&").replace(
                    "&#34", '"')
        else:
            names = re.findall(pattern_name, content)[0]. \
                replace('&#39;', "'").replace('&amp;', "&").replace("&#34", '"')

            tmp = names.split()
            if len(tmp) == 2:
                if '第' in tmp[1] and '季' in tmp[1]:
                    name1 = self.text_handler.replace_symbol(
                        tmp[0] + ' ' + tmp[1])
                    name2 = ' '.join(tmp[2:])
                elif not re.search(u"[\u4e00-\u9fa5]+", u"tmp[1]"):  # 第二段若不含中文
                    name1 = self.text_handler.replace_symbol(tmp[0])
                    name2 = self.text_handler.replace_symbol(tmp[1])
                else:
                    name1 = self.text_handler.replace_symbol(
                        tmp[0] + ' ' + tmp[1])
                    name2 = ''
            elif len(tmp) == 1:
                name1 = self.text_handler.replace_symbol(tmp[0])
                name2 = ' '.join(tmp[1:])
                name2 = self.text_handler.replace_symbol(name2)
            else:  # 大于3
                if '第' in tmp[1] and '季' in tmp[1]:
                    name1 = tmp[0] + ' ' + tmp[1]
                    name2 = ' '.join(tmp[2:])
                elif not re.search(u"[\u4e00-\u9fa5]+", u"tmp[1]"):  # 第二段若不含中文
                    name1 = tmp[0].strip()
                    name2 = ' '.join(tmp[1:])
                else:
                    name1 = tmp[0].strip() + ' ' + tmp[1].strip()
                    name2 = ' '.join(tmp[2:])
            name1 = self.text_handler.replace_symbol(name1)
            name2 = self.text_handler.replace_symbol(name2)
            if enable_log:
                LOG.info('%s：《%s》' % (cate_chn, name1))
        return name1, name2

    def get_region(self, content, enable_log=True):
        try:
            region = re.findall(self.pattern_region, content)[0]
            region = re.sub(self.pattern_tag, '', region).strip()
        except IndexError:
            region = '未知'
            if enable_log:
                LOG.info('无国家地区信息，默认设为-未知')
        return region

    def get_type(self, content, enable_log=True):
        _type = re.findall(self.pattern_type, content)
        if _type:
            _type = re.sub(self.pattern_tag, '', _type[0]).strip()
            if len(_type) > 64:
                _type = '未知'
                if enable_log:
                    LOG.info('类型信息错误，默认设为-未知')
        else:
            _type = '未知'
            if enable_log:
                LOG.info('无类型信息，默认设为-未知')
        return _type

    def get_douban_text_info(self, content, cate_eng, cate_chn, enable_log=True):
        """
        Common info
        :param content:
        :param cate_eng:
        :param cate_chn:
        :return:
        """
        name1, name2 = self.get_douban_name_info(content, cate_eng,
                                                 cate_chn=cate_chn)
        # 年代
        year = re.findall(self.pattern_year, content)
        if year:
            year = year[0].replace('(', '').replace(')', '')
            if len(year) > 4:
                year = '1970'
        else:
            year = '1970'
            if enable_log:
                LOG.info('没有年代，设为1970年，记得修改')

        # 导演
        director = re.findall(self.pattern_director, content)
        if director:
            director = re.sub(self.pattern_tag, '', director[0])
            if len(director) > 256:
                director = ''
                if enable_log:
                    LOG.info('导演信息错误，默认设为空')
        else:
            director = ''
            if enable_log:
                LOG.info('无导演信息，默认设为空')

        # 编剧
        screenwriter = re.findall(self.pattern_screenwriter, content)
        if screenwriter:
            screenwriter = re.sub(self.pattern_tag, '', screenwriter[0])
            if len(screenwriter) > 100:
                screenwriter = director
        else:
            screenwriter = ''
            if enable_log:
                LOG.info('无编剧信息，默认设为空')

        # 演员
        actor = re.findall(self.pattern_actor, content)
        if actor:
            actor = re.sub(self.pattern_tag, '', actor[0])
            max_length = 512
            if len(actor) > max_length:
                actor_list = actor.split('/')
                if len(actor_list) > 10:
                    # over length
                    new_actor = ''
                    for item in actor_list:
                        if len(new_actor) < max_length + len(item) + 3:
                            new_actor += ' / %s' % item
                        else:
                            break
                    actor = new_actor
                else:
                    actor = ''
        else:
            actor = ''
            if enable_log:
                LOG.info('无主演信息，默认设为空')

        # 类型
        mtype = self.get_type(content, enable_log)

        # 国家地区
        region = self.get_region(content, enable_log)

        # 上映时间，若没有可能是电视剧（首播）
        if cate_eng == MOVIE_NAME_ENG:
            try:
                date_show = re.findall(self.pattern_shangying, content)[0]
                date_show = re.sub(self.pattern_tag, '', date_show).strip()
            except Exception:
                if not re.findall(self.pattern_shoubo, content):  # 没有上映且没有首播，设为默认
                    # date_show = year
                    date_show = ''
                else:
                    if enable_log:
                        LOG.info('啊哦，这可能是一部电视剧...继续匹配下一个')
                    time.sleep(round(uniform(2, 4), 1))
                    return 'continue'
            try:
                date = re.search('^(.*?)\(', date_show).group(1).strip()
                if re.search('^(.*?)\(', date_show) and len(date) > 10:
                    date = re.search('^(.*?)/', date_show).group(1).strip()
            except AttributeError:
                if re.search('^\d+\-\d+\-\d+$', date_show):
                    date = date_show
                else:
                    date = ''
        else:
            try:
                date_show = re.findall(self.pattern_shoubo, content)[0]
                date_show = re.sub(self.pattern_tag, '', date_show).strip()
                # print date_show
            except Exception:
                pattern_shangying = re.compile('>上映日期.*?</span>(.*?)<br.*?>',
                                               re.S)
                if re.findall(pattern_shangying, content):
                    # 没有上映且没有首播，设为空
                    if enable_log:
                        LOG.info('啊哦，这可能是一部电影...略过')
                    time.sleep(round(uniform(2, 4), 1))
                    return 'continue'
                else:
                    date_show = ''
            try:
                if date_show == '':
                    date = date_show
                else:
                    date = re.search('^(.*?)\(', date_show).group(1).strip()
                    if re.search('^(.*?)\(', date_show) and len(date) > 10:
                        date = re.search('^(.*?)\/', date_show).group(1).strip()
            except AttributeError:
                if re.search('^\d+\-\d+\-\d+$', date_show):
                    date = date_show
                else:
                    date = ''

        # 片长
        try:
            _text = '片长' if cate_eng == MOVIE_NAME_ENG else '单集片长'
            pattern_running_time = re.compile(
                '>%s.*?</span>(.*?)<br.*?>' % _text,
                re.S)
            running_time = re.findall(pattern_running_time, content)[
                0]
            running_time = re.sub(self.pattern_tag, '',
                                  running_time).strip()
        except IndexError:
            if enable_log:
                LOG.info('无片长时间，设为默认值-空')
            running_time = ''

        # 评分
        score = re.findall(self.pattern_score, content)[0]
        score = re.sub(self.pattern_tag, '', score).strip()
        if not score:
            try:
                pattern_imdb = '>IMDb链接.*?<a.*?href="(.*?)"'
                imdb_url = re.findall(pattern_imdb, content, re.S)[0]
                imdb_url = imdb_url.strip()
                imdb_content = get_html_content(imdb_url, url_log=False)
                score = re.findall('itemprop="ratingValue">(.*?)<',
                                   imdb_content, re.S)[0]
            except IndexError:
                score = 0
            try:
                score = float(score)
                if score < 0 or score > 10:
                    score = 0
            except Exception:
                score = 0

        # 又名
        other_name = re.findall(self.pattern_othername, content)
        if other_name:
            other_name = other_name[0].strip()
        else:
            other_name = ''

        # IMDB
        imdb = re.findall(self.pattern_imdb, content)
        if imdb:
            imdb = imdb[0].strip()
        else:
            imdb = ''

        # 简介
        try:
            intro = re.findall(self.pattern_intro, content)[0]
            intro = re.sub(self.pattern_tag, '', intro).strip()
            intro = re.sub(' {4}', '', intro)
            intro = re.sub('　', '', intro)
        except IndexError:
            intro = '暂无简介'
            if enable_log:
                LOG.info('无简介，设为默认值-暂无简介')

        return (name1, name2, year, director, screenwriter, actor, mtype, region,
                date_show, date, running_time, score, other_name, imdb, intro)

    def get_movie_info(self, d_url, d_content, l_url, l_content, compare_way, conn):

        text_info = self.get_douban_text_info(d_content, MOVIE_NAME_ENG,
                                             MOVIE_NAME_CH)
        if not isinstance(text_info, tuple):
            return text_info
        (name1, name2, year, director, screenwriter, actor, mtype,
         region, date_show, date, running_time, score, othername, imdb,
         intro) = text_info
        director_condition = None
        actor_condition = None
        cur = conn.cursor()
        if director:
            sql_director = ('SELECT id FROM movie_movie WHERE ch_name="%s" '
                             'and foreign_name="%s" and director="%s"'
                             % (name1, name2, director))
            director_condition = cur.execute(sql_director)
        elif actor:
            # 一般不可能同一个演员出演多部名字相同的电影
            sql_actor = ('SELECT id FROM movie_movie WHERE ch_name="%s" '
                         'and foreign_name="%s" and actor LIKE "%%%s%%"'
                         % (name1, name2, actor.split('/')[0]))
            actor_condition = cur.execute(sql_actor)

        # urls
        args = self.Lol.get_movie_down_urls(l_content)
        down_name1 = args[0]
        down_url1 = args[1]
        down_name2 = args[2]
        down_url2 = args[3]

        if director_condition or actor_condition:
            _id = None
            if director_condition:
                _id = director_condition.fetchone()[0]
            elif actor_condition:
                _id = actor_condition.fetchone()[0]
            if _id:
                sql_u = ('UPDATE movie_movie SET down_url=%s,down_name=%s,'
                        'down_url2=%s,down_name2=%s,link_addr=%s WHERE id="%s"')
                cur.execute(sql_u,
                            (down_url1, down_name1, down_url2, down_name2,
                             l_url, name1, name2, _id))
                conn.commit()
                LOG.info('《%s》更新成功' % name1)
                return 'movie_exists'
        cur.close()

        # 海报
        poster = self._get_poster(d_url, d_content, MOVIE_NAME_ENG)

        # 截图
        ss1, ss2, ss3, ss4 = self._get_screenshot(d_url, MOVIE_NAME_ENG)

        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        douban_sn = get_douban_sn(d_url)
        return (name1, name2, year, director, screenwriter, actor, mtype,
                region, date_show, date, running_time, othername, score,
                intro, poster, ss1, ss2, ss3, ss4, down_name1, down_url1,
                down_name2, down_url2, '正式片', '无视频', '无视频',
                l_url, douban_sn, imdb, compare_way, 0, 0, 0, create_date,
                create_date, MOVIE_NAME_ENG)

    def get_series_info(self, d_url, content, conn, l_url, cate_eng,
                        cate_chn, down_urls, down_names, updated_eps,
                        seq, compare_way):
        """
        For tv, anime and show
        :param d_url: douban url
        :param content: douban content
        :param conn:
        :param l_url:
        :param cate_eng:
        :param cate_chn:
        :param down_urls:
        :param down_names:
        :param updated_eps: series only
        :param seq: series only
        :param compare_way: 添加匹配方式
        :return: a tuple for database
        """
        # common info
        text_info = self.get_douban_text_info(content, cate_eng, cate_chn)
        if not isinstance(text_info, tuple):
            return text_info
        (name1, name2, year, director, screenwriter, actor, mtype,
         region, date_show, date, running_time, score, othername, imdb,
         intro) = text_info
        sql_name1 = ('SELECT ch_name FROM movie_tv WHERE ch_name="' + name1
                     + '";')
        sql_name2 = ('SELECT foreign_name FROM movie_tv where foreign_name="'
                     + name2 + '";')
        sql_name3 = ('SELECT ch_name FROM movie_show WHERE ch_name="' + name1
                     + '";')
        sql_name4 = ('SELECT foreign_name FROM movie_show where foreign_name="'
                     + name2 + '";')
        cur = conn.cursor()
        if cur.execute(sql_name1) and cur.execute(sql_name2):
            sqlu = ('UPDATE movie_tv SET down_names=%s,down_urls=%s,'
                    'updated_eps=%s,seq=%s,link_addr=%s WHERE ch_name=%s AND '
                    'foreign_name=%s')
            cur.execute(sqlu, (
                down_names, down_urls, updated_eps, seq, l_url, name1, name2))
            conn.commit()
            return 'tv_exists'
        elif cur.execute(sql_name3) and cur.execute(sql_name4):
            sqlu = ('UPDATE movie_show SET down_names=%s,down_urls=%s,'
                    'updated_eps=%s,seq=%s,link_addr=%s WHERE ch_name=%s AND '
                    'foreign_name=%s')
            # try:
            cur.execute(sqlu, (
                down_names, down_urls, updated_eps, seq, l_url, name1, name2))
            conn.commit()
            return 'show_exists'

        # 海报
        poster = self._get_poster(d_url, content, cate_eng)

        # 截图
        ss1, ss2, ss3, ss4 = self._get_screenshot(d_url, cate_eng)

        create_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        try:
            pattern_eps = re.compile('>集数:.*?</span>(.*?)<br', re.S)
            douban_eps = re.findall(pattern_eps, content)[0]
            douban_eps = re.sub(self.pattern_tag, '', douban_eps).strip()
            douban_eps = int(douban_eps)
        except Exception:
            LOG.info('集数错误，设置为默认值999')
            douban_eps = 999
        douban_sn = get_douban_sn(d_url)
        return (name1, name2, year, director, screenwriter, actor, mtype, region,
                date, date_show, douban_eps, running_time, othername, score,
                intro, poster, ss1, ss2, ss3, ss4, updated_eps, down_names,
                down_urls, l_url, douban_sn, imdb, compare_way, seq, 0, 0, 0,
                create_date, create_date, cate_eng)

    def compare_name(self, l_name, d_content, cate_eng):
        name1, _ = self.get_douban_name_info(d_content, cate_eng,
                                             enable_log=False)
        pattern = re.compile('^.*?第(.*?)季$', re.S)
        for item in l_name.split(r'/'):
            l_season = re.findall(pattern, item)
            d_season = re.findall(pattern, name1)
            l_name_s = l_name.split()
            d_name_s = name1.split()
            # 1. 都有第X季，必须相同
            if l_season and d_season:
                if len(l_name_s) >=2 and len(d_name_s) >=2:
                    # xxxx 第x季 ...
                    contrast_d = {'1': '一', '2': '二', '3': '三', '4': '四',
                                  '5': '五', '6': '六', '7': '七', '8': '八',
                                  '9': '九', '10': '十', '11': '十一', '12': '十二',
                                  '13': '十三', '14': '十四', '15': '十五'}
                    l_sn = l_season[0]
                    d_sn = d_season[0]
                    LOG.debug('l_sn: %s, d_sn: %s' % (l_sn, d_sn))
                    for k, v in contrast_d.items():
                        if l_sn == k:
                            l_sn = v
                        if d_sn == k:
                            d_sn = v
                    if l_name_s[0] == d_name_s[0] and l_sn == d_sn:
                        return True
            # 2. 一边有第X季，另一边没有，有可能豆瓣没有，lol有第一季
            elif l_season and not d_season:
                if l_season[0] in ('一', '1') and l_name_s[0] == d_name_s[0]:
                    return True
            # 3. 两边都没有，必须完全相同
            elif not l_season and not d_season:
                sy_list = (':', '：', '.', '。', ',', '，', '(', '（', ')',
                           '）', '[', '【', ']', '】', '-', '——')
                for s in sy_list:
                    item = item.replace(s, '')
                    name1 = name1.replace(s, '')
                if item == name1:
                    return True
        return False

    @staticmethod
    def compare_imdb(l_content, d_content):
        try:
            l_imdb = re.findall('<br>IMDb链接: (.*?)<', l_content, re.S)[0]
        except IndexError:
            return False
        p2 = re.compile('IMDb链接.*?<a.*?>(.*?)<', re.S)

        d_imdb = re.findall(p2, d_content)
        if not d_imdb:
            return False
        else:
            d_imdb = d_imdb[0]

        if l_imdb == d_imdb:
            LOG.info('IMDB match!')
            return True
        else:
            return False

    @staticmethod
    def compare_actor(content_l, content_d):
        actor_matches = False
        pattern_d_actor = re.compile('>主演.*?: (.*?)<br', re.S)
        pattern1 = '<.*?>'
        try:
            d_actor = re.findall(pattern_d_actor, content_d)[0]
            d_actor = re.sub(pattern1, '', d_actor)
            # d_actor = unicode(d_actor, 'utf-8')
        except IndexError:
            # 豆瓣无主演直接返回
            return False
        try:
            l_actor = re.findall('<br>主演: (.*?)\/', content_l, re.S)[0]
        except IndexError:
            # 尝试另一种匹配
            l_actor = re.findall('<li>主.*?演.*?：(.*?)</li>',
                                 content_l, re.S)
            if l_actor:
                l_actor = l_actor[0]
            else:
                return False
            for item in l_actor.split():
                if item.strip() in d_actor:
                    # pattern_name = re.compile(self.h1_name_pat, re.S)
                    # names = re.findall(pattern_name, content_d)[0]
                    # name1 = names.split(' ')[0].strip()
                    LOG.info('Actor matches!')
                    actor_matches = True
                    break

        for item in l_actor.split():
            if item.strip() in d_actor:
                LOG.info('Actor matches!')
                actor_matches = True
                break

        if actor_matches:
            # TODO: 可能会在同一系列电视剧匹配错误，如果带“第X季”，需要再匹配
            pass
        else:
            return False


class Lol(object):

    def __init__(self):
        self.text_handler = TextHandler()

    @staticmethod
    def get_new_urls(l_index_content, cate_chn):

        # 拿到最新部分
        latest_content = re.findall('最新%s</h2>.*?<ul>.*?</ul>' % cate_chn,
                                    l_index_content, re.S)[0]
        # 拿到最新URL列表
        item_pattern = '<li>.*?</p>.*?【(.*?)】.*?<a.*?href.*?"(.*?)">(.*?)</a>'
        latest_urls = re.findall(item_pattern, latest_content, re.S)

        if not latest_urls:
            raise GetLatestUrlsFailed
        return latest_urls

    def get_movie_down_urls(self, l_content):
        # l_content = l_content.decode('utf8')
        p_down = '<li.*?id="li.*?"><a.*?href.*?"(.*?)".*?>(.*?)<' #.decode('utf8')
        downurl_tmp = re.findall(p_down, l_content, re.S)  # 包括了磁力链接
        downurl = []
        for item in downurl_tmp:
            if not 'magnet:' in item[0]:
                downurl.append(item)
        downurl_filter = []
        magnet_list = []
        down_name1, down_url1, down_name2, down_url2 = None, None, None, None
        # print '总链接数：' + str(len(downurl_tmp))
        # print '迅雷链接数：' + str(len(downurl))
        # 若迅雷总链接数大于2，进行筛选
        if len(downurl) >= 2:
            # print '满足2个链接。。。。'
            selected = 0  # 已选数目
            # 对下载链接列表循环，找出最先符合条件的两个
            for url, name in downurl:
                # name = name.decode('gbk','ignore').encode('utf8')
                decoded_line = self.text_handler.decode_url(url)
                name = self.text_handler.movie_clean_name(name)

                if 'BD1280' in name and 'ed2k' in decoded_line:
                    url = self.text_handler.movie_process_urls(decoded_line, name)
                    downurl_filter.append((url, name))
                    selected += 1
                    if selected >= 2:
                        break

            for url, name in downurl:
                if selected >= 2:
                    break
                # name = name.decode('gbk','ignore').encode('utf8')
                decoded_line = self.text_handler.decode_url(url)
                name = self.text_handler.movie_clean_name(name)
                if 'HD1280' in name and 'ed2k' in decoded_line:
                    url = self.text_handler.decode_url(decoded_line)
                    downurl_filter.append((url, name))
                    selected += 1
                    if selected >= 2:
                        break

            for url, name in downurl:
                if selected >= 2:
                    break
                # name = name.decode('gbk','ignore').encode('utf8')
                decoded_line = self.text_handler.decode_url(url)
                name = self.text_handler.movie_clean_name(name)

                if '720p' in name and 'ed2k' in decoded_line:
                    url = self.text_handler.movie_process_urls(decoded_line, name)
                    downurl_filter.append((url, name))
                    selected += 1
                    if selected >= 2:
                        break

            for url, name in downurl:
                if selected >= 2:
                    break
                # name = name.decode('gbk','ignore').encode('utf8')
                decoded_line = self.text_handler.decode_url(url)
                name = self.text_handler.movie_clean_name(name)
                if 'ed2k:' in decoded_line:
                    url = self.text_handler.movie_process_urls(decoded_line, name)
                    downurl_filter.append((url, name))
                    selected += 1
                    if selected >= 2:
                        break
                elif 'magnet:' in url:
                    magnet_list.append((url, name))  # 先将磁力链接存起来

            if selected == 0:  # 循环完成，若都不满足，选前两个链接
                downurl_filter = downurl[:2]

            # 若满足一个，再选一个非ed2k链接
            elif selected == 1:
                # 再次循环下载链接列表
                for url1, name1 in downurl:
                    decoded_line = self.text_handler.decode_url(url1)
                    # 拿到一个非ed2k格式的链接
                    if 'ed2k:' not in decoded_line:
                        name1 = self.text_handler.movie_clean_name(name1)
                        downurl_filter.append((url1, name1))  # 天
                        selected += 1
                        break
            # print '下载列表长度' + str(len(downurl_filter))
            (down_name1, down_url1,
             down_name2, down_url2) = (downurl_filter[0][1], downurl_filter[0][0],
                                       downurl_filter[1][1], downurl_filter[1][0])

            if selected == 2:
                return down_name1, down_url1, down_name2, down_url2
                # print '总链接'+str(len(downurl))

        # 若没有一个迅雷链接，则找种子和磁力
        elif len(downurl) == 0:
            # print '没有链接。。。。'
            selected = 0
            try:  # 匹配两个种子的情况
                p_down1 = ('id="bt".*?<a.*?href.*?"(.*?)".*?>(.*?)</a>.*?'
                           '<a.*?href.*?"(.*?)".*?>(.*?)</a>.*?</ul>')
                bt_downurl1 = re.findall(p_down1, l_content, re.S)[0]  # 种子
                # print downurl
                down_name1 = bt_downurl1[1]
                down_name1 = self.text_handler.movie_clean_name(down_name1)
                down_url1 = bt_downurl1[0]
                selected += 1
                if 'thunder' in bt_downurl1[2]:  # 确保第二个种子匹配正确
                    down_name2 = bt_downurl1[3]
                    down_url2 = bt_downurl1[2]
                    down_name2 = self.text_handler.movie_clean_name(down_name2)
                    selected += 1
                else:  # 没有第二个种子
                    down_name2 = 'N/A'
                    down_url2 = '无下载'
            except Exception:  # 出错则匹配一个种子的情况
                try:
                    p_down2 = 'id="bt".*?<a.*?href.*?"(.*?)".*?>(.*?)</a>'
                    bt_downurl2 = re.findall(p_down2, l_content, re.S)[0]
                    down_name1 = bt_downurl2[1]
                    down_name1 = self.text_handler.movie_clean_name(down_name1)
                    down_url1 = bt_downurl2[0]
                    selected += 1
                    down_name2 = 'N/A'
                    down_url2 = '无下载'
                except IndexError:
                    down_name1 = down_name2 = 'N/A'
                    down_url1 = down_url2 = '无下载'

            if selected == 0:  # 迅雷链接和种子都没有
                # print '没有种子。。。。'
                if len(magnet_list) == 1:
                    down_url1, down_name1 = magnet_list[0][0], magnet_list[0][1]
                    down_name2 = 'N/A'
                    down_url2 = '无下载'
                elif len(magnet_list) > 1:
                    down_url1, down_name1 = magnet_list[0][0], magnet_list[0][1]
                    down_url2, down_name2 = magnet_list[1][0], magnet_list[1][1]
            elif selected == 1:  # 已找到一个迅雷链接或种子
                if len(magnet_list) >= 1:
                    down_url2, down_name2 = magnet_list[0][0], magnet_list[0][1]

        # 总链接数为1
        elif len(downurl) == 1:
            # print '一个链接。。。。。'
            url, name = downurl[0]
            name = self.text_handler.movie_clean_name(name)
            decoded_line = self.text_handler.decode_url(url)
            if 'ed2k:' in decoded_line:
                url = self.text_handler.movie_process_urls(decoded_line, name)
            else:
                pass
            downurl_filter.append((url, name))
            down_name1, down_url1 = name, url
            selected = 1
            # 匹配第一个种子，如果有的话
            try:
                pattern_bt = 'id="bt".*?<a.*?href.*?"(.*?)".*?>(.*?)</a>'
                bt_url = re.findall(pattern_bt, l_content, re.S)[0]
                down_name2 = bt_url[1]
                down_name2 = self.text_handler.movie_clean_name(down_name2)
                down_url2 = bt_url[0]
                selected += 1
            except IndexError:
                down_name2, down_url2 = 'N/A', '无下载'

            if selected == 1:
                if len(magnet_list) >= 1:
                    down_url2, down_name2 = magnet_list[0][0], magnet_list[0][1]

        return down_name1, down_url1, down_name2, down_url2
    
    def series_get_down_urls(self, l_content):
        """
        处理lol链接
        :param l_content:
        :return:
        """
        # name_input = args[1]
        eps_count = 0
        thunder_result_list = []
        origin_filename_list = []  # a标签显示的内容
        name_url_list, seq = self._get_series_name_url_list(l_content)
        for url, name in name_url_list:
            # 此处url已经base64 decode
            url = url.strip()
            if 'magnet:' in url:
                thunder_result = url
            elif 'ed2k:' in url:
                res = re.findall('.*?\|file\|.*?(\.\w+)\|.*', url)
                if res:
                    t_format = re.findall('.*?\|file\|.*?(\.\w+)\|.*', url)[0]
                    url_pattern = re.compile('(.*?\|file\|)(.*?)(\|.*)', re.S)
                    head = re.search(url_pattern, url).group(1)
                    tail = re.search(url_pattern, url).group(3)
                    # 若用户输入不空，得到文件名列表
                    filename = name + t_format
                    my_ed2k = head + filename + tail
                    thunder_result = self.text_handler.encode_url(my_ed2k)
                else:
                    thunder_result = url
            else:
                # ftp, http等
                thunder_result = self.text_handler.encode_url(url)
            thunder_result_list.append(thunder_result)
            origin_filename_list.append(name)
            eps_count += 1

        filename_str, thunder_str = '', ''
        for item in origin_filename_list:
            filename_str += item + NEW_LINE
        for item in thunder_result_list:
            thunder_str += item + NEW_LINE
        # print 'URLs处理完毕，共' + str(eps_num) + '集。'
        return filename_str, thunder_str, eps_count, seq

    def _get_series_name_url_list(self, l_content):
        seq = 1
        while True:  # 寻找720P的ed2k
            p = '.*<li.*?"li' + str(seq) + '.*?>.*?<a.*?href="(.*?)".*?>(.*?)</a>'
            new_list = []
            name_url_list = re.findall(p, l_content)
            if name_url_list:
                first_url = name_url_list[0][0]
                first_decode_url = self.text_handler.decode_url(first_url)
                if 'ed2k:' in first_decode_url and '720P' in first_decode_url:
                    for url, name in name_url_list:
                        new_list.append((self.text_handler.decode_url(url),
                                         name))
                    return new_list, seq
                else:
                    seq += 1
            else:
                break
        seq = 1
        while True:  # 寻找ed2k
            p = '.*<li.*?"li' + str(seq) + '.*?>.*?<a.*?href="(.*?)".*?>(.*?)</a>'
            new_list = []
            name_url_list = re.findall(p, l_content)
            if name_url_list:
                first_url = name_url_list[0][0]
                first_decode_url = self.text_handler.decode_url(first_url)
                if 'ed2k:' in first_decode_url:
                    for url, name in name_url_list:
                        new_list.append((self.text_handler.decode_url(url),
                                         name))
                    return new_list, seq
                else:
                    seq += 1
            else:
                break

        p1 = '.*<li.*?"li1.*?>.*?<a.*?href="(.*?)".*?>(.*?)</a>'
        name_url_list = re.findall(p1, l_content)
        if name_url_list:
            for url, name in name_url_list:
                new_list.append((self.text_handler.decode_url(url),
                                 name))
            return new_list, 1
        else:
            return [], 1


class TextHandler(object):

    def __init__(self):
        pass

    @staticmethod
    def replace_symbol(s):
        res = s.replace("&#39;", "'").replace("&amp;", "&").replace("&#34", '"')
        return res

    @staticmethod
    def movie_process_urls(ed2k_line, name):
        name = name.strip().replace('[心中的阳光原创]', '')
        try:
            t_format = re.findall('.*?\|file\|.*?(\.\w+[ ]?)\|.*', ed2k_line)[0]
            t_format = t_format.strip()
        except IndexError:
            return ''
        url_pattern = re.compile('(.*?\|file\|)(.*?)(\|.*)', re.S)
        head = re.search(url_pattern, ed2k_line.strip()).group(1)
        tail = re.search(url_pattern, ed2k_line.strip()).group(3)

        filename = name + t_format

        my_ed2k = head + filename + tail
        final_ed2k = ('AA' + my_ed2k + 'ZZ').strip()
        thunder_result = 'thunder://' + base64.b64encode(final_ed2k)
        return thunder_result

    @staticmethod
    def movie_clean_name(name):
        name = str(name)
        s1 = ('【.*?】', '\[lol.*?\]', '\(lol.*?\)',
              '\[bt.*?\]', '\[www.*?\]', '\(www.*?\)',
              )
        for item in s1:
            name = re.sub(item, '', name, re.I)
        # name = re.sub('【.*?】', '', str(name))
        # name = re.sub('\[LOL.*?\]', '', name)
        # name = re.sub('\[lol.*?\]', '', name)
        # name = re.sub('\[bt.*?\]', '', name)
        # name = re.sub('\[www.*?\]', '', name)
        # name = re.sub('\(www.*?\)', '', name)
        # name = re.sub('\(lol.*?\)', '', name)
        name = name.replace('-LOL电影天堂', '')
        name = name.replace('bt猪猪', '')
        return name

    @staticmethod
    def encode_url(url):
        """
        Encode http and ftp url to thunder url
        :param url:
        :return:
        """
        url = 'AA%sZZ' % url
        thunder_result = 'thunder://' + base64.b64encode(url)
        return thunder_result

    @staticmethod
    def decode_url(url):
        try:
            org_url = url.decode('gbk', 'ignore').encode('utf8', 'ignore')
        except Exception as e:
            LOG.error('decode url failed: %s' % str(e))
            return url
        if 'magnet:' in org_url:
            decoded_line = org_url
        elif 'thunder:' in org_url:
            base64_line = str(org_url).strip().replace('thunder://', '')
            try:
                decoded_line = base64.urlsafe_b64decode(base64_line)
            except Exception as e:
                LOG.error('base64 decode failed: %s' % str(e))
                return org_url
            else:
                decoded_line = re.sub('^AA', '', decoded_line)
                decoded_line = re.sub('ZZ$', '', decoded_line)
                decoded_line = decoded_line.decode('gbk').encode('utf8')
        else:
            decoded_line = org_url
        return decoded_line


if __name__ == '__main__':
    l_content = get_html_content('http://www.loldytt.com/Anime/MWZWHTD/')
    name_url_list, seq = Lol()._get_series_name_url_list(l_content)
    for k,v in name_url_list:
        print k
        print v
