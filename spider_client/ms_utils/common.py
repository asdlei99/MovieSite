# coding=utf-8
import re
import socket
import time
import urllib2
import random

from ms_constants import HEADER_CHROME_1, HEADER_FF_1, HEADER_IE_1, HEADERS
from ms_exceptions import *
from ms_utils import log

LOG = log.Log()

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
            time.sleep(random.uniform(5, 10))
            timer += 1
        except urllib2.URLError as e:
            LOG.error('%s：URLError %s' % (url, e.reason))
            time.sleep(random.uniform(5, 10))
            timer += 1
        except socket.timeout as e:
            LOG.error('%s：%s' % (url, str(e)))
            time.sleep(random.uniform(2, 10))
            timer += 1
        except socket.error as e:
            LOG.error('%s：%s' % (url, str(e)))
            time.sleep(2, 5)
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


def get_douban_sn(d_url):
    sn = None
    res = re.findall(r'http.*?/subject/(\d+)/$', d_url)
    if res:
        sn = res[0]
    return sn


def get_douban_url(sn):
    return 'https://movie.douban.com/subject/%s/' % sn


if __name__ == '__main__':

    pass
