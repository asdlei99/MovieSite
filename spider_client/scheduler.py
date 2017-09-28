# coding=utf-8
import datetime
import time
from ms_main import Main

INTERVAL = 60
START_POINT = (10, 14, 18, 22)


def get_hour():
    return int(datetime.datetime.now().strftime('%H'))


def get_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Schedule(object):

    def __init__(self):
        self.last_hour = None  # last run time
        self.first = True   # when run schedule
        self.printed = False
        self.next_hour = get_hour()

    @staticmethod
    def _get_next_hour():
        now_hour = get_hour()
        if max(START_POINT) > now_hour:
            return (now_hour + min([item - now_hour for item in START_POINT
                                    if item > now_hour]))
        else:
            return min(START_POINT)

    def run(self):
        while True:
            hour_now = get_hour()

            if self.next_hour == hour_now:
                self.first = False
                print 'Schedule started at %s' % get_datetime()
                Main().start()
                self.printed = False
                self.next_hour = self._get_next_hour()
                print 'Schedule ended at %s' % get_datetime()
            else:
                if not self.printed:
                    print 'Next schedule will run at %.2d:00' % self.next_hour
                    self.printed = True

                time.sleep(INTERVAL)


if __name__ == '__main__':
    Schedule().run()