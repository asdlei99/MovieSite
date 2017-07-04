


var loadingCoverHtml = '<div class="loading-cover"></div>'
$(function() {
	//点击更换验证码
	var $regCodeImg = $('#reg-form .code-wrap img');
	$regCodeImg.click(function () {
		var loadingImg = '/static/images/common/loading/ajax-spinner.gif';
		$(this).html('<img src="'+loadingImg+'">');
		$.ajax({
			url: '/user/change_code/',
			type: 'POST',
			data: {'action':'register'},
			error: function() {
				$(this).html('<span class="label label-default">刷新验证码出错</span>');
			},
			success:function(callback){
				obj = jQuery.parseJSON(callback);
				$regCodeImg.attr('src', obj.code_path);
			}
		});
	});
	
	var $formWrap = $('.form-wrap');
	var errColor = '#e74c3c';
	var iconColor = '#bfc9ca';
	var successColor = '#1abc9c';
	var email_pat = /^[a-zA-Z0-9_-]+\@{1}[a-zA-Z0-9_-]+\.{1}[a-zA-Z0-9]{2,4}$/;
	var space_pat = /\s/;
    var digital_pat = /\d/
    var letter_pat = /[a-zA-Z]/
	var $regForm = $('#reg-form');
	
	var tip_head = '<div class="alert alert-danger alert-dismissible fade in" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button>' 
	var tip_tail = '</div>'
		
	function resetColor(arg) {
		arg.css('border-color', 'transparent');
		arg.parent().find('label').css('color', iconColor);
	}
	function setErrColor(arg) {
		arg.css('border-color', errColor);
		arg.parent().find('label').css('color', errColor);
	}
	function setSuccessColor(arg) {
		arg.css('border-color', successColor);
		arg.parent().find('label').css('color', successColor);
		arg.parent().find('.alert').remove();
	}
	function setWarningColor(arg) {
		arg.css('border-color', warningColor);
		arg.parent().find('label').css('color', warningColor);
	}
	function emailCheck($target) {  //$target为input对象
		$target.blur(function() {
			var emailVal = $target.val();
			var email_result1 = emailVal.length < 6 && emailVal;  //邮箱长度错误
			var email_result2 = !email_pat.test(emailVal) && emailVal;  //邮箱格式错误
			if(email_result1 || email_result2) {
				setErrColor($target);
				var tip = tip_head + '邮箱格式错误，请重新输入' + tip_tail;
				$target.parent().find('.alert').remove();
				$target.parent().append(tip);
			} else {resetColor($target);}
		});
		$target.bind('input propertychange focus', function() {
			var emailVal = $target.val();
			var email_result1 = emailVal.length < 6 && emailVal;  //邮箱长度错误
			var email_result2 = !email_pat.test(emailVal) && emailVal;  //邮箱格式错误
			if(email_result1 || email_result2) {
				setErrColor($target);
			} else {setSuccessColor($target);}
		});
	}
	function passCheck($target) {  //$target为input对象
		$target.blur(function() {
			var passVal = $target.val();
			var pass_result1 = (passVal.length < 8 && passVal) || passVal.length > 32;
			var pass_result2 = (!digital_pat.test(passVal) && passVal) || (!letter_pat.test(passVal) && passVal);
			if(pass_result1 || pass_result2) {
				setErrColor($target);
				var tip = tip_head + '请输入8—32位由数字与字母组合的密码，字母区分大小写' + tip_tail;
				$target.parent().find('.alert').remove();
				$target.parent().append(tip);
			} else {resetColor($target);}
		});
		$target.bind('input propertychange focus', function() {
			var passVal = $target.val();
			var pass_result1 = (passVal.length < 8 && passVal) || passVal.length > 32;
			var pass_result2 = (!digital_pat.test(passVal) && passVal) || (!letter_pat.test(passVal) && passVal);
			if(pass_result1 || pass_result2) {
				setErrColor($target);
			} else {setSuccessColor($target);}
		});
	}
	/*
	function passConfirmCheck($target) {
		$target.blur(function() {
			var passConVal = $target.val();
			var passcon_result1 = (passConVal.length < 8 && passConVal) || passConVal.length > 32;
			var passcon_result2 = (!digital_pat.test(passConVal) && passConVal) || (!letter_pat.test(passConVal) && passConVal);
			if(passcon_result1 || passcon_result2) {
				setErrColor($target);
				var tip = tip_head + '请输入8—32位由数字与字母组合的密码，字母区分大小写' + tip_tail;
				$target.parent().find('.alert').remove();
				$target.parent().append(tip);
			} else {resetColor($target);}
		});
		$target.bind('input propertychange focus', function() {
			var passConVal = $target.val();
			var passcon_result1 = (passConVal.length < 8 && passConVal) || passConVal.length > 32;
			var passcon_result2 = (!digital_pat.test(passConVal) && passConVal) || (!letter_pat.test(passConVal) && passConVal);
			if(passcon_result1 || passcon_result2) {
				setErrColor($target);
			} else {setSuccessColor($target);}
		});
	}*/
	
	
	
	/*
	 * REGISTER
	 */
	if($regForm) {
		var $email = $('#reg-name');
		var $pass = $('#reg-pass');
		var $passConfirm = $('#reg-pass-confirm');
		var $nickname = $('#reg-nickname');
		var $regCode = $('#reg-code-input');
		emailCheck($email);
		passCheck($pass);
		passCheck($passConfirm);

		$nickname.bind('input propertychange focus', function() {
			$nickname.parent().find('.alert').remove();
			setSuccessColor($nickname);
		});
		$nickname.blur(function() {
			$nickname.parent().find('.alert').remove();
			resetColor($nickname);
		});
		$regCode.blur(function() {
			$regCode.parent().find('.alert').remove();
			resetColor($regCode);
		});
		$regCode.bind('input propertychange focus', function() {
			$regCode.parent().find('.alert').remove();
			setSuccessColor($regCode);
		});
		//提交注册
		var $submitBtn = $('#reg-btn');
		$submitBtn.bind('click submit', function(event) {
			var $email = $('#reg-name');
			var $pass = $('#reg-pass');
			var $passConfirm = $('#reg-pass-confirm');
			var $nickname = $('#reg-nickname');
			var $regCode = $('#reg-code-input');
			if(!$email.val()) {
				$email.focus();
				return false;
			}
			if(!$pass.val()) {
				$pass.focus();
				return false;
			}
			if(!$passConfirm.val()) {
				$passConfirm.focus();
				return false;
			}
			if(!$nickname.val()) {
				$nickname.focus();
				return false;
			}
			if(!$regCode.val()) {
				$regCode.focus();
				return false;
			}
			$('.alert').remove();
			$('.form-wrap').prepend(loadingCoverHtml);
			//$submitBtn.attr('disabled',true).text('注册中 ...');
			$submitBtn.text('注册中 ...');
			$.ajax({
				url: '/user/register/submit/',
				type: 'POST',
				data: {'email': $email.val(), 'pass': $pass.val(), 
					'pass_confirm': $passConfirm.val(), 'nickname': $nickname.val(), 'reg_code': $regCode.val()},
				complete: function() {
					//$submitBtn.removeAttr('disabled').text('注册');
					$submitBtn.text('注册');
					$('.form-wrap .loading-cover').remove();
				},
				success: function(callback) {
					var obj = jQuery.parseJSON(callback);
					var msg = obj.msg;
					if(msg) {
						resetColor($('#reg-form input'));
						if(msg=='21' || msg=='22' || msg=='23') {
							$email.focus();
							setErrColor($email);
							if(msg=='21') {
								var content = '请输入邮箱';
							} else if(msg=='22') {
								var content = '邮箱格式错误，请重新输入';
							} else if(msg=='23') {
								var content = '邮箱已被注册，请重新输入';
							}
							tip = tip_head + content + tip_tail;
							$email.parent().append(tip);
						}
						else if(msg=='11' || msg=='12' || msg=='13' || msg=='14' || msg=='15') {
							$pass.focus();
							setErrColor($pass);
							if(msg=='11') {
								var content = '请输入密码';
							} else if(msg=='12' || msg=='13' || msg=='15') {
								var content = '请输入8—32位由数字与字母组合的密码，字母区分大小写';
							} else if(msg=='14') {
								var content = '请输入正确的密码格式，不能包含空格等特殊字符';
							 }
							var tip = tip_head + content + tip_tail;
							$pass.parent().append(tip);
						}
						else if(msg=='17' || msg=='16' || msg=='19' || msg=='1a') {  //confirm_pass
							$passConfirm.focus();
							setErrColor($passConfirm);
							if(msg=='17') {
								var content = '请再次输入密码'
							} else if(msg=='16') {
								var content = '两次密码输入不一致，请重新输入'
							} else if(msg=='19') {
								var content = '请输入正确的密码格式，不能包含空格等特殊字符';
							} else if(msg=='1a') {
								var content = '请输入8—32位由数字与字母组合的密码，字母区分大小写';
							}
							var tip = tip_head + content + tip_tail;
							$passConfirm.parent().append(tip);
						} else if(msg=='32' || msg=='31') {  //验证码
							$regCode.focus();
							$regCode.val('');
							resetColor($regCode);
							if(msg=='31') {
								var content = '请输入验证码';
							} else if(msg=='32') {
								var content = '验证码错误，请重新输入';
							}
							var tip = tip_head + content + tip_tail;
							console.log(tip)
							$regCode.parent().append(tip);
							$regCodeImg.trigger('click');  //刷新验证码
							setErrColor($regCode);
							
						} else if(msg=='43' || msg=='41' || msg=='42') {  //昵称
							$nickname.focus();
							resetColor($('#reg-form input'));
							if(msg=='43') {
								var tip = tip_head + '昵称已存在，请重新输入' + tip_tail;
							} else if(msg=='41') {
								var tip = tip_head + '请输入昵称' + tip_tail;
							} else if(msg=='42') {
								var tip = tip_head + '昵称长度不超过8个汉字或16个英文字符' + tip_tail;
							}
							$nickname.parent().append(tip);
							setErrColor($nickname);
						} else if(msg=='301') {
							var tip = tip_head + '激活邮件发送失败，请重新提交' + tip_tail;
							$email.parent().append(tip);
						} else if(msg=='success') {
							$formWrap.html('<div class="login-form"><p><i class="fa fa-check-circle text-primary"></i> 账号激活确认邮件邮件已发送至你的邮箱，请登录邮箱后根据邮件提示激活账号。</p><p>如有任何问题请联系我们。</p><p>Email：<a href="mailto:bigedianying@gmail.com">bigedianying@gmail.com</a></p><p><a href="/user/login/">登录</a><a href="/" style="float: right;">返回主页</a></p></div>')
						}
					} else {
						var tip = tip_head + '错误'+ msg + tip_tail;
						$email.parent().append(tip);
					}
				}
			});
			event.preventDefault();
		});

	}
	
	
	/*
	 * LOGIN
	 */
	var $loginForm = $('#login-form');
	if($loginForm) {
		var $loginBtn = $('#login-form button');
		var $loginInput = $('#login-form input');
		var $loginEmail = $('#login-form #login-name');
		var $loginPass = $('#login-form #login-pass');

		emailCheck($loginEmail);
		passCheck($loginPass);
		
		$loginBtn.bind('click submit', function(event) {
			var $email = $('#login-name');
			var $pass = $('#login-pass');
			/*if(!$email.val()) {
				$email.focus();
				return false;
			}
			if(!$pass.val()) {
				$pass.focus();
				return false;
			}*/
			$checkbox_status = $loginForm.find('.checkbox input').is(':checked');
			if($checkbox_status) {
				var checked = 'yes';
			}
			$loginBtn.text('登录中 ...');
			$('.form-wrap').prepend(loadingCoverHtml);
			$.ajax({
				type: 'POST',
				url: '/user/login/submit/',
				data: {"email": $email.val(), "password": $pass.val(), 'checkbox': checked},
				complete: function() {
					$loginBtn.text('登录');
					$('.form-wrap .loading-cover').remove();
				},
				success: function(callback) {
					var obj = jQuery.parseJSON(callback);
					console.log(obj)
					if(obj.msg) {
						var msg = obj.msg;
						$('#login-form .alert').removeClass('in').remove();
						resetColor($('#login-name, #login-pass'));
						if(msg=='22' || msg=='21' || msg=='24' || msg=='25' || msg=='26') {
							$email.focus();
							setErrColor($email);
							if(msg=='22') {
								var content = '邮箱格式错误，请重新输入';
							} else if(msg=='21') {
								var content = '请输入邮箱';
							} else if(msg=='24') {
								var content = '账号不存在，请重新输入';
							} else if(msg=='25') {
								var content = '账号尚未激活'
							} else if(msg=='26') {
								var content = '账号已被封，如有疑问请联系管理员'
							}
							tip = tip_head + content + tip_tail;
							$email.parent().append(tip);
						}
						else if(msg=='11' || msg=='12' || msg=='13' || msg=='14' || msg=='15' || msg=='18') {
							$pass.focus();
							setErrColor($pass);
							if(msg=='11') {
								var content = '请输入密码。';
							} else if(msg=='12' || msg=='13' || msg=='15') {
								var content = '请输入8—32位由数字与字母组合的密码，字母区分大小写';
							} else if(msg=='14') {
								var content = '请输入正确的密码格式，不能包含空格等特殊字符。';
							} else if(msg=='18') {
								var content = '密码错误，注意字母区分大小写。';
							}
							var tip = tip_head + content + tip_tail;
							$pass.parent().append(tip);
							
						} else if(msg='success') {
							$.cookie('logined', 'yes', {path:'/'});
							$.cookie('recvpush', 'yes', {path:'/'});
							if(obj.recvpush==0) {
								$.cookie('recvpush', 'no', {path:'/'});
							}
							if(obj.login_from) {
								window.location.href = obj.login_from;
							} else {
								window.location.href = '/';
							}
						}
						
					}
					
				}
			});
		
		event.preventDefault();
		});
	}
	
	//找回密码
	var $forgetPwdCodeImg = $('#forget-pwd-form .code-wrap img');
	$forgetPwdCodeImg.click(function () {
		var loadingImg = '/static/images/common/loading.gif';
		$(this).html('<img src="'+loadingImg+'">');
		$.ajax({
			url: '/user/change_code/',
			type: 'POST',
			data: {'action':'forget_pwd'},
			error: function() {
				$(this).html('<span class="label label-default">刷新验证码出错</span>');
			},
			success:function(callback){
				obj = jQuery.parseJSON(callback);
				$forgetPwdCodeImg.attr('src', obj.code_path);
			}
		});
	});
	

	//提交找回密码
	var $getbackPwdBtn = $('#forget-pwd-form > button');
	var $getbackEmail = $('#forget-pwd-name');
	var $getbackCode = $('#forgetpwd-code-input');
	if($getbackPwdBtn) {
		$getbackPwdBtn.click(function(e) {
			if(!$getbackEmail.val()) {
				$getbackEmail.focus();
				return false;
			}
			if(!$getbackCode.val()) {
				$getbackCode.focus();
				return false;
			}
			$this = $(this);
			$this.text('提交中...');
			$('.form-wrap').prepend(loadingCoverHtml);
			$('#forget-pwd-form .alert').removeClass('in').remove();
			$.ajax({
				url: '/user/forget_pwd/submit/',
				data: {'email':$getbackEmail.val(), 'code':$getbackCode.val()},
				type: 'POST',
				complete: function() {
					$this.text('找回密码');
					$formWrap.find('.loading-cover').fadeOut().remove();
				},
				success: function(callback) {
					var obj = $.parseJSON(callback);
					var msg = obj.msg;
					if(msg) {
						$('.form-wrap').find('.loading-cover').remove();
						$('#forget-pwd-form .alert').removeClass('in').remove();
						if(msg=='21' || msg=='22' || msg=='24') {
							$getbackEmail.focus();
							setErrColor($getbackEmail);
							if(msg=='21') {
								var content = '请输入邮箱';
							} else if(msg=='22') {
								var content = '邮箱格式错误，请重新输入';
							} else if(msg=='24') {
								var content = '账号不存在，请重新输入';
							}
							var tip = tip_head + content + tip_tail;
							$getbackEmail.parent().append(tip);
						} else if(msg=='31' || msg=='32') {
							$getbackCode.focus();
							setErrColor($getbackCode);
							if(msg=='31') {
								var content = '请输入验证码'
							} else if(msg=='32') {
								var content = '验证码错误，请重新输入';
								$forgetPwdCodeImg.trigger('click');
								$getbackCode.val('');
							}
							var tip = tip_head + content + tip_tail;
							$getbackCode.parent().append(tip);
						} else {
							var tip = tip_head + '错误'+msg + tip_tail;
							$getbackEmail.parent().append(tip);
						}
					} else {  //success
						
						$formWrap.html('<div class="login-form"><p><i class="fa fa-check-circle text-primary"></i> 验证邮件已发送至你的邮箱，请登录邮箱后根据邮件提示修改密码。</p><p>如有任何问题请联系我们。</p><p>Email：<a href="mailto:bigedianying@gmail.com">bigedianying@gmail.com</a></p><p><a href="/user/login/">登录</a><a href="/" style="float: right;">返回主页</a></p></div>')
					}
				}
			});
			e.preventDefault();
		});
		emailCheck($getbackEmail);
	}
	
	//重置密码
	$resetPassForm = $('#forget-pwd-change-form');
	if($resetPassForm) {
		var $pass = $('#pass');
		var $passConfirm = $('#pass-confirm');
		passCheck($pass);
		passCheck($passConfirm);
		$('#forget-pwd-change-form > button').bind('click submit', function(event) {
			$formWrap.prepend(loadingCoverHtml);
			$this = $(this);
			$resetPassForm.find('.alert').remove();
			$.ajax({
				url: '/user/forget_pwd/change/',
				data: {'pass':$pass.val(), 'pass_confirm':$passConfirm.val()},
				type: 'POST',
				complete: function() {
					$formWrap.find('.loading-cover').fadeOut().remove();
				},
				success: function(callback) {
					var obj = $.parseJSON(callback);
					console.log(obj);
					var msg = obj.msg
					if(msg) {
						if(msg=='11' || msg=='12' || msg=='13' || msg=='15') {
							if(msg=='11') {
								var content = '请输入密码';
							} if(msg=='14') {
								var content = '请输入正确的密码格式，不能包含空格等特殊字符';
							} else {
								var content = '请输入8—32位由数字与字母组合的密码，字母区分大小写';
							}
							var tip = tip_head + content + tip_tail;
							$pass.parent().append(tip);
							$pass.focus();
							setErrColor($pass);
						} else if(msg=='16' || msg=='17') {
							if(msg=='16') {
								var content = '两次密码输入不一致，请重新输入';
							} else if(msg='17') {
								var content = '请再次输入密码';
							}
							var tip = tip_head + content + tip_tail;
							$passConfirm.parent().append(tip);
							$passConfirm.focus();
							setErrColor($passConfirm);
						} else if(msg=='success') {
							$formWrap.html('<div class="login-form"><p><i class="fa fa-check-circle text-primary"></i> 密码重置成功，请牢记你的密码。</p><p>如有任何问题请联系我们。</p><p>Email：<a href="mailto:bigedianying@gmail.com">bigedianying@gmail.com</a></p><p><a href="/user/login/">登录</a><a href="/" style="float: right;">返回主页</a></p></div>')
						}
					}
					
				}
			});
			event.preventDefault();
		});
	}
});




/*====================django ajax ======*/
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
/*===============================django ajax end===*/
