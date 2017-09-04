# coding=utf-8
"""
Update douban_addr and socre for db
"""
import urllib
import re
import os
from ms_utils.db_helper import connect_db
from ms_utils.html_helper import Douban
from ms_utils.common import get_webdriver, get_html_content, get_douban_sn, \
    get_douban_url
from ms_utils.log import Log
from ms_constants import CATES_ENG_CH, UPDATE_SCORE_PATH, MOVIE_NAME_ENG, \
    TV_NAME_ENG, ANIME_NAME_ENG, SHOW_NAME_ENG

LOG = Log()
Douban = Douban()


def _replace_symbol(s):
    res = s.replace("&#39;", "'").replace("&amp;", "&").replace("&#34", '"')
    return res


def _update(url, sid, cate_eng, ch_name, foreign_name, douban_sn_old, imdb_sn_old,
            score_old, conn, force=False):
    """

    :param url:
    :param sid:
    :param cate_eng:
    :param ch_name:
    :param foreign_name:
    :param douban_sn_old:
    :param imdb_sn_old:
    :param score_old:
    :param conn:
    :param force: Force to update
    :return:
    """
    content = get_html_content(url)
    cate_chn = CATES_ENG_CH.get(cate_eng)
    db_value = Douban.get_douban_text_info(
        content, cate_eng, cate_chn, enable_log=False)
    if db_value == 'continue':
        return 'mismatch'
    else:
        (name1, name2, year, director, screenwriter, actor, mtype,
         region, date_show, date, running_time, score_new, othername,
         imdb_sn_new, intro) = db_value
    score_new = float(score_new)
    condition = True if force else (name1 == ch_name and name2 == foreign_name)
    if condition:
        set_clause = 'SET score="%s"' % score_new
        if not douban_sn_old:
            douban_sn_new = get_douban_sn(url)
            if douban_sn_new:
                set_clause += ',douban_sn="%s"' % douban_sn_new
        if not imdb_sn_old:
            set_clause += ',imdb_sn="%s"' % imdb_sn_new
        sql = ('UPDATE movie_%s %s WHERE id=%s' % (cate_eng, set_clause, sid))
        try:
            _cur = conn.cursor()
            _cur.execute(sql)
            conn.commit()
            _cur.close()
        except Exception as e:
            LOG.info('%5s  FAILED  %s %s %s' % (cate_chn, name1, name2, str(e)),
                     path=UPDATE_SCORE_PATH,
                     filename='update_score.log')
            return 'error'
        LOG.info('%5s %3.1f(%3.1f) %s %s' %
                 (cate_chn, score_old, score_new, name1, name2),
                 path=UPDATE_SCORE_PATH,
                 filename='update_score.log')
        return 'ok'
    else:
        return 'mismatch'


def _compare_info(d_url, ch_name_db, foreign_name_db,
                  director_db, actor_db, year_db, region_db, cate_eng, conn):
    """
    比较名字（30），年代（10），国家地区（10），导演（25），演员（25）
    :return:
    """
    d_content = get_html_content(d_url, url_log=False)
    text_info = Douban.get_douban_text_info(d_content, cate_eng)
    if not isinstance(text_info, tuple):
        return text_info
    (name1, name2, year, director, screenwriter, actor, mtype,
     region, date_show, date, running_time, score, othername, imdb,
     intro) = text_info

    director_db = director_db.split('/')[0].strip()
    actor_db = actor_db.split('/')[0].strip()
    weight = 0

    # name
    if ch_name_db == name1 and foreign_name_db == name2:
        LOG.debug('Name match (30)')
        weight += 30
    if director_db in director:
        LOG.debug('Director match (25)')
        weight += 25
    if actor_db in actor:
        LOG.debug('Actor match (25)')
        weight += 25
    # TODO



def main():
    """
    Update Douban link and score
    :return:
    """
    if not os.path.exists(UPDATE_SCORE_PATH):
        os.makedirs(UPDATE_SCORE_PATH)
    conn = connect_db()

    driver = get_webdriver()
    for cate_eng in ('movie', 'tv', 'anime', 'show'):
        sid = 10
        while True:
            print sid
            cur = conn.cursor()
            cur.execute('SELECT ch_name, foreign_name, score, director, actor, '
                        'year, region, douban_sn, imdb_sn FROM movie_%s '
                        'WHERE id=%d' % (cate_eng, sid))
            res = cur.fetchone()
            cur.close()
            if res:
                res = (item.encode('utf-8') for item in res)
                (ch_name, foreign_name, score_old, director, actor, year,
                 region, douban_sn_old, imdb_sn_old) = res
                score_old = float(score_old)
                if douban_sn_old:
                    url = get_douban_url(douban_sn_old)
                    _update(url, sid, cate_eng, ch_name, foreign_name,
                            douban_sn_old, imdb_sn_old, score_old, conn, force=True)

                else:
                    urls = Douban.get_douban_search_result(ch_name, driver)
                    for url in urls:
                        # 对比豆瓣与数据库信息
                        res = _compare_info(url, ch_name, foreign_name,
                                            director, actor, year,
                                            region, cate_eng, conn)
                        if res:
                            result = _update(url, sid, cate_eng, ch_name,
                                             foreign_name, douban_sn_old, imdb_sn_old,
                                             score_old, conn)
                            if result == 'ok' or result == 'error':
                                sid += 1
                                break
                            elif result == 'mismatch':
                                continue

                    LOG.info('%5s  FAILED  %s %s' % (CATES_ENG_CH.get(cate_eng),
                                                     ch_name, foreign_name),
                             path=UPDATE_SCORE_PATH,
                             filename='update_score.log')
                sid += 1

            else:
                sid += 1


if __name__ == '__main__':
    main()