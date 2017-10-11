# coding=utf-8

from ms_main import Main
import time
import requests

if __name__ == '__main__':

    data = {'secret': '5826f119-c0bc-4ad7-9017-30369eb75b75'}
    print 'Requesting...'
    try:
        time_start = time.time()
        r = requests.post('http://www.bigedianying.com/spider/update_score/',
                          data=data, timeout=1200.0)
        time_end = time.time()
        print 'Response: %s, Cost: %f' % (r.content, time_end - time_start)
    except Exception as e:
        print str(e)
