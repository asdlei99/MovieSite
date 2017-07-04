#_*_coding:UTF-8_*_
'''
from django import forms

class Search(forms.Form):    
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'search', 'placeholder':'请输入电影名或类型'}), 
                               max_length=20, 
                               error_messages={'required':'搜索内容不能为空', 'invalid':'内容格式错误'})
   
'''
    