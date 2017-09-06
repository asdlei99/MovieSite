# coding=utf-8
import time

from ms_constants import *


class Log(object):
    def __init__(self):
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)

    @property
    def date_str(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def debug(self, content, enable_print=True, path=None, filename='main.log'):
        if LOG_DEBUG:
            assert isinstance(content, (str, unicode))
            _path = path if path else LOG_PATH
            if enable_print:
                print '%s [DEBUG] %s' % (self.date_str, content)
            with open(os.path.join(_path, filename), mode='a+') as f:
                f.write('%s [DEBUG] %s%s' % (self.date_str, content, NEW_LINE))

    def info(self, content, enable_print=True, path=None, filename='main.log'):
        assert isinstance(content, (str, unicode))
        _path = path if path else LOG_PATH
        if enable_print:
            print '%s [INFO] %s' % (self.date_str, content)
        with open(os.path.join(_path, filename), mode='a+') as f:
            f.write('%s [INFO] %s%s' % (self.date_str, content, NEW_LINE))

    def error(self, content, enable_print=True, path=None, filename='main.log'):
        assert isinstance(content, (str, unicode))
        _path = path if path else LOG_PATH
        if enable_print:
            print '%s [ERROR] %s' % (self.date_str, content)
        with open(os.path.join(_path, filename), mode='a+') as f:
            f.write('%s [ERROR] %s%s' % (self.date_str, content, NEW_LINE))

    @staticmethod
    def info_record(name, url):
        """a specified method in order to record not-matched info"""
        with open(os.path.join(LOG_PATH, 'not_matched.log'), mode='a+') as f:
            f.write('%s%s%s%s%s' % (name, NEW_LINE, url, NEW_LINE, NEW_LINE))

    def split_line(self, with_tip_center='',
                   enable_print=True, path=None, filename='main.log'):
        _ = '-'*20
        content = '%s%s%s' % (_, with_tip_center, _)
        assert isinstance(content, (str, unicode))
        _path = path if path else LOG_PATH
        if enable_print:
            print '%s %s' % (self.date_str, content)
        with open(os.path.join(_path, filename), mode='a+') as f:
            f.write('%s %s%s' % (self.date_str, content, NEW_LINE))

    @staticmethod
    def write_latest_url(content, cate_eng):
        assert isinstance(content, (str, unicode))
        with open(LOL_LINK_FILE % cate_eng, mode='w+') as f:
            f.write(content)

    @staticmethod
    def read_latest_url(cate_eng):
        try:
            with open(LOL_LINK_FILE % cate_eng) as f:
                res = f.read()
        except IOError as e:
            res = ''
        return res.strip()


if __name__ == '__main__':

    log = Log()
    s = log.read_latest_url()
    print s