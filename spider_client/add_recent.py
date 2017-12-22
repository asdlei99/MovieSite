# coding=utf-8
from __future__ import print_function
from ms_main import Main
import requests
import re


class GetRecentContentError(Exception):
    pass


def get_recent_list():
    rl = requests.get('https://movie.douban.com/coming')
    content = re.findall('(<div id="content">.*?)<div id="footer"', rl.content,
                         re.S)
    if content:
        content = content[0]
        items = re.findall('<td>\s*<a href="(.*?)"', content, re.S)
        return items
    else:
        raise GetRecentContentError


if __name__ == '__main__':
    items = get_recent_list()
    for i in items[:30]:
        print(i)
        Main().add_new_movie(i)
