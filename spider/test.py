# coding=utf-8
from ms_utils.html_helper import TextHandler, Lol
from ms_utils.common import get_html_content

# 获取url
l_content = get_html_content('http://www.loldytt.com/Anime/haizeiwang/',
                             url_log=False)
filename_str, thunder_str, eps_count, seq = Lol().series_get_down_urls(l_content)

print thunder_str
# 解码
# decode_url = TextHandler().decode_url()