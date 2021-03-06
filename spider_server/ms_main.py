# coding=utf-8
from __future__ import division

import random
# import jieba
import re
import time
# from subprocess import check_output, CalledProcessError


from ms_constants import *
from ms_exceptions import Warn, Fatal
from ms_utils.log import Log
from ms_utils.common import get_html_content, get_webdriver
from ms_utils.db_helper import connect_db
from ms_utils.html_helper import Douban, TextHandler, Lol

LOG = Log()
Douban = Douban()
Lol = Lol()
TextHandler = TextHandler()


class Media(object):

    def __init__(self):
        pass

    @staticmethod
    def clean_lol_name(lol_name):
        return re.sub(r'^(.*?)\(.*?\)$', r'\1', lol_name)

    @staticmethod
    def type_matches(d_type, l_type):
        """
        for movie comparision
        :param d_type:
        :param l_type:
        :return:
        """
        LOG.debug('d_type: %s, l_type: %s' % (d_type, l_type))
        return True if l_type in d_type else False

    @staticmethod
    def region_matches(d_region, l_region):
        """
        for tv comparision
        :param d_region: 日本, 美国, 台湾 ...
        :param l_region: 日剧, 美剧, 台剧 ...
        :return:
        """
        paris = (('日剧', '日本'),
                 ('韩剧', '韩国'),
                 ('大陆', '大陆'),
                 ('港剧', '香港'))
        LOG.debug('d_region: %s, l_region: %s' % (d_region, l_region))
        for l, d in paris:
            if l == l_region and d in d_region:
                LOG.debug('region match 1')
                return True
        if l_region == '美剧':
            non_western = ('大陆', '香港', '台湾', '日本',
                           '新加坡', '韩国', '泰国', '印度')
            for item in non_western:
                if item in d_region:
                    return False
            LOG.debug('region match 2')
            return True

    """
    def name_matches(self, d_name, l_name):
        # pre process
        l_name = self.clean_lol_name(l_name)
        l_name1, l_name2 = None, None
        for item in ('/', '\\'):
            if item in l_name:
                res = l_name.split(item)
                if len(res) == 2:
                    l_name1, l_name2 = res
                    break
                else:
                    pass

        if l_name1 and l_name2:
            l_names = [l_name1, l_name2]
        else:
            l_names = [l_name]
        for l_name in l_names:
            # jieba
            l_cut = [item for item in jieba.cut(l_name)]
            d_cut = [item for item in jieba.cut(d_name)]
            # 移除特殊字符
            sy_list = (u':', u'：', u'.', u'。', u',', u'，', u'(', u'（', u')',
                       u'）', u'[', u'【', u']', u'】', u'-', u'——')
            for item in (d_cut, l_cut):
                for s in sy_list:
                    if s in item:
                        item.remove(s)
            # 计算匹配率
            # TODO，有第X季，及1,2,3等不准
            is_in = 0
            is_not_in = 0
            for item in l_cut:
                if item in d_cut:
                    is_in += 1
                else:
                    is_not_in += 1
            for item in d_cut:
                if item in l_cut:
                    is_in += 1
                else:
                    is_not_in += 1

            rate = is_in / (is_in + is_not_in)
            res = True if rate > 0.8 else False
            LOG.info('名字匹配%s 匹配度%.2f%%' % (res, round(rate, 4) * 100))
            if res:
                return res
            else:
                continue
        res = False
        return res
    """


class Movie(Media):
    """
    For movie
    """
    def __init__(self):
        super(Movie, self).__init__()

    @staticmethod
    def update(down_name1, down_url1, down_name2, down_url2, l_url, conn):
        """
        Update movie
        :param down_name1
        :param down_url1
        :param down_name2
        :param down_url2
        :param l_url
        :param conn:
        :return:
        """

        sqli = ("UPDATE %s" % MOVIE_TABLE +
                " SET down_name=%s,down_url=%s,down_name2=%s, "
                "down_url2=%s WHERE link_addr=%s")
        db_value = (down_name1, down_url1, down_name2, down_url2, l_url)
        assert all(db_value)
        try:
            cur = conn.cursor()
            cur.execute(sqli, db_value)
            conn.commit()
            cur.close()
        except Exception:
            return False
        else:
            return True

    @staticmethod
    def _select_name(lol_name):
        lol_name = re.sub('^(.*)\(.*?\)$', r'\1', lol_name)
        return lol_name

    def add(self, l_type, l_url, l_name, l_content,  conn, driver, cate_eng):
        search_name = self._select_name(l_name)
        douban_name_url_list = Douban.get_douban_search_result(
            search_name, driver)

        # 对列表电影进行循环，判断正确性
        LOG.info('正在匹配%s……' % cate_eng)
        db_value = ()
        compare_way = ''
        for d_url in douban_name_url_list:  # 对搜索结果的电影进行逐一判断
            d_content = get_html_content(d_url, url_log=False)
            time.sleep(round(random.uniform(3, 5), 1))
            # 首先判断对应性：1.IMDb链接 || 2.前两个演员
            imdb_match = Douban.compare_imdb(l_content, d_content)
            actor_match = Douban.compare_actor(l_content, d_content, l_name,
                                               cate_eng)
            if imdb_match or actor_match:
                if imdb_match:
                    compare_way = 'imdb'
                elif actor_match:
                    compare_way = 'actor'
                # 可能会由于电影存在而进行link_addr更新
                db_value = Douban.get_movie_info(d_url, d_content, l_url,
                                                 l_content, compare_way, conn)
                if db_value == 'continue':
                    continue
                else:
                    break  # 找到后跳出对搜索列表的循环
            elif Douban.compare_name(l_name, d_content, cate_eng):
                # d_type = Douban.get_type(d_content, enable_log=False)
                # if self.type_matches(d_type, l_type) or len(l_name) > 3:
                #     db_value = Douban.get_movie_info(d_url, d_content, l_url,
                #                                      l_content, conn)
                #     if db_value == 'continue':
                #         continue
                #     else:
                #         break  # 找到后跳出对搜索列表的循环
                # else:
                #     continue
                compare_way = 'name'
                db_value = Douban.get_movie_info(d_url, d_content, l_url,
                                                 l_content, compare_way, conn)
                if db_value == 'continue':
                    continue
                else:
                    break  # 找到后跳出对搜索列表的循环
            else:
                # d_name, _ = Douban.get_douban_name_info(d_content, cate_eng,
                #                                         enable_log=False)
                # d_type = Douban.get_type(d_content, enable_log=False)
                # if self.name_matches(d_name, l_name) and self.type_matches(
                #         d_type, l_type):
                #     db_value = Douban.get_movie_info(d_url, d_content, l_url,
                #                                      l_content, conn)
                #     if db_value == 'movie_exists':
                #         return db_value
                #     elif db_value == 'continue':
                #         continue
                pass

        sqli = ("INSERT INTO " + MOVIE_TABLE + " (ch_name,foreign_name,year,"
                                               "director,"
                "screenwriter, actor,types,region,release_date_show,release_date,"
                "running_time,other_name,score,intro,poster,ss1,ss2,ss3,ss4,"
                "down_name,down_url,down_name2,down_url2,video_type,video,video2,"
                "link_addr,douban_sn,imdb_sn,compare_way,visit_count,week_visit_count,"
                                               "month_visit_count,"
                "create_date,update_date,cate) VALUES(%s" + ",%s" * 35 + ")")
        if db_value:
            cur = conn.cursor()
            cur.execute(sqli, db_value)
            conn.commit()
            return True
        else:
            LOG.debug('db_value: %s' % str(db_value))
            LOG.debug('Add %s failed' % cate_eng)
            return False


class Series(Media):
    """
    For tv, anime and show
    """

    def __init__(self, cate_eng):
        super(Series, self).__init__()
        d = {TV_NAME_ENG: (TV_NAME_CH, TV_NAME_ENG, TV_TABLE),
             ANIME_NAME_ENG: (ANIME_NAME_CH, ANIME_NAME_ENG, ANIME_TABLE),
             SHOW_NAME_ENG: (SHOW_NAME_CH, SHOW_NAME_ENG, SHOW_TABLE)}
        info = d.get(cate_eng)
        if info:
            self.CH_NAME = info[0]
            self.ENG_NAME = info[1]
            self.DB_NAME = info[2]

    def update(self, down_names, down_urls, updated_eps, seq,
               l_url, conn):
        sql_update = ("UPDATE %s" % self.DB_NAME +
                " SET down_names=%s,down_urls=%s,updated_eps=%s," +
                "seq=%s WHERE link_addr=%s")
        sql1 = "SELECT down_names FROM %s " % self.DB_NAME + "WHERE link_addr=%s"
        cur = conn.cursor()
        cur.execute(sql1, (l_url,))
        tmp_num1 = len(cur.fetchall())  # 查到的旧的内容
        tmp_num2 = len(down_names.splitlines())  # 拿到的更新内容
        if tmp_num2 < tmp_num1:
            return False
        db_value = (down_names, down_urls, updated_eps, seq, l_url)
        if all(db_value):
            try:
                cur.execute(sql_update, db_value)
                conn.commit()
                cur.close()
            except Exception:
                return False
            else:
                return True
        else:
            return False

    def add(self, l_region, l_url, l_name, l_content, conn, driver, cate_eng):
        # 处理lolname
        # search_name = format_lol_name(l_name)  # 豆瓣搜索用
        search_name = l_name
        '''
        **Get douban search list**
        '''
        not_match = False
        db_value = ()
        douban_name_url_list = list()
        try:
            douban_name_url_list = Douban.get_douban_search_result(
                search_name, driver)
            if not douban_name_url_list and '第一季' in search_name:
                # not_match = True
                time.sleep(1)
                search_name = search_name.replace('第一季', '').strip()
                douban_name_url_list = Douban.get_douban_search_result(
                    search_name, driver)
                if not douban_name_url_list:
                    not_match = True
                    # 若未匹配到，也记录
                    LOG.info('无搜索结果1')
                    LOG.info_record(l_name, l_url)
            elif not douban_name_url_list:
                not_match = True
                # 若未匹配到，也记录
                LOG.info('无搜索结果2')
                LOG.info_record(l_name, l_url)
        except Exception as e:
            not_match = True
            LOG.info('Querying Failed')
            LOG.info_record(l_name, l_url)

        '''
        ** Match series **
        '''
        # 对series进行循环，判断正确性
        if not not_match:
            LOG.debug('douban_name_url_list length: %s' % len(douban_name_url_list))
            LOG.info('正在匹配 ...')
            cate_chn = CATES_ENG_CH.get(cate_eng)
            filename_str = str()
            thunder_str = str()
            eps_num = 0
            seq = 0
            compare_way = ''
            LOG.debug('douban_name_url_list: %s' % str(douban_name_url_list))
            for d_url in douban_name_url_list:  # 对搜索结果的电影进行逐一判断
                LOG.debug('豆瓣详情页: %s' % str(d_url))
                db_value = None
                try:
                    d_content = get_html_content(d_url, url_log=False)
                    LOG.debug('详情页长度为：%d' % len(d_content))
                except Exception as e:
                    LOG.debug('matching exception: %s' % str(e))
                    raise
                # time.sleep(round(random.uniform(3, 5), 1))
                # 首先判断对应性：1.IMDb链接 || 2.前两个演员（·替换为·） || 3.简介的前几个字
                imdb = Douban.compare_imdb(l_content, d_content)
                actor = Douban.compare_actor(l_content, d_content, l_name)
                LOG.info('IMDB: %s' % imdb)
                LOG.info('ACTOR: %s' % actor)
                if imdb or actor:
                    if imdb:
                        compare_way = 'imdb'
                        LOG.info('IMDB matching')
                    elif actor:
                        compare_way = 'actor'
                        LOG.info('actor matching')

                    # 拿到lol页面中一组迅雷url
                    (filename_str,
                     thunder_str,
                     eps_num, seq) = Lol.series_get_down_urls(l_content)
                    db_value = Douban.get_series_info(d_url, d_content, conn,
                                                      l_url, cate_eng,
                                                      cate_chn, thunder_str,
                                                      filename_str, eps_num, seq,
                                                      compare_way)

                elif Douban.compare_name(search_name, d_content, cate_eng):
                    (filename_str,
                     thunder_str,
                     eps_num, seq) = Lol.series_get_down_urls(l_content)
                    compare_way = 'name'
                    LOG.info('name matching')
                    db_value = Douban.get_series_info(d_url, d_content, conn,
                                                      l_url, cate_eng,
                                                      cate_chn, thunder_str,
                                                      filename_str, eps_num, seq,
                                                      compare_way)

                else:
                    # d_name, _ = Douban.get_douban_name_info(d_content, cate_eng,
                    #                                         enable_log=False)
                    # d_region = Douban.get_region(d_content, enable_log=False)
                    # if self.name_matches(d_name, l_name) and self.region_matches(
                    #         d_region, l_region):
                    #     db_value = Douban.get_series_info(d_url, d_content, conn,
                    #                                       l_url, cate_eng,
                    #                                       cate_chn, thunder_str,
                    #                                       filename_str, eps_num,
                    #                                       seq)
                    # else:
                    #     continue
                    LOG.info('Not matching')
                    continue

                if db_value and db_value == 'continue':
                    continue
                else:
                    LOG.debug('dbvalue is not "continue"')
                    break

            if db_value == '%s_exists' % self.ENG_NAME:
                self.update(down_names=filename_str,
                            down_urls=thunder_str,
                            updated_eps=eps_num,
                            seq=seq,
                            l_url=l_url,
                            conn=conn)
                return True
            elif db_value and isinstance(db_value, tuple):
                self._insert_db(db_value, conn)
                return True
            else:
                LOG.debug('db_value: %s' % str(db_value))
                LOG.debug('Add %s failed' % cate_eng)
                return False

    def _insert_db(self, db_value, conn):
        dbkey = (
            'ch_name', 'foreign_name', 'year', 'director', 'screenwriter',
            'actor', 'types', 'region', 'release_date', 'release_date_show',
            'eps', 'running_time', 'other_name', 'score', 'intro', 'poster',
            'ss1', 'ss2', 'ss3', 'ss4', 'updated_eps', 'down_names', 'down_urls',
            'link_addr', 'douban_sn', 'imdb_sn', 'compare_way','seq',
            'visit_count', 'week_visit_count',
            'month_visit_count', 'create_date', 'update_date', 'cate')

        sqli = "INSERT INTO %s " % self.DB_NAME + str(dbkey).replace("'", "") + \
               ' VALUES(' + '%s,' * 33 + '%s)'

        if db_value:
            try:
                cur = conn.cursor()
                cur.execute(sqli, db_value)
                conn.commit()
            except Exception as e:
                LOG.error('MySQL error: %s' % str(e))
                pass
            else:
                cur.close()
                LOG.info('写入数据库成功')


class Main(object):

    def __init__(self):
        self.new_operation = list()
        timer = 1
        while True:
            try:
                self.conn = connect_db()
                break
            except Exception:
                time.sleep(5)
                # TODO: may need to restart mysqld
                if timer >= 10:
                    break
                timer += 1
        # initialize paths
        LOG.info('Initializing paths ...')
        for item in NEW_PATHS:
            if not os.path.exists(item):
                os.makedirs(item)
        # get driver
        LOG.info('Initializing drivers ...')
        self.driver = get_webdriver()

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

    def _item_exists(self, url, cate_eng):
        _TABLE_NAME = 'movie_%s' % cate_eng
        # Check if item exists
        sql = ('SELECT id FROM %s' % _TABLE_NAME + ' WHERE link_addr=%s')
        cur = self.conn.cursor()
        num = cur.execute(sql, (url,))  # 按link_addr查询
        # item_num = len(cur.fetchall())
        cur.close()
        return num

    def update(self, l_tag, l_url, l_name, l_content, cate_eng):
        """

        :param l_tag: l_tag is type of movie or region of tv
        :param l_url:
        :param l_name:
        :param l_content:
        :param cate_eng:
        :return:
        """
        try:
            cate_chn = CATES_ENG_CH.get(cate_eng)
            if cate_eng == MOVIE_NAME_ENG:
                # for movie
                movie = Movie()
                if self._item_exists(l_url, cate_eng):
                    (down_name1, down_url1, down_name2,
                     down_url2) = Lol.get_movie_down_urls(l_content)
                    op_type = '更新'
                    LOG.info('%s%s《%s》' % (op_type, cate_chn, l_name))
                    result = movie.update(down_name1, down_url1, down_name2, down_url2,
                                          l_url, self.conn)
                else:
                    op_type = '添加'
                    LOG.info('%s%s《%s》' % (op_type, cate_chn, l_name))
                    result = movie.add(l_tag, l_url, l_name, l_content, self.conn,
                                       self.driver, cate_eng)
            else:
                # for tv, anime and show
                series = Series(cate_eng)
                if self._item_exists(l_url, cate_eng):
                    (down_names,
                     down_urls,
                     updated_eps, seq) = Lol.series_get_down_urls(l_content)
                    op_type = '更新'
                    LOG.info('%s%s《%s》' % (op_type, cate_chn, l_name))
                    result = series.update(down_names, down_urls, updated_eps, seq,
                                           l_url, self.conn)
                else:
                    op_type = '添加'
                    LOG.info('%s%s《%s》' % (op_type, cate_chn, l_name))
                    result = series.add(l_tag, l_url, l_name, l_content, self.conn,
                                        self.driver, cate_eng)
            result = '成功' if result else '失败'
            LOG.info('%s%s' % (op_type, result))
            self.new_operation.append(self.operation(op_type, result, l_url,
                                                     l_name, cate_eng, cate_chn))
        except Exception as e:
            LOG.debug('Update Exception: %s' % str(e))
            self.driver.close()
            self.driver.quit()
            raise e
        else:
            self.driver.close()
            self.driver.quit()

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
        # try:
        #     check_output('ps -ef | grep ms_main.py', shell=True)
        # except CalledProcessError as e:
        #     LOG.error(str(e))
        #     pass
        # else:
        #     pass
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
                    # 需要更新时间使目录名一致
                    Douban.update_current_date()
                    l_content = get_html_content(
                        url=l_url, url_log=False).decode(
                        'gbk', 'ignore').encode('utf8', 'ignore')
                    try:
                        # start update
                        LOG.split_line(index+1)
                        self.update(l_tag=l_type,
                                    l_url=l_url,
                                    l_name=l_name,
                                    l_content=l_content,
                                    cate_eng=cate_eng)
                        time.sleep(1.5)
                    except Exception as e:
                        if isinstance(e, Warn):
                            continue
                        elif isinstance(e, Fatal):
                            raise
                        else:
                            LOG.error('Update failed: %s' % str(e))
                            continue
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
            LOG.info('更新结束')
        finally:
            if self.driver:
                self.driver.close()
                self.driver.quit()
            # TODO: send mail


if __name__ == '__main__':
    m = Main()
    m.start()

