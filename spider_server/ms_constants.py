# coding=utf-8
import os

""" common """
MOVIE_NAME_CH = '电影'
MOVIE_NAME_ENG = 'movie'
TV_NAME_CH = '电视剧'
TV_NAME_ENG = 'tv'
ANIME_NAME_CH = '动漫'
ANIME_NAME_ENG = 'anime'
SHOW_NAME_CH = '综艺'
SHOW_NAME_ENG = 'show'
CATES_ENG_CH = {MOVIE_NAME_ENG: MOVIE_NAME_CH,
                TV_NAME_ENG: TV_NAME_CH,
                ANIME_NAME_ENG: ANIME_NAME_CH,
                SHOW_NAME_ENG: SHOW_NAME_CH
                }

NEW_LINE = '\n'


""" path """
# need change to the directory where you place the spider in
WORKSPACE_PATH = r'E:\PycharmProjects\MovieSite\spider_server'
LOG_PATH = os.path.join(WORKSPACE_PATH, 'logs')
DOWNLOAD_IMAGE_PATH = os.path.join(WORKSPACE_PATH, 'images')

# change this to the site's directory .../static/images
WEB_IMAGE_PATH = r'E:\PycharmProjects\MovieSite\static\images'

NEW_PATHS = (WORKSPACE_PATH, DOWNLOAD_IMAGE_PATH)

""" log """
LOL_LINK_FILE = os.path.join(LOG_PATH, 'lol_%s_link.log')
UPDATE_SCORE_PATH = os.path.join('logs', 'update_score')
LOG_DEBUG = False

# only one can be enabled
PHANTOMJS = True
CHROME = False

# modify driver's path
WEB_DRIVER_PHANTOMJS = r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe'
WEB_DRIVER_CHROME = r'D:\chromedriver.exe'

""" images """
P_HEIGHT = 284
P_WIDTH = 200
S_HEIGHT = 242
S_WIDTH = 430

""" db """
DB_HOST = '192.168.100.11'
DB_PORT = 3306
DB_USER = 'root'
DB_PASS = 'kevin123'
DB_NAME = 'MovieSite'
MOVIE_TABLE = 'movie_movie'
TV_TABLE = 'movie_tv'
ANIME_TABLE = 'movie_anime'
SHOW_TABLE = 'movie_show'

""" html """
HEADER_CHROME_1 = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/webp,image/apng,*/*;q=0.8',
}

HEADER_FF_1 = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 '
                  'Firefox/54.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

HEADER_IE_1 = {
    'Connection': 'Keep-Alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) '
                  'like Gecko',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

HEADERS = (HEADER_CHROME_1, HEADER_FF_1, HEADER_IE_1)
PROXY_HOST = '116.196.101.221'
PROXY_PORT = 8088
# PROXY_HOST = '123.57.216.98'
# PROXY_PORT = 8080
