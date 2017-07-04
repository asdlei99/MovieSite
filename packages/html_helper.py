#_*_coding:UTF-8_*_

from django.utils.safestring import mark_safe
from datetime import datetime, date
import json

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        #如果对象时datetime格式，序列化为所定义格式的字符串
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            #默认序列化（不能格式化datetime格式）
            return json.JSONEncoder.default(self, obj)

class PageInfo:
    def __init__(self, cur_Page, total_Item_Counts, per_Page_Items=10):
        self.cur_page = cur_Page
        self.total_item_counts = total_Item_Counts
        self.per_page_items = per_Page_Items
    
    @property
    def start(self):
        return (self.cur_page - 1)*self.per_page_items
    
    @property
    def end(self):
        return self.cur_page*self.per_page_items
    
    @property
    def total_page_counts(self):
        temp = divmod(self.total_item_counts, self.per_page_items)
        if temp[0] == 0:
            self.total_page_counts = 1
        if temp[1] == 0:
            self.total_page_counts = temp[0]
        else:
            self.total_page_counts = temp[0]+1
        return self.total_page_counts


def Pager(page, page_counts, url):
    '''
    page: 当前页
    page_counts：总页数
    '''
    #生成a标签列表
    page_num_list = []
    #page_num_list.append('<a href="%s/1/">首页</a>' %url)
    
    if page <= 1:
        pre_page = u'<li class="previous"><a href="%s1" class="fui-arrow-left" title="上一页"></a></li>' %(url)
    else:
        pre_page = u'<li class="previous"><a href="%s%d" class="fui-arrow-left" title="上一页"></a></li>' %(url,page-1)
    page_num_list.append(pre_page)
    
    #默认共显示11个页码，当总页数小于11时
    if page_counts < 11:
        begin_page = 1
        end_page = page_counts
    else:
        #总页数大于11时，且当前页小于6时
        if page < 6:
            begin_page = 0
            end_page = 11
        #总页数大于11时，且当前页在倒数后6页中，显示最后11个页码
        elif page >= page_counts - 5:
            begin_page = page_counts - 11
            end_page = page_counts
        else:
            begin_page = page - 6
            end_page = page + 5
    
    if end_page <= 10:
        if page == 1:
            page_num_list.append('<li class="active"><a href="%s1">1</a></li>'%url)
        else:
            page_num_list.append('<li class="hidden-xs hidden-sm"><a href="%s1">1</a></li>'%url)
    for i in range(begin_page, end_page):

        if page == i + 1:
            a_tag = '<li class="active"><a href="%s%d">%d</a></li>' %(url, i+1, i+1)
        else:
            a_tag = '<li class="hidden-xs hidden-sm"><a href="%s%d">%d</a></li>' %(url, i+1, i+1)
        page_num_list.append(a_tag)
        
    if page >= page_counts:
        next_page = u'<li class="next"><a href="%s%d" class="fui-arrow-right" title="下一页"></a></li>' %(url, page)
    else:
        next_page = u'<li class="next"><a href="%s%d" class="fui-arrow-right" title="下一页"></a></li>' %(url, page+1)
    page_num_list.append(next_page)
    #page_num_list.append('<a href="%s/%d/">尾页</a>' %(url, page_counts))
    #将a标签列表的元素用空格连接，并进行安全转义
    page_list = mark_safe(' '.join(page_num_list))
    return page_list

def ajaxScrollPager(page, page_counts, url):
    '''
    page: 当前页
    page_counts：总页数
    '''
    #生成a标签列表
    page_num_list = []
    
        
    if page >= page_counts:
        next_page = u''
    else:
        next_page = u'<a href="%s%d">下一页</a>' %(url, page+1)
    page_num_list.append(next_page)
    #page_num_list.append('<a href="%s/%d/">尾页</a>' %(url, page_counts))
    #将a标签列表的元素用空格连接，并进行安全转义
    page_list = mark_safe(' '.join(page_num_list))
    return page_list