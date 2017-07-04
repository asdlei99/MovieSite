#_*_coding:UTF-8_*_

from django.utils.safestring import mark_safe

class PageInfo:
    def __init__(self, cur_Page, total_Item_Counts, per_Page_Items=10, first_page_items=10): #first_page_items小于等于10
        self.cur_page = cur_Page
        self.per_page_items = per_Page_Items
        self.first_page_items = first_page_items
        self.differ = per_Page_Items - first_page_items
        self.total_item_counts = total_Item_Counts + self.differ  #加上前面楼层（如一楼）
    @property
    def start(self):
        if self.first_page_items == 10:
            return (self.cur_page - 1)*self.per_page_items
        else:
            if self.cur_page == 1:
                return 0
            else:
                start_page = (self.cur_page - 1)*self.per_page_items - self.differ
                return start_page
    @property
    def end(self):
        if self.first_page_items == 10:
            return self.cur_page*self.per_page_items
        else:
            if self.cur_page == 1:
                return 9
            else:
                end_page = self.cur_page*self.per_page_items - self.differ
                return end_page
    
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


"""
class TvPageInfo:
    def __init__(self, cur_Page, m_Count, items_Per_Page=20):
        self.cur_page = cur_Page
        self.m_count = m_Count
        self.items_per_page = items_Per_Page
        self.m_page = self.m_count / self.items_per_page
        #第m_page页m的数量
        self.m_part = self.m_count % self.items_per_page
    @property
    def start(self):
        if self.cur_page == self.m_page + 1:
            return 0
        if self.cur_page < self.m_page + 1:
            return 0
        else:
            return (self.cur_page-self.m_page-1)*self.items_per_page - self.m_part
    @property
    def end(self):
        if self.cur_page == self.m_page + 1:
            return self.items_per_page - self.m_part
        if self.cur_page < self.m_page + 1:
            return 0
        else:
            return (self.cur_page-self.m_page)*self.items_per_page - self.m_part
"""

def Pager(page, page_counts, url):
    '''
    page: 当前页
    page_counts：总页数
    url: 分页链接
    '''
    #生成a标签列表
    page_num_list = []
    #page_num_list.append(u'<a href="%s1">首页</a>' %url)
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
    #page_num_list.append(u'<a href="%s%d">尾页</a>' %(url, page_counts))
    #将a标签列表的元素用空格连接，并进行安全转义
    page_list = mark_safe(' '.join(page_num_list))

    return page_list



