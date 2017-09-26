# coding=utf-8
import requests
import time
import random
import re
import chardet

from ms_constants import *
from ms_exceptions import *
from ms_utils.common import get_html_content
from ms_utils.html_helper import Lol
from ms_utils.log import Log
from spider.ms_main import Main as Server_Main

Lol = Lol()
LOG = Log()


DEFAULT_TIMEOUT = 60


class Main(object):

    def __init__(self):
        self.new_operation = list()

        # initialize paths
        LOG.info('Initializing paths ...')
        for item in NEW_PATHS:
            if not os.path.exists(item):
                os.makedirs(item)
        # get driver
        # LOG.info('Initializing drivers ...')
        # self.driver = get_webdriver()

    @staticmethod
    def _format_lol_name(name):
        name = re.sub('^(.*)\(.*?\)$', r'\1', name, re.U)
        name = re.sub('^(.*?)(第.*?季.*)$', r'\1 \2', name, re.U)
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
                print 'All %ss: %d' % (cate_eng, len(all_type_url_name_list))
                to_do_list = self._get_to_do_name_urls(all_type_url_name_list,
                                                       cate_eng)
                print 'To Do %ss: %d' % (cate_eng, len(to_do_list))
                for index, (l_type, l_url, l_name) in enumerate(to_do_list):
                    try:
                        # start update
                        LOG.split_line(index+1)
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
                        r = requests.post('http://www.bigedianying.com/crawl/',
                                          data=data)
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
    Main().start()
