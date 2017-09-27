# coding=utf-8
import requests
import time
import random
import re

from ms_constants import *
from ms_exceptions import *
from ms_utils.common import get_html_content
from ms_utils.html_helper import Lol
from ms_utils.log import Log


Lol = Lol()
LOG = Log()


DEFAULT_TIMEOUT = 60

SHOW_EXCEPTION = ('综艺大集合', )


class Main(object):

    def __init__(self):
        self.new_operation = list()
        self.manual_list = list()

        # initialize paths
        # LOG.info('Initializing paths ...')
        for item in NEW_PATHS:
            if not os.path.exists(item):
                os.makedirs(item)
        # get driver
        # LOG.info('Initializing drivers ...')
        # self.driver = get_webdriver()

    @staticmethod
    def _format_lol_name(name):
        name = re.sub('^(.*)\(.*?\)$', r'\1', name, re.S)
        name = re.sub('^(.*?)(第.*?季.*)$', r'\1 \2', name, re.S)
        return name

    @staticmethod
    def _get_to_do_name_urls(all_type_url_name_list, cate_eng):
        all_urls = [item[1] for item in all_type_url_name_list]
        latest_url = LOG.read_latest_url(cate_eng)
        LOG.debug('latest_url: %s' % latest_url)
        try:
            index = all_urls.index(latest_url)
        except ValueError:
            index = None
        LOG.debug('index: %s' % index)
        if index is None:
            to_do_name_urls = all_type_url_name_list
        else:
            to_do_name_urls = all_type_url_name_list[:index]
        return to_do_name_urls

    @staticmethod
    def operation(op_type, state, l_url, l_name, cate_eng, cate_chn):
        assert op_type in ('添加', '更新')
        return {'type': op_type, 'state': state, 'l_url':l_url, 'l_name': l_name,
                'cate_eng': cate_eng, 'cate_chn': cate_chn}

    @staticmethod
    def _add_new_movie(d_url):
        data = {'name': '',
                'url': '',
                'content': '',
                'secret': '5826f119-c0bc-4ad7-9017-30369eb75b75',
                'tag': '',
                'cate_eng': 'movie',
                'd_url': d_url}
        print 'Requesting...'
        try:
            time_start = time.time()
            r = requests.post('http://www.bigedianying.com/spider/crawl/',
                              data=data, timeout=300.0)
            time_end = time.time()
            print 'Response: %s, Cost: %f' % (r.content, time_end - time_start)
        except Exception as e:
            print str(e)

    def add(self, d_url=None):

        l_url = None
        l_name = l_content = tag = cate_eng = ''

        while not d_url or 'douban' not in d_url:
            d_url = raw_input('Douban URL: ')
            if d_url == 'start':
                print 'Enter into multi-task'
                self.manual_list = []
                end = False
                while not end:
                    _d_url = raw_input('Douban URL: ')
                    if _d_url and 'douban' in _d_url:
                        self.manual_list.append(_d_url.strip())
                    elif _d_url == 'end':
                        print 'Multi-task start'
                        break
                for item in self.manual_list:
                    self._add_new_movie(item)
                print 'Multi-task end'
                return

        while not l_url or 'loldytt' not in l_url:
            l_url = raw_input('Lol URL: ')
            if l_url == '':
                break
        # it will skip comparing if d_url is not None
        l_url = l_url.strip()
        d_url = d_url.strip()
        if l_url:
            l_content = get_html_content(l_url).decode(
                'gbk', 'ignore').encode('utf-8')
            title = re.findall(r'<h1>(.*?)<a.*?>(.*?)</a>', l_content, re.S)[0]
            if len(title) != 2:
                raise ValueError
            info = title[0].replace('&gt;', '').strip()
            if '电影' in info:
                cate_eng = 'movie'
                tag = info.replace('电影', '')
            elif '电视剧' in info:
                cate_eng = 'tv'
                tag = info.replace('电视剧', '')
            elif '动漫' in info:
                cate_eng = 'anime'
                tag = info.replace('动漫', '')
            elif '综艺' in info:
                cate_eng = 'show'
                tag = info.replace('综艺', '')
            else:
                raise ValueError

            l_name = self._format_lol_name(title[1])
        else:
            while not cate_eng:
                cate_eng = raw_input('cate_eng(default is movie): ')
                if cate_eng == '':
                    cate_eng = 'movie'
                    break
                if cate_eng not in ('movie', 'tv', 'anime', 'show'):
                    cate_eng = None

        data = {'name': l_name,
                'url': l_url,
                'content': l_content,
                'secret': '5826f119-c0bc-4ad7-9017-30369eb75b75',
                'tag': tag,
                'cate_eng': cate_eng,
                'd_url': d_url}
        print 'Requesting...'
        try:
            time_start = time.time()
            r = requests.post('http://www.bigedianying.com/spider/crawl/',
                              data=data, timeout=300.0)
            time_end = time.time()
            print 'Response: %s, Cost: %f' % (r.content, time_end - time_start)
        except Exception as e:
            print str(e)

    def start(self):
        """
        Spider Entrance
        :return:
        """

        try:
            LOG.info('Fetching lol index page ...')
            l_index_content = get_html_content(
                'http://www.loldytt.com/', url_log=False).decode(
                'gbk', 'ignore').encode('utf8', 'ignore')

            # 首先根据记录（上次更新的lol第一条url）拿到当前需要更新的列表
            for cate in CATES_ENG_CH.items():
                cate_eng = cate[0]
                cate_chn = cate[1]
                all_type_url_name_list = Lol.get_new_urls(l_index_content, cate_chn)
                to_do_list = self._get_to_do_name_urls(all_type_url_name_list,
                                                       cate_eng)
                for index, (l_type, l_url, l_name) in enumerate(to_do_list):
                    try:
                        # start update
                        LOG.split_line('%s %s/%s' % (cate_chn, index+1, len(to_do_list)))
                        # start job
                        l_content = get_html_content(l_url).decode(
                            'gbk', 'ignore').encode('utf-8')
                        l_name = self._format_lol_name(l_name)
                        pass

                        # #
                        # Server_Main().update(l_type, l_url, l_name, l_content, cate_eng)

                        #
                        data = {'name': l_name,
                                'url': l_url,
                                'content': l_content,
                                'secret': '5826f119-c0bc-4ad7-9017-30369eb75b75',
                                'tag': l_type,
                                'cate_eng': cate_eng}
                        print 'Requesting...'
                        try:
                            r = requests.post('http://www.bigedianying.com/spider/crawl/',
                                              data=data, timeout=300.0)
                        except Exception as e:
                            print str(e)
                        else:
                            print 'Response: %s' % r.content
                    except Exception as e:
                        if isinstance(e, Warn):
                            continue
                        elif isinstance(e, Fatal):
                            raise
                        else:
                            LOG.error('Update failed: %s' % str(e))
                            continue
                    finally:
                        time.sleep(random.uniform(5, 15))
                # 记录
                latest_name_url = to_do_list[0] if to_do_list else None
                if latest_name_url:
                    LOG.write_latest_url(latest_name_url[1], cate_eng)
        except KeyboardInterrupt as e:
            LOG.debug(str(e))
        except Exception as e:
            LOG.debug('Unexpected exit: %s' % str(e))
            raise e
        else:
            LOG.info('Update End')
        # finally:
        #     if self.driver:
        #         self.driver.close()
        #         self.driver.quit()
        #     # TODO: send mail


if __name__ == '__main__':
    Main().add()
