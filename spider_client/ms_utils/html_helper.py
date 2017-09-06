# coding=utf-8
from __future__ import division

import base64
import os
import re
import time
import urllib
from random import uniform

from common import get_html_content, get_douban_sn
from ms_constants import DOWNLOAD_IMAGE_PATH, WEB_IMAGE_PATH, MOVIE_NAME_ENG, \
    MOVIE_NAME_CH, NEW_LINE
from ms_exceptions import *
from ms_utils import log

LOG = log.Log()


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
