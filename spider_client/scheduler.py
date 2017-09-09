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
        self.last_point = None  # last run time
        self.first = True   # when run schedule
        self.printed = False

    def run(self):
        while True:
            hour_now = get_hour()

            if (hour_now in START_POINT and hour_now != self.last_point) or self.first:
                if self.first:
                    self.first = False
                print 'Schedule started at %s' % get_datetime()
                Main().start()
                self.last_point = hour_now
                self.printed = False
                print 'Schedule ended at %s' % get_datetime()
            else:
                try:
                    next_hour = (hour_now +
                                 min([item - hour_now for item in START_POINT if item > hour_now]))
                    if not self.printed:
                        print 'Schedule will run at %.2d:00' % next_hour
                        self.printed = True
                except ValueError:
                    pass
                time.sleep(INTERVAL)


if __name__ == '__main__':
    Schedule().run()