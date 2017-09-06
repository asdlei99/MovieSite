# coding=utf-8
import datetime
import time
from ms_main import Main

INTERVAL = 60
START_POINT = (8, 11, 14, 17, 20, 23)


def get_hour():
    return int(datetime.datetime.now().strftime('%H'))

def get_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M%S')

last_point = get_hour()


class Schedule(object):

    def __init__(self):
        self.last_point = get_hour()
        self.first = True

    def run(self):
        while True:
            hour_now = get_hour()

            if (hour_now in START_POINT and hour_now != self.last_point) or self.first:
                if self.first:
                    self.first = False
                print 'Schedule started at %s' % get_datetime()
                Main().start()
                self.last_point = hour_now
                print 'Schedule ended at %s' % get_datetime()
            else:
                try:
                    next_hour = (hour_now +
                                 min([item - hour_now for item in START_POINT if item > hour_now]))
                    print 'Schedule will run at %s' % next_hour
                except ValueError:
                    pass
                time.sleep(INTERVAL)


if __name__ == '__main__':
    Schedule().run()