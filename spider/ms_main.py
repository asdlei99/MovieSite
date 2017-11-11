# coding=utf-8
from __future__ import division

import random
# import jieba
import re
import time
# from subprocess import check_output, CalledProcessError


from ms_constants import *
from ms_exceptions import Warn, Fatal
import log
from common import get_html_content, get_webdriver
from db_helper import connect_db
from html_helper import Douban, TextHandler, Lol

LOG = log.Log()
Douban = Douban()
Lol = Lol()
TextHandler = TextHandler()


class Media(object):

    def __init__(self):
        pass

    @staticmethod
    def clean_lol_name(lol_name):
        return re.sub(r'^(.*?)\(.*?\)$', r'\1', lol_name)

    def add(self, l_type, l_url, l_name, l_content,  conn, driver, cate_eng, d_url):
        pass

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

    def format_lol_name(self, lol_name):
        result = None
        for item in lol_name.split(r'/'):
            if re.findall(r'.*?第.*?季$', item.strip(), re.S):
                result = item.strip()
                break
        if not result:
            result = lol_name.split(r'/')[0].strip()
        return result


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
        except Exception as e:
            LOG.error(str(e))
            return False
        else:
            return True

    @staticmethod
    def _select_name(lol_name):
        lol_name = re.sub('^(.*)\(.*?\)$', r'\1', lol_name)
        return lol_name

    def _insert_db(self, db_value, conn):
        sqli = ("INSERT INTO " +
                MOVIE_TABLE +
                " (ch_name,foreign_name,year,"
                "director,"
                "screenwriter, actor,types,region,release_date_show,release_date,"
                "running_time,other_name,score,intro,poster,ss1,ss2,ss3,ss4,"
                "down_name,down_url,down_name2,down_url2,video_type,video,video2,"
                "link_addr,douban_sn,imdb_sn,compare_way,visit_count,week_visit_count,"
                "month_visit_count,"
                "create_date,update_date,cate) VALUES(%s" + ",%s" * 35 + ")")
        cur = conn.cursor()
        cur.execute(sqli, db_value)
        conn.commit()

    def add(self, l_type, l_url, l_name, l_content,  conn, driver, cate_eng, d_url):
        if d_url:
            d_content = get_html_content(d_url, url_log=False)
            db_value = Douban.get_movie_info(d_url, d_content, l_url,
                                             l_content, 'manual', conn)
        else:
            search_name = self._select_name(l_name)
            douban_name_url_list = Douban.get_douban_search_result(
                search_name, driver)

            # 对列表电影进行循环，判断正确性
            LOG.info('正在匹配%s……' % cate_eng)
            db_value = ()
            compare_way = ''
            for _d_url in douban_name_url_list:  # 对搜索结果的电影进行逐一判断
                d_content = get_html_content(_d_url, url_log=False)
                time.sleep(round(random.uniform(3, 5), 1))
                # 首先判断对应性：1.IMDb链接 || 2.前两个演员
                imdb_match = Douban.compare_imdb(l_content, d_content)
                actor_match = Douban.compare_actor(l_content, d_content, l_name)
                if imdb_match or actor_match:
                    if imdb_match:
                        compare_way = 'imdb'
                    elif actor_match:
                        compare_way = 'actor'
                    # 可能会由于电影存在而进行link_addr更新
                    db_value = Douban.get_movie_info(_d_url, d_content, l_url,
                                                     l_content, compare_way, conn)
                elif Douban.compare_name(l_name, d_content, cate_eng):
                    compare_way = 'name'
                    db_value = Douban.get_movie_info(_d_url, d_content, l_url,
                                                     l_content, compare_way, conn)
                else:
                    LOG.debug('Not matching')
                    continue

                if db_value == 'continue':
                    continue
                else:
                    break  # 找到后跳出对搜索列表的循环

        if db_value and isinstance(db_value, tuple):
            self._insert_db(db_value, conn)
            return True
        elif db_value == 'movie_exists':
            # updated already
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
            except Exception as e:
                LOG.error(str(e))
                return False
            else:
                return True
        else:
            return False

    def add(self, l_region, l_url, l_name, l_content, conn, driver, cate_eng, d_url):
        cate_chn = CATES_ENG_CH.get(cate_eng)
        if d_url:
            d_content = get_html_content(d_url, url_log=False)
            (filename_str,
             thunder_str,
             eps_num, seq) = Lol.series_get_down_urls(l_content)
            db_value = Douban.get_series_info(d_url, d_content, conn,
                                              l_url, cate_eng,
                                              cate_chn, thunder_str,
                                              filename_str, eps_num, seq,
                                              'manual')
        else:
            # search_name = format_lol_name(l_name)  # 豆瓣搜索用
            search_name = l_name
            '''
            **Get douban search list**
            '''
            db_value = ()

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
                        # 若未匹配到，也记录
                        LOG.info('无搜索结果1')
                        LOG.info_record(l_name, l_url)
                        return False
                elif not douban_name_url_list:
                    # 若未匹配到，也记录
                    LOG.info('无搜索结果2')
                    LOG.info_record(l_name, l_url)
                    return False
            except Exception as e:
                LOG.info('Querying Failed: %s' % str(e))
                LOG.info_record(l_name, l_url)
                return False

            '''
            ** Match series **
            '''
            # 对series进行循环，判断正确性

            LOG.debug('douban_name_url_list length: %s' % len(douban_name_url_list))
            LOG.info('正在匹配 ...')
            filename_str = str()
            thunder_str = str()
            eps_num = 0
            seq = 0
            compare_way = ''
            LOG.debug('douban_name_url_list: %s' % str(douban_name_url_list))
            for _d_url in douban_name_url_list:  # 对搜索结果的电影进行逐一判断
                LOG.debug('豆瓣详情页: %s' % str(_d_url))
                db_value = None
                try:
                    d_content = get_html_content(_d_url, url_log=False)
                    LOG.debug('详情页长度为：%d' % len(d_content))
                except Exception as e:
                    LOG.debug('matching exception: %s' % str(e))
                    raise
                # time.sleep(round(random.uniform(3, 5), 1))
                imdb = Douban.compare_imdb(l_content, d_content)
                actor = Douban.compare_actor(l_content, d_content, l_name)
                LOG.debug('IMDB: %s' % imdb)
                LOG.debug('ACTOR: %s' % actor)
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
                    db_value = Douban.get_series_info(_d_url, d_content, conn,
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
                    db_value = Douban.get_series_info(_d_url, d_content, conn,
                                                      l_url, cate_eng,
                                                      cate_chn, thunder_str,
                                                      filename_str, eps_num, seq,
                                                      compare_way)

                else:
                    LOG.info('Not matching')
                    continue

                if db_value == 'continue':
                    LOG.debug('dbvalue is "continue"')
                    # In some cases, anime may be a movie, so add it
                    if cate_eng == 'anime':
                        LOG.info('这部动画可能是电影，添加电影……')
                        Movie().add(l_region, l_url, l_name, l_content,
                                    conn, driver, cate_eng, d_url=_d_url)
                        break
                    continue
                else:
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
        # LOG.info('Initializing paths ...')
        for item in NEW_PATHS:
            if not os.path.exists(item):
                os.makedirs(item)
        # get driver
        # LOG.info('Initializing drivers ...')
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
        if not url:
            return 0, cate_eng
        _TABLE_NAME = 'movie_%s' % cate_eng
        # Check if item exists
        sql = ('SELECT * FROM %s' % _TABLE_NAME + ' WHERE link_addr="%s"')
        cur = self.conn.cursor()
        num = cur.execute(sql % url)  # 按link_addr查询
        LOG.debug('SQL: %s, num: %d' % ((sql % url), num))
        if not num:
            if cate_eng == 'anime':
                sql = 'SELECT * FROM movie_tv WHERE link_addr="%s"'
                num = cur.execute(sql % url)
                if num:
                    LOG.info('cate is anime, but found in movie_tv')
                    cate_eng = 'tv'
            elif cate_eng == 'tv':
                sql = 'SELECT * FROM movie_anime WHERE link_addr="%s"'
                num = cur.execute(sql % url)
                if num:
                    LOG.info('cate is tv, but found in movie_anime')
                    cate_eng = 'anime'
            elif cate_eng == 'show':
                sql = 'SELECT * FROM movie_tv WHERE link_addr="%s"'
                num = cur.execute(sql % url)
                if num:
                    LOG.info('cate is show, but found in movie_tv')
                    cate_eng = 'tv'

        cur.close()
        return num, cate_eng

    def update(self, l_tag, l_url, l_name, l_content, cate_eng, d_url=None):
        """

        :param l_tag: l_tag is type of movie or region of tv
        :param l_url:
        :param l_name:
        :param l_content:
        :param cate_eng:
        :param d_url: manually add if this is True
        :return:
        """
        try:
            cate_chn = CATES_ENG_CH.get(cate_eng)
            if cate_eng == MOVIE_NAME_ENG:
                # for movie
                movie = Movie()
                num, cate_eng = self._item_exists(l_url, cate_eng)
                if num:
                    (down_name1, down_url1, down_name2,
                     down_url2) = Lol.get_movie_down_urls(l_content)
                    op_type = '更新'
                    LOG.info('------ %s%s《%s》 ------' % (op_type, cate_chn, l_name))
                    result = movie.update(down_name1, down_url1, down_name2, down_url2,
                                          l_url, self.conn)
                else:
                    op_type = '添加'
                    LOG.info('------ %s%s《%s》 ------' % (op_type, cate_chn, l_name))
                    result = movie.add(l_tag, l_url, l_name, l_content, self.conn,
                                       self.driver, cate_eng, d_url)
            else:
                # for tv, anime and show
                series = Series(cate_eng)
                num, cate_eng = self._item_exists(l_url, cate_eng)
                if num:
                    (down_names,
                     down_urls,
                     updated_eps, seq) = Lol.series_get_down_urls(l_content)
                    op_type = '更新'
                    LOG.info('------ %s%s《%s》 ------' % (op_type, cate_chn, l_name))
                    result = series.update(down_names, down_urls, updated_eps, seq,
                                           l_url, self.conn)
                else:
                    op_type = '添加'
                    LOG.info('------ %s%s《%s》 ------' % (op_type, cate_chn, l_name))
                    result = series.add(l_tag, l_url, l_name, l_content, self.conn,
                                        self.driver, cate_eng, d_url)
            result = '成功' if result else '失败'
            LOG.info('%s%s' % (op_type, result))
            LOG.info_record(l_name, l_url)
            self.new_operation.append(self.operation(op_type, result, l_url,
                                                     l_name, cate_eng, cate_chn))
            self.driver.close()
            self.driver.quit()
            return op_type, result

        except Exception as e:
            LOG.debug('Update Exception: %s' % str(e))
            self.driver.close()
            self.driver.quit()
            raise e

    @staticmethod
    def operation(op_type, state, l_url, l_name, cate_eng, cate_chn):
        assert op_type in ('添加', '更新')
        return {'type': op_type, 'state': state, 'l_url': l_url, 'l_name': l_name,
                'cate_eng': cate_eng, 'cate_chn': cate_chn}

    def update_score(self):
        for item in ('movie', 'tv', 'anime', 'show'):
            sql = ('SELECT id, ch_name, douban_sn FROM movie_%s WHERE score=0 '
                   'AND douban_sn!=""' % item)
            try:
                cur = self.conn.cursor()
                cur.execute(sql)  # 按link_addr查询
                media = cur.fetchall()
                cur.close()
                LOG.info('Total counts: %s %s' % (len(media), item))
                for m in media:
                    _id, ch_name, douban_sn = m
                    d_content = get_html_content(Douban.get_url_from_sn(
                        douban_sn))
                    (name1, name2, year, director, screenwriter, actor, mtype, region,
                     date_show, date, running_time, score, other_name, imdb, intro
                     ) = Douban.get_douban_text_info(d_content, item, enable_log=False)
                    if not score == 0:
                        _sql = ('UPDATE movie_%s SET ch_name="%s", foreign_name="%s",'
                                ' year="%s", director="%s", screenwriter="%s", actor="%s",'
                                ' types="%s", region="%s", release_date_show="%s",'
                                ' release_date="%s", running_time="%s", score=%s,'
                                ' other_name="%s", imdb_sn="%s", intro="%s"'
                                ' WHERE id=%s' %
                                (item, name1, name2, year, director, screenwriter,
                                 actor, mtype, region, date_show, date,
                                 running_time, score, other_name, imdb,
                                 intro, _id))
                        _cur = None
                        try:
                            _cur = self.conn.cursor()
                            _cur.execute(_sql)
                            self.conn.commit()
                        except Exception as e:
                            LOG.error('Update %s %s score failed: %s' %
                                      (item, ch_name, str(e)))
                            _cur.close()
                        else:
                            _cur.close()
                            LOG.info('Update %s %s score successfully: %s' %
                                     (item, ch_name, score))
                    time.sleep(3)
            except Exception as e:
                LOG.error('Unexpected error: %s' % str(e))
                return False
        return True

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
    # m = Main()
    # m.start()
    Main()._item_exists('http://www.loldytt.com/Zuixinmeiju/JPLMDWJ/', 'tv')
