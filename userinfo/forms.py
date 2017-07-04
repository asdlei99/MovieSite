#_*_coding:UTF-8_*_

from django import forms

class Login(forms.Form):    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'login_input', 'placeholder':'用户名', 'autofocus':"autofocus", 'spellcheck':"false"}), 
                               max_length=20, 
                               error_messages={'required':'用户名不能为空', 'invalid':'用户名格式错误'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login_input', 'placeholder':'密码'}), 
                               error_messages={'required':'密码不能为空', 'invalid':'密码格式错误'})

class QuickLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control login-field', 
                                                             'id': 'login-name',
                                                             'name': 'login-name',
                                                             'type': 'text',
                                                             'value': '',
                                                             'placeholder': '用户名/邮箱', 
                                                             'autofocus':"autofocus", 
                                                             'spellcheck': "false",
                                                             }), 
                               max_length=30, 
                               error_messages={'required':'用户名不能为空', 'invalid':'用户名格式错误'})
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control login-field', 
                                                             'id': 'login-pass',
                                                             'name': 'login-pass',
                                                             'type': 'text',
                                                             'value': '',
                                                             'placeholder': '密码',
                                                             }), 
                               max_length=30,
                               error_messages={'required':'密码不能为空', 'invalid':'密码格式错误'})

class Register(forms.Form):
    username = forms.CharField(max_length=20, 
                               error_messages={'required':'用户名不能为空', 'invalid':'用户名格式错误'},
                               widget=forms.TextInput(attrs={'class': 'register_input', 'placeholder':'用户名', 'autofocus':'autofocus','spellcheck':"false",'onblur':"Checkuservalid(this)"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'register_input', 'placeholder':'密码', 'onblur':"Checkpwdvalid(this)"}), 
                               error_messages={'required':'密码不能为空', 'invalid':'密码格式错误'})
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'register_input', 'placeholder':'确认密码'}), 
                                       error_messages={'required':'请再次输入密码', 'invalid':'密码格式错误'})
    email = forms.EmailField(error_messages={'required':'邮箱不能为空', 'invalid':'邮箱格式错误'},
                             widget=forms.EmailInput(attrs={'class': 'register_input', 'placeholder':'邮箱','spellcheck':"false"}))
    
    
class ChangePwd(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login_input', 'placeholder':'密码', 'onblur':"Checkpwdvalid(this)"}), 
                               error_messages={'required':'密码不能为空', 'invalid':'密码格式错误'})
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'login_input', 'placeholder':'确认密码'}), 
                                       error_messages={'required':'请再次输入密码', 'invalid':'密码格式错误'}) 

class UserPhoto(forms.Form):
    photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn'}))