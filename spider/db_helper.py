# coding=utf-8
import MySQLdb

from ms_constants import DB_PASS, DB_NAME, DB_PORT, DB_USER, DB_HOST
import log

Log = log.Log()


def connect_db(db_host=DB_HOST):
    # 连接数据库
    # Log.info('Connecting to %s@%s:%s ...' % (DB_USER, db_host, DB_PORT))
    try:

        conn = MySQLdb.connect(host=db_host, port=DB_PORT, user=DB_USER,
                               passwd=DB_PASS, db=DB_NAME, charset='utf8')
    except Exception as e:
        Log.error(str(e))
        raise
    return conn


if __name__ == '__main__':
    conn = connect_db()
    cur = conn.cursor()
    sql_director = ('SELECT id FROM movie_movie WHERE ch_name="%s" '
                    'and foreign_name="%s" and director="%s"'
                    % ('至尊计状元', '至尊計狀元才', '黄泰来 / 向华胜'))
    print cur.execute(sql_director)
    print cur.fetchone()
