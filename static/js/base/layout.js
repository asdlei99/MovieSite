/*!
 * jQuery Cookie Plugin v1.4.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2013 Klaus Hartl
 * Released under the MIT license
 */
(function (factory) {
	if (typeof define === 'function' && define.amd) {
		// AMD
		define(['jquery'], factory);
	} else if (typeof exports === 'object') {
		// CommonJS
		factory(require('jquery'));
	} else {
		// Browser globals
		factory(jQuery);
	}
}(function ($) {

	var pluses = /\+/g;

	function encode(s) {
		return config.raw ? s : encodeURIComponent(s);
	}

	function decode(s) {
		return config.raw ? s : decodeURIComponent(s);
	}

	function stringifyCookieValue(value) {
		return encode(config.json ? JSON.stringify(value) : String(value));
	}

	function parseCookieValue(s) {
		if (s.indexOf('"') === 0) {
			// This is a quoted cookie as according to RFC2068, unescape...
			s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
		}

		try {
			// Replace server-side written pluses with spaces.
			// If we can't decode the cookie, ignore it, it's unusable.
			// If we can't parse the cookie, ignore it, it's unusable.
			s = decodeURIComponent(s.replace(pluses, ' '));
			return config.json ? JSON.parse(s) : s;
		} catch(e) {}
	}

	function read(s, converter) {
		var value = config.raw ? s : parseCookieValue(s);
		return $.isFunction(converter) ? converter(value) : value;
	}

	var config = $.cookie = function (key, value, options) {

		// Write

		if (value !== undefined && !$.isFunction(value)) {
			options = $.extend({}, config.defaults, options);

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setTime(+t + days * 864e+5);
			}

			return (document.cookie = [
				encode(key), '=', stringifyCookieValue(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		// Read

		var result = key ? undefined : {};

		// To prevent the for loop in the first place assign an empty array
		// in case there are no cookies at all. Also prevents odd result when
		// calling $.cookie().
		var cookies = document.cookie ? document.cookie.split('; ') : [];

		for (var i = 0, l = cookies.length; i < l; i++) {
			var parts = cookies[i].split('=');
			var name = decode(parts.shift());
			var cookie = parts.join('=');

			if (key && key === name) {
				// If second argument (value) is a function it's a converter...
				result = read(cookie, value);
				break;
			}

			// Prevent storing a cookie that we couldn't decode.
			if (!key && (cookie = read(cookie)) !== undefined) {
				result[name] = cookie;
			}
		}

		return result;
	};

	config.defaults = {};

	$.removeCookie = function (key, options) {
		if ($.cookie(key) === undefined) {
			return false;
		}

		// Must not alter options, thus extending a fresh object...
		$.cookie(key, '', $.extend({}, options, { expires: -1 }));
		return !$.cookie(key);
	};

}));
//hover-dropdown
!function(e,n){var o=e();e.fn.dropdownHover=function(t){return"ontouchstart"in document?this:(o=o.add(this.parent()),this.each(function(){function r(){d.parents(".navbar").find(".navbar-toggle").is(":visible")||(n.clearTimeout(a),n.clearTimeout(i),i=n.setTimeout(function(){o.find(":focus").blur(),v.instantlyCloseOthers===!0&&o.removeClass("open"),n.clearTimeout(i),d.attr("aria-expanded","true"),s.addClass("open"),d.trigger(h)},v.hoverDelay))}var a,i,d=e(this),s=d.parent(),u={delay:200,hoverDelay:0,instantlyCloseOthers:!0},l={delay:e(this).data("delay"),hoverDelay:e(this).data("hover-delay"),instantlyCloseOthers:e(this).data("close-others")},h="show.bs.dropdown",c="hide.bs.dropdown",v=e.extend(!0,{},u,t,l);s.hover(function(e){return s.hasClass("open")||d.is(e.target)?void r(e):!0},function(){n.clearTimeout(i),a=n.setTimeout(function(){d.attr("aria-expanded","false"),s.removeClass("open"),d.trigger(c)},v.delay)}),d.hover(function(e){return s.hasClass("open")||s.is(e.target)?void r(e):!0}),s.find(".dropdown-submenu").each(function(){var o,t=e(this);t.hover(function(){n.clearTimeout(o),t.children(".dropdown-menu").show(),t.siblings().children(".dropdown-menu").hide()},function(){var e=t.children(".dropdown-menu");o=n.setTimeout(function(){e.hide()},v.delay)})})}))},e(document).ready(function(){e('[data-hover="dropdown"]').dropdownHover()})}(jQuery,window);

/*
 * COMMON FUNCTION
 */
var loadingCoverHtml = '<div class="loading-cover"></div>';
var loadingCoverHtmlInverse = '<div class="loading-cover loading-cover-inverse"></div>';
//改变评论框状态 
var focusColor = '#1abc9c';
var orgColor = '#bdc3c7';
function ChangePubColor(obj,act) {
	console.log(obj)
	if(act=='focus') {
		obj.css({'border-left-color':focusColor, 'border-bottom-color':focusColor, 'border-right-color':focusColor});
	} else if(act=='blur') {
		obj.css({'border-left-color':orgColor, 'border-bottom-color':orgColor, 'border-right-color':orgColor});
	}
}
function ChangeTextareaState($box, threshold) {
	var $textarea = $box.find('.text-wrapper');
	var $submitBtnGrp = $box.find('.submit-btn-group');
	$emotion = $box.find('.emotion-icon-rr');
	if(!$emotion.length) {
		$emotion = $box.find('.emotion-icon');
	}
	$emotion.SinaEmotion($textarea); //绑定表情
	$textarea.focus(function() {
		console.log('focus')
		console.log($submitBtnGrp.length)
		ChangePubColor($submitBtnGrp, 'focus');
	});
	$textarea.blur(function() {
		ChangePubColor($submitBtnGrp, 'blur')
	});
	$submitBtnGrp.click(function() {
		$textarea.focus();
		ChangePubColor($submitBtnGrp, 'focus');
	});
	/*$submitBtnGrp.blur(function() {
		ChangePubColor($submitBtnGrp,'blur');
	});*/
	$textarea.maxlength({
	    //alwaysShow: true,
	    threshold: threshold,
	    warningClass: "label label-warning",
	    limitReachedClass: "label label-danger",
	    separator: ' / ',
	    preText: ' ',
	    postText: ' ',
	    validate: true
	});
}
//加载tips
function showTip(content, type, $wrap) {
	if(type == 'success') {
		var tipHead = '<div class="alert alert-success" style="position:absolute;z-index:2000;padding:10px 20px">';
	} else if(type == 'warning') {
		var tipHead = '<div class="alert alert-warning" style="position:absolute;z-index:2000;padding:10px 20px">';
	} else if(type == 'danger') {
		var tipHead = '<div class="alert alert-danger" style="position:absolute;z-index:2000";padding:10px 20px>';
	}
	var tipTail = '</div>'
	var tip = tipHead + content + tipTail;
	$wrap.prepend(tip);
	$alert = $wrap.find('.alert');
	var targetTop = $wrap.innerHeight() / 2 - $alert.innerHeight() / 2;
	var targetLeft = $wrap.innerWidth() /2 - $alert.innerWidth() / 2;
	$alert.css({'top': targetTop, 'left': targetLeft});

	var timerRunning = true;
	if(!timer || typeof(timer)=='undefined') {
		var timer = window.setTimeout(temp,1000);
	}
	function temp() {
		timer = null;
		$wrap.find('.alert').fadeOut(function() {
			$wrap.find('.alert').remove();
		});
	}
}
//登录检查
function checkLogin() {
	$logined_cookie = $.cookie('logined');
	if(!$logined_cookie) {  //cookie不存在
		$.ajax({
			url: '/user/reply_check_login/',
			type: 'POST',
			success: function(callback) {
				obj = $.parseJSON(callback);
				if(!obj.logined) {
					$('#loginModal').modal();
					$.cookie('logined', 'no', {path:'/'});
					return false;
				} else {
					$.cookie('logined', 'yes', {path:'/'});
					return true;
				}
			}
		});
		return false;
	}  else {
		if($logined_cookie == 'no') {
			$('.modal').modal('hide');
			$('#loginModal').modal();
			return false;
		} else {
			return true;
		}
	}
}
//空字符检查
function checkReplyContent($text) {
	var result = /^\s+$/.test($text.val());
	if(!$text.val()) {
		var tip = '请输入内容';
	} else if(result) {
		var tip = '内容不能全部为空格';
	} else {
		tip = null;
	}
	return tip;
}
//动态加载提交内容时替换换行为<br>
function replaceWithBr(text) {
	try {  
		text = text.replace(/\r\n/g,"<br>");
		text = text.replace(/\n/g,"<br>");  
	} catch(e) {}  
	return text;
}
//fadeout
function itemFadeOut($wrap, target) {
	//target is a style like '.style'
	if(target == 'item_self') {
		$wrap.fadeOut('slow');
		window.setTimeout(function() {
			$wrap.remove();
		},1000);
	} else {
		$wrap.find(target).fadeOut('slow');
		window.setTimeout(function() {
			$wrap.find(target).remove();
		},1000);
	}
}
function itemSlideUp($wrap, target) {
	//target is a style like '.style'
	if(target == 'item_self') {
		$wrap.slideUp();
		window.setTimeout(function() {
			$wrap.remove();
		},1000);
	} else {
		$wrap.find(target).slideUp();
		window.setTimeout(function() {
			$wrap.find(target).remove();
		},1000);
	}
}

/*
 * 搜索相关
 *
 */
$(function() {
	//直接点击nav菜单
	$('#nav-menu-notice>a').click(function() {
		window.location.href="/user/home/notification/";
	});
	$('#navUserPhoto').click(function() {
		window.location.href="/user/home/";
	});
	
	//拼接url进行搜索
	var $navSearchInput = $('nav #search-input');
	var $navSearchInputGrp = $('nav #search-form .input-group');
	var $seWrap = $('nav .search-wrap')
	//input单击事件
	$navSearchInput.click(function(event) {
		if(!$navSearchInputGrp.is(':animated') && $navSearchInputGrp.width() < 200) { //非动画且input宽度小于200
			$navSearchInputGrp.animate({width: '350'}, 400);
			$('nav ul li.dropdown').removeClass('open');  //关闭下拉菜单（若有打开项）
		}
		$seWrap.css({'width': '329',}); //设置搜索结果框宽度
		event.stopPropagation();
		if(!$seWrap.is(':visible')) {
			if($seWrap.children().length) { //不可见但wrap有内容，显示
				$seWrap.slideDown(100);
			}
		}
	});

	
	//body单击事件
	$('html').click(function(event) {
		if(!$navSearchInputGrp.is(':animated') && $navSearchInputGrp.width() > 200) {
			$navSearchInputGrp.animate({width: '195'}, 400);  //缩小input
			$seWrap.hide(400);  //隐藏搜索框
		}

	});
	


	var $searchBtn = $('#search-input button');
	var $searchInput = $('#search-input');
	var $searchFormGroup = $('#search-form .form-group');
	//点击按钮，，拼接url并跳转
	$searchBtn.click(function() {
		$q = $searchInput.val();
		if($q) {
			var url = '/search/result/?category=all&focus=af&type=at&region=ar&keyword=' + $q;
			window.location.href = url;
		} else {
			var url = '/search/';
			window.location.href = url;
		}
		return false;
	});
	//表单提交，拼接url并跳转
	$('#search-form').submit(function() {
		$q = $searchInput.val();
		if($q) {
			var url = '/search/result/?category=all&focus=af&type=at&region=ar&keyword=' + $q;
			window.location.href = url;
		} else {
			var url = '/search/';
			window.location.href = url;
		}
		return false;
	});
	
	/*
	 * 首次进入页面
	 *
	 */


	/*
	 * 当input的value改变，提交ajax请求
	 */
	$.cookie('lastSearchValue', '');
	$searchInput.bind('input propertychange', function() {
		window.searchVal = $.trim($searchInput.val());	//发生input值变更时读取其value(去掉两边空格)
		//console.log('当前值：'+searchVal);
		//console.log('cookie：'+$.cookie('lastSearchValue'))
		//在input改变后到ajax成功期间，暂时解绑body的click，防止input缩小(如果会发生ajax)
		if(searchVal && searchVal != $.cookie('lastSearchValue')) {
			$('body').unbind('click');  
		}
		if(!searchVal && $.cookie('lastSearchValue')) {  //input被用户清空，不会发送请求
			$seWrap.fadeOut(100).empty();  
			$.cookie('lastSearchValue', '');	//隐藏wrap并清空，记录cookie
			try {clearTimeout(search_timer)} catch(e) {}
			return false;
		}
		if(searchVal && searchVal != $.cookie('lastSearchValue')) { //value非空 且 value和cookie不等
			if(($navSearchInputGrp).hasClass('focus') && $navSearchInputGrp.width() < 200) {  //若只是鼠标选择了文字，input并未拉宽
				$navSearchInputGrp.animate({width: '350'}, 400);
			}
			try {clearTimeout(search_timer)} catch(e) {}
			window.search_timer = window.setTimeout(function() {  //延迟时间后执行ajax
			$.ajax({
				url:'/search/value_change/',
				data:{sv: searchVal},	//发送当前value
				type:'POST',
				complete:function() {
					$.cookie('lastSearchValue', searchVal); //searchVal记录到cookie中
				},
				success:function(callback){
					var obj = jQuery.parseJSON(callback);
					$seWrap.empty();
					if(obj.illegal) {  //若返回为非法
						$seWrap.hide();
					} else {  //若合法
						$.each(obj, function(k,v) {
							console.log(v.eps)
							if(v.eps) {
								if(v.eps==999) {var epsHtml = '<div class="foreign-name">集数未知</div>';} else {var epsHtml = '<div class="foreign-name">共' + v.eps + '集</div>';}
							} else { epsHtml = ''}
							if(v.foreign_name) {var fnHtml = '<div class="foreign-name">' + v.foreign_name + '</div>';} else {var fnHtml = '';}
							var searchItem = '<a class="search-item" href="' + v.url + 
							'"><div class="col-lg-2 col-md-2"><img src="' + v.poster +
							'"></div><div class="col-lg-10 col-md-10"><div class="movie-name">' + v.ch_name + '<span>' + 
							v.year + '</span></div>' + fnHtml + epsHtml + '</div></a>';
                        $seWrap.append(searchItem).css({'width': '329',}).slideDown(100);
						});
					}
					$('html').click(function() {  //执行完毕ajax后重新绑定bodyclick
						if(!$navSearchInputGrp.is(':animated') && $navSearchInputGrp.width() > 200) {
							$navSearchInputGrp.animate({width: '195'}, 400);
							$seWrap.hide(100);
						}
					});
				}
				
			});}, 400);
		}
		
	});
	
	
	//goup
	$(document).ready(function () {
        $.goup({
            bottomOffset: 80,
            locationOffset: 20,
            trigger: 600,
            entryAnimation: 'slide',
        });

    });

});



/*
 * 导航登录
 */

$(function() {
	$('#navLogin').click(function() {
		setTimeout(function() {
			$('#menuLogin').find('#quick-login-name').focus();
		},10);
		
	});
	//navbar quick login
	var $loginBtn = $('#quick-login-form button');
	var $loginInput = $('#quick-login-form input');
	var $loginForm = $('#quick-login-form');
	var $loginEmail = $('#quick-login-form #quick-login-name');
	var $loginPass = $('nav #quick-login-form #quick-login-pass');
	var activeColor = '#1abc9c';
	var iconColor = '#bfc9ca';
	var warningColor = '#e74c3c';
	var oneLine = '-3px';
	var twoLine = '-12px';
	var mailReg = /^\s*[a-zA-Z0-9_-]+\@{1}[a-zA-Z0-9_-]+\.{1}[a-zA-Z0-9]{2,4}\s*$/;
	var reg1 = /[a-zA-Z]{1,}/;  
	var reg2 = /[0-9]{1,}/;
	
	$loginInput.bind('input propertychange focus', function() {
		/*
		 * 每次触发事件时，进行email和password检查
		 * 0表示正确，1表示长度不对，2表示格式不对
		 */
		var email = $loginEmail.val();
		var pass = $loginPass.val();
		var emailState = 0;
		var passState = 0;
		if(!mailReg.test(email) && email) {emailState = 2;}
		
		if(pass.length>=8) {
			if(!reg1.test(pass) || !reg2.test(pass)) { 
				passState = 2;
			} 
		}
		else {
			if(pass.length==0) {passState = 0;} else {passState = 1;}
			
		}

		//事件发生于email input
		if($(this).attr('id')=='quick-login-name') {
			var $emailTip = $(this).next();
			var $emailIcon = $(this).parent().find('label');
			if(!emailState==0) {
				$loginEmail.css('border-color', warningColor);
				$emailIcon.css('color', warningColor);
				$emailTip.removeClass('hide');
				
				//$loginBtn.attr('disabled',true);
				
				if(emailState==2) {  //邮箱格式错误
					$emailTip.find('.tooltip-inner').text('邮箱格式不正确');
					$emailTip.css({'left': -153, 'top': oneLine});
				}
			}
			
			else {  //邮箱正确
				$loginEmail.css('border-color', activeColor);
				$emailIcon.css('color', activeColor);
				$emailTip.addClass('hide');
				if(passState==0) {
					//$loginBtn.removeAttr('disabled');
				}
			}
		}
		
		else if($(this).attr('id')=='quick-login-pass'){
			var $passTip = $(this).parent().find('.tooltip');
			var $passIcon = $(this).parent().find('label');
			if(!passState==0) {
				$loginPass.css('border-color', warningColor);
				$passIcon.css('color', warningColor);
				$passTip.removeClass('hide');
				//$loginBtn.attr('disabled',true);
				
				if(passState==1) {  //密码长度错误
					$passTip.find('.tooltip-inner').text('密码长度最少为8位');
					$passTip.css({'left': -175, 'top': oneLine});
				} else if(passState==2) {  //密码格式错误
					$passTip.find('.tooltip-inner').text('密码至少含有一位字母和数字');
					$passTip.css({'left': -214, 'top': twoLine});
				}
			}
			
			else {  //密码正确
				$loginPass.css('border-color', activeColor);
				$passIcon.css('color', activeColor);
				$passTip.addClass('hide');
				if(emailState==0) {
					//$loginBtn.removeAttr('disabled');
				}
			}
		}
		
	});
		
	
	$loginInput.blur(function() {
		var email = $loginEmail.val();
		var pass = $loginPass.val();
		var emailState = 0;
		var passState = 0;
		if(email.length>22 || email.length<6) {
			if(email.length==0) {emailState=0;} else {emailState = 1;}
		} else {
			if(!mailReg.test(email)) {emailState = 2;}
		}
		if(pass.length>=8) {
			if(!reg1.test(pass) || !reg2.test(pass)) { 
				passState = 2;
			} 
		}
		else {
			if(pass.length==0) {passState = 0;} else {passState = 1;}
			
		}
		
		if($(this).attr('id')=='quick-login-name') {
			var $emailTip = $(this).next();
			var $emailIcon = $(this).parent().find('label');
			if(emailState==0) {
				$(this).css('border-color', 'transparent');
				$emailIcon.css('color', iconColor);
				$emailTip.addClass('hide');
			}

		}
		else if($(this).attr('id')=='quick-login-pass'){
			var $passTip = $(this).next();
			var $passIcon = $(this).parent().find('label');
			if(passState==0) {
				$(this).css('border-color', 'transparent');
				$passIcon.css('color', iconColor);
				$passTip.addClass('hide');
			}
		}
		
	});
	
	$loginBtn.bind('click submit', function(event) {
		var $user = $('#quick-login-name');
		var $pass = $('#quick-login-pass');
		/*if(!$user.val()) {
			$user.focus();
			return false;
		}
		if(!$pass.val()) {
			$pass.focus();
			return false;
		}*/
		var $checkbox_status = $loginForm.find('.checkbox input').is(':checked');
		if($checkbox_status) {
			var checked = 'yes';
		}
		//$loginBtn.attr('disabled',true).text('登录中 ...');
		$box = $('#menuLogin>.navbar-form');
		$box.append(loadingCoverHtmlInverse);
		$.ajax({
			type: 'POST',
			url: '/user/quicklogin/',
			data: {'username': $user.val(), 'password': $pass.val(), 'checkbox':checked},
			success: function(callback) {
				var obj = jQuery.parseJSON(callback);
				var msg = obj.msg
				//$loginBtn.removeAttr('disabled').text('登录');
				if(msg) {
					$user.focus();  //首先让input获得焦点
					var $userTip = $user.next();
					var $userIcon = $user.parent().find('label');
					$userTip.removeClass('hide');
					$user.css('border-color', warningColor);
					$userIcon.css('color', warningColor);
					if(msg=='22') {
						$user.next().find('.tooltip-inner').text('邮箱格式不正确');
						$user.next().css({'left': -140, 'top': oneLine});
					} else if(msg=='21') {
						$user.next().find('.tooltip-inner').text('请输入邮箱');
						$user.next().css({'left': -125, 'top': oneLine});
					} else if(msg=='24') {
						$user.next().find('.tooltip-inner').text('账号不存在');
						$user.next().css({'left': -125, 'top': oneLine});
					}  else if(msg=='25') {
						$user.next().find('.tooltip-inner').text('账号尚未激活');
						$user.next().css({'left': -140, 'top': oneLine});
					} else if(msg=='26') {
						$user.next().find('.tooltip-inner').text('账号已被封，如有疑问请联系管理员');
						$user.next().css({'left': -215, 'top': twoLine});
					}else if(msg=='101') {
						$user.next().find('.tooltip-inner').text('错误101，请联系管理员');
						$user.next().css({'left': -205, 'top': oneLine});
					} else if(msg=='102') {
						$user.next().find('.tooltip-inner').text('错误102，请联系管理员');
						$user.next().css({'left': -205, 'top': oneLine});
					} else if(msg=='103') {
						$user.next().find('.tooltip-inner').text('错误103，请联系管理员');
						$user.next().css({'left': -205, 'top': oneLine});
					}
					
					else {  //密码栏提示错误
						$pass.focus();
						if($pass.next().hasClass('hide')) {
							$pass.next().removeClass('hide');
						}
						if(msg=='12' || msg=='13' || msg=='15') {
							$pass.next().find('.tooltip-inner').text('请输入8—32位由数字与字母组合的密码');
							$pass.next().css({'left': -215, 'top': twoLine});
						} else if(msg=='14') {
							$pass.next().find('.tooltip-inner').text('密码不能包含空格等特殊字符');
							$pass.next().css({'left': -215, 'top': twoLine});
						} else if(msg=='11') {
							$pass.next().find('.tooltip-inner').text('请输入密码');
							$pass.next().css({'left': -125, 'top': oneLine});
						} else if(msg=='18') {
							$pass.next().find('.tooltip-inner').text('密码错误，注意字母区分大小写');
							$pass.next().css({'left': -215, 'top': twoLine});
						}
						$pass.css('border-color', warningColor);
						$pass.parent().find('label').css('color', warningColor);
					}

					
				}
				if(obj.logined) {
					console.log('^_^');
					$loginPass.css('border-color', 'transparent');
					$loginPass.parent().find('label').css('color', iconColor);
					$loginPass.tooltip('destroy');
					$.cookie('logined','yes', {path:'/'});
					$.cookie('recvpush', 'yes', {path:'/'});
					if(obj.recvpush==0) {
						$.cookie('recvpush', 'no', {path:'/'});
					}
					window.location.reload();
				} else {
					itemFadeOut($box, '.loading-cover');
				}
					
			}
		});
		event.preventDefault();
		event.stopPropagation();
		
	});
	
	//nav退出登录
	$('#nav-logout-btn').click(function() {
		$.cookie('logined', 'no', {path:'/'});
		$.cookie('recvpush', 'yes', {path:'/'});
	});
	
	
	//modal login
	$loginModalForm = $('#modal-login-form');
	$loginModalContent = $('#loginModal .modal-content');
	$loginModalBtn = $('#modal-login-form>button');
	$loginModalName = $('#modal-login-name');
	$loginModalPass = $('#modal-login-pass');
	$loginModalCheckStatus = $('#modal-login-form .custom-checkbox').is(':checked');
	$('#loginModal').on('shown.bs.modal', function () {
		$loginModalName.focus()
	});
	$loginModalBtn.bind('click', function(event) {
		$_this = $(this);
		$_this.text('登录中...');
		$loginModalForm.find('.alert').remove();
		$loginModalContent.prepend(loadingCoverHtml);
		$.ajax({
			url: '/user/quicklogin/',
			data: {'username':$loginModalName.val(), 'password':$loginModalPass.val(), 'checkbox':$loginModalCheckStatus},
			type: 'POST',
			success: function(callback) {
				$loginModalContent.find('.loading-cover').remove();
				$_this.text('登录');
				var obj = $.parseJSON(callback);
				var tip_head = '<div class="alert alert-danger alert-dismissible fade in" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">×</span></button>' 
				var tip_tail = '</div>'
				var msg = obj.msg;
				if(msg) {
					if(msg=='11'||msg=='14'||msg=='21') {
						content = '用户名或密码不能为空';
					} else if(msg=='12'||msg=='13'||msg=='18'||msg=='14'||msg=='15'||msg=='22'||msg=='24') {
						content = '用户名或密码错误';
					} else if(msg=='25') {
						content = '账号尚未激活';
					} else if(msg=='25') {
						content = '账号已被封，如有疑问请联系管理员';
					} else if(msg=='success') {
						$.cookie('logined', 'yes', {path:'/'});
						$.cookie('recvpush', 'yes', {path:'/'});
						window.location.reload();	
					}
					var tip = tip_head + content + tip_tail;
					$loginModalForm.find('#modal-login-pass').parent().append(tip);
				} else {
					
				}
			},
		});
		event.preventDefault();
	});
	
	
	
	//polling

	if($('#nav-menu-notice').length) {
		
		window.lastMsgCounts = 0;
		window.lastReplyCounts = 0;
		window.lastFocusCounts = 0;
		window.lastMRLikeCounts = 0;
		window.setInterval(function() {
			if($.cookie('recvpush')=='no') {
				return false;
			}
			if($.cookie('logined') == 'yes') {
				$.ajax({
					url: '/user/polling/',
					type: 'POST',
					success: function(callback) {
						var obj = $.parseJSON(callback);
						var $navUnread = $('#nav-menu-notice .navbar-unread');
						var $navNew = $('#nav-menu-notice .navbar-new');
						var $menuWrap = $('#nav-menu-notice > ul');
						if(obj.new_msg||obj.movie_rr||obj.movie_r_like||obj.bbs_r||obj.focus) {
							$('#notice-default').remove();
							if(obj.new_msg && !lastMsgCounts==obj.new_msg) {
								$('#notice-msg').remove();
								var subMenuHtml = '<li id="notice-msg"><a href="/user/home/messages/" style="padding-right:30px" role="button">' + '<i class="fa fa-envelope-o fa-fw"></i> 收到了新私信 <span class="navbar-new">' + obj.new_msg + '</span>' + '</a></li>';
								$menuWrap.prepend(subMenuHtml);
								window.lastMsgCounts = obj.new_msg;
							}
							if(obj.focus && !(lastFocusCounts==obj.focus)) {
								$('#notice-focus').remove();
								var subMenuHtml = '<li id="notice-focus"><a href="/user/home/notification/" style="padding-right:30px" role="button">' + '<i class="fa fa-heart-o fa-fw"></i> 收获了新粉丝 <span class="navbar-new">' + obj.focus + '</span>' + '</a></li>';
								$menuWrap.append(subMenuHtml);
								window.lastFocusCounts = obj.focus;
							}
							
							var totalReplys = parseInt(obj.bbs_r) + parseInt(obj.movie_rr);
							if(totalReplys && !(lastReplyCounts==totalReplys)) {
								$('#notice-bbs-r').remove();
								var total = parseInt(obj.bbs_r) + parseInt(obj.movie_rr);
								var subMenuHtml = '<li id="notice-bbs-r"><a href="/user/home/notification/" style="padding-right:30px" role="button">' + '<i class="fa fa-comment-o fa-fw"></i> 有人回复了你 <span class="navbar-new">' + totalReplys + '</span>' + '</a></li>';
								$menuWrap.prepend(subMenuHtml);
								window.lastReplyCounts = totalReplys;
							}
							if(obj.movie_r_like && !lastMRLikeCounts==obj.movie_r_like) {
								$('#notice-movie-r-like').remove();
								var subMenuHtml = '<li id="notice-movie-r-like"><a href="/user/home/notification/" style="padding-right:30px" role="button">' + '<i class="fa fa-thumbs-o-up fa-fw"></i> 有人赞了你 <span class="navbar-new">' + obj.focus + '</span>' + '</a></li>';
								$menuWrap.prepend(subMenuHtml);
								window.lastMRLikeCounts = obj.movie_r_like;
							}
							$navUnread.removeClass('hidden');
						} else {
							if(obj.msg) {
								var msg = obj.msg;
								if(msg=='402') {
									$.cookie('recvpush', 'no', {path:'/'});
								}
							}
							$navUnread.addClass('hidden');
							if(!$('#notice-default').length) {
								$menuWrap.empty();
								$menuWrap.append('<li id="notice-default"><a style="cursor:default">暂时没有新消息哦~</a></li>')
							}
						}
						
						
					}
				});
			}
		}, '3000');
	}
	

});



//顶部进度条
$(function() {
  NProgress.start();
  $(window).load(function() {
	  NProgress.done();
	});	
});

$(function() {
	$('nav#menu').mmenu({
		extensions	: [ 'effect-slide-menu', 'pageshadow', 'theme-dark' ,'pagedim-black'],
		navbar 		: {
			title		: '比格电影'
		},
		navbars		: [
			 {
				position	: 'top',
				content		: [
					'prev',
					'title',
					'close'
				]
			}, {
				position	: 'bottom',
				content		: [
		                        '<a class="fa fa-gear" href="/user/home/settings/"></a>',
		                        '<a class="fa fa-envelope" href="/user/home/messages/"></a>',
		                        '<a class="fa fa-search" href="/search/"></a>'
		                     ]
			}
		]
	});
});



/*
var myHeader = document.querySelector("#main-nav");
// 创建 Headroom 对象，将页面元素传递进去
var headroom  = new Headroom(myHeader,{
	  tolerance: 5,
	  //offset: 205,
	  offset: 0,
	  "classes": {
		    "initial": "animated",
		    "pinned": "slideDown",
		    "unpinned": "slideUp"
		  }
});
// 初始化
headroom.init(); 
*/





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

/*
*
* Copyright (c) 2014-2016 Daniele Lenares (https://github.com/Ryuk87)
* Dual licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
* and GPL (http://www.opensource.org/licenses/gpl-license.php) licenses.
*
* Version 1.1.0
*
*/
!function(t){"use strict";function e(t,e,i){if("show"==e)switch(i){case"fade":t.fadeIn();break;case"slide":t.slideDown();break;default:t.fadeIn()}else switch(i){case"fade":t.fadeOut();break;case"slide":t.slideUp();break;default:t.fadeOut()}}function i(e,i){var o=!0;e.on("click",function(){1==o&&(o=!1,t("html, body").animate({scrollTop:0},i,function(){o=!0}))})}t.goup=function(o){var n=t.extend({location:"right",locationOffset:20,bottomOffset:10,containerSize:40,containerRadius:10,containerClass:"goup-container",arrowClass:"goup-arrow",alwaysVisible:!1,trigger:200,entryAnimation:"fade",goupSpeed:"normal",hideUnderWidth:500,containerColor:"#1abc9c",arrowColor:"#fff",title:"回到顶部",titleAsText:!1,titleAsTextClass:"goup-text",zIndex:1},o);"right"!=n.location&&"left"!=n.location&&(n.location="right"),n.locationOffset<0&&(n.locationOffset=0),n.bottomOffset<0&&(n.bottomOffset=0),n.containerSize<20&&(n.containerSize=20),n.containerRadius<0&&(n.containerRadius=0),n.trigger<0&&(n.trigger=0),n.hideUnderWidth<0&&(n.hideUnderWidth=0);var r=/(^#[0-9A-F]{6}$)|(^#[0-9A-F]{3}$)/i;r.test(n.containerColor)||(n.containerColor="#000"),r.test(n.arrowColor)||(n.arrowColor="#fff"),""===n.title&&(n.titleAsText=!1),isNaN(n.zIndex)&&(n.zIndex=1);var a=t("body"),s=t(window),d=t("<div>");d.addClass(n.containerClass);var l=t("<div>");l.addClass(n.arrowClass),d.html(l),a.append(d);var c={position:"fixed",width:n.containerSize,height:n.containerSize,background:n.containerColor,cursor:"pointer",display:"none","z-index":n.zIndex};if(c.bottom=n.bottomOffset,c[n.location]=n.locationOffset,c["border-radius"]=n.containerRadius,d.css(c),n.titleAsText){var f=t("<div>");a.append(f),f.addClass(n.titleAsTextClass).text(n.title),f.attr("style",d.attr("style")),f.css("background","transparent").css("width",n.containerSize+40).css("height","auto").css("text-align","center").css(n.location,n.locationOffset-20);var h=parseInt(f.height())+10,p=parseInt(d.css("bottom")),u=h+p;d.css("bottom",u)}else d.attr("title",n.title);var g=.25*n.containerSize,y={width:0,height:0,margin:"0 auto","padding-top":Math.ceil(.325*n.containerSize),"border-style":"solid","border-width":"0 "+g+"px "+g+"px "+g+"px","border-color":"transparent transparent "+n.arrowColor+" transparent"};l.css(y);var w=!1;s.resize(function(){s.outerWidth()<=n.hideUnderWidth?(w=!0,e(d,"hide",n.entryAnimation),"undefined"!=typeof f&&e(f,"hide",n.entryAnimation)):(w=!1,s.trigger("scroll"))}),s.outerWidth()<=n.hideUnderWidth&&(w=!0,d.hide(),"undefined"!=typeof f&&f.hide()),n.alwaysVisible?(e(d,"show",n.entryAnimation),"undefined"!=typeof f&&e(f,"show",n.entryAnimation)):s.scroll(function(){s.scrollTop()>=n.trigger&&!w&&(e(d,"show",n.entryAnimation),"undefined"!=typeof f&&e(f,"show",n.entryAnimation)),s.scrollTop()<n.trigger&&!w&&(e(d,"hide",n.entryAnimation),"undefined"!=typeof f&&e(f,"hide",n.entryAnimation))}),s.scrollTop()>=n.trigger&&!w&&(e(d,"show",n.entryAnimation),"undefined"!=typeof f&&e(f,"show",n.entryAnimation)),i(d,n.goupSpeed),"undefined"!=typeof f&&i(f,n.goupSpeed)}}(jQuery);
