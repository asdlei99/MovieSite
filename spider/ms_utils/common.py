# coding=utf-8
import random
import re
import socket
import time
import urllib2

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from ms_constants import WEB_DRIVER_CHROME, WEB_DRIVER_PHANTOMJS, PHANTOMJS, \
    CHROME, HEADER_CHROME_1, HEADERS
from ms_exceptions import *
from ms_utils import log

LOG = log.Log()

dcap = dict(DesiredCapabilities.PHANTOMJS)
DEFAULT_TIMEOUT = 180


def get_html_content(url, url_log=True):
    url = str(url).strip()
    timer = 1
    while True:
        # if timer > 10:
        #     LOG.error('Tried %d times constantly, take a break' % timer)
        #     timer = 1
        #     time.sleep(60)
        try:
            if url_log:
                LOG.info(url)
            request = urllib2.Request(url, headers=HEADER_CHROME_1)
            response = urllib2.urlopen(request, timeout=DEFAULT_TIMEOUT)
            content = response.read()
            response.close()
            break
        except urllib2.HTTPError as e:
            LOG.error('%s：HTTPError %s' % (url, e.code))
            if str(e.code) == '404':
                raise Http404
            time.sleep(10)
            timer += 1
        except urllib2.URLError as e:
            LOG.error('%s：URLError %s' % (url, e.reason))
            time.sleep(10)
            timer += 1
        except socket.timeout as e:
            LOG.error('%s：%s' % (url, str(e)))
            time.sleep(10)
            timer += 1
        except socket.error as e:
            LOG.error('%s：%s' % (url, str(e)))
            time.sleep(2)
            timer += 1

    # for special case
    if len(content) < 500 and 'loldytt' in url:
        res = re.findall(r'window.location=(.*?)[;|<]', content, re.S)
        if len(res) == 1:
            location = 'http://www.loldytt.com' + res[0].replace('"',
                                                                 '').replace(
                ' ', '').replace('+', '')
            return get_html_content(location)
        raise InvalidHTMLContent('The content is not valid')
    return content


def get_webdriver(set_headers=False, disable_load_image=False):
    driver = None
    if PHANTOMJS or CHROME:
        try:
            if PHANTOMJS:
                if set_headers:
                    dcap["phantomjs.page.settings.userAgent"] = (
                    random.choice(HEADERS))
                if disable_load_image:
                    dcap["phantomjs.page.settings.loadImages"] = False
                driver = webdriver.PhantomJS(WEB_DRIVER_PHANTOMJS)
            elif CHROME:
                driver = webdriver.Chrome(WEB_DRIVER_CHROME)
            driver.set_page_load_timeout(DEFAULT_TIMEOUT)
        except Exception as e:
            raise e
        else:
            return driver
    else:
        raise WebDriverNotSet


def get_douban_sn(d_url):
    sn = None
    res = re.findall(r'http.*?/subject/(\d+)/$', d_url)
    if res:
        sn = res[0]
    return sn


def get_douban_url(sn):
    return 'https://movie.douban.com/subject/%s/' % sn


def format_lol_name(name):
    name = re.sub('^(.*)\(.*?\)$', r'\1', name)
    name = re.sub(r'^([^\s]+)(第.*?季.*)$', r'\1 \2', name)
    return name


if __name__ == '__main__':

    def get_lol_index():
        driver = None
        try:
            driver = get_webdriver(disable_load_image=True, set_headers=True)
            driver.get('http://www.loldytt.com')
        except WebDriverTimeOut:
            pass
        except Exception as e:
            if driver:
                driver.quit()
            raise e
        else:
            driver.quit()
            pass

    get_lol_index()
