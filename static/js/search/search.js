/**
 * 
 */

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



$(function() {
	var $submitBtn = $('.form-group button');
	var $searchInput = $('#search-index-input');
	var $formGroup = $('.form-group');
	var $seWrap = $('#search-wrap');
	var $seWrapRec = $('#search-wrap-recommend');
	var $well = $('.well');
	//初始化窗口高度
	var screenHeight = parseInt($(window).height() - 40);
	$('.container').css('height',screenHeight);
	/*
	 * 首次进入页面
	 *刷新页面自动focus
	 *
	 *$formGroup.addClass('focus');
	 */
	
	//点击除input外的部分，去掉focus样式
	$('html').click(function() {
		if($formGroup.hasClass('focus')) {
			$formGroup.removeClass('focus');
		}
		 //input-group没有focus样式
		if($seWrap.is(':visible')) {
			$seWrap.slideUp(100);

		} else if($seWrapRec.is(':visible')) {
			$seWrapRec.hide();

		}

	});
	//给input绑定click事件
	$searchInput.click(function(event) {
		if(!$seWrap.is(':visible')) {
			if($seWrap.children().length) { //不可见但wrap有内容
				$seWrap.slideDown(100);
			}
			else { //不可见且无内容，显示默认推荐
				$($seWrapRec).show();
				
			}
		}
		
		event.stopPropagation();
	});
	//点击按钮，，拼接url并跳转
	$submitBtn.click(function() {
		$q = $searchInput.val();
		console.log($searchInput.length)
		console.log($q)
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
	$('form').submit(function() {
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
	 * 当input的value改变
	 */
	$.cookie('lastSearchValue', '');
	window.first = true;
	$searchInput.bind('input propertychange', function() {
		window.searchVal = $.trim($searchInput.val());	//发生input值变更时读取其value(去掉两边空格)
		//console.log('当前值：'+searchVal);
		//console.log('cookie：'+$.cookie('lastSearchValue'))
		if(!searchVal && $.cookie('lastSearchValue')) {  //input被用户清空，不会发送请求
			$seWrap.fadeOut(100).empty();  
			$.cookie('lastSearchValue', '');
			try {clearTimeout(search_timer)} catch(e) {}
			return false;
		}
		if(searchVal && searchVal != $.cookie('lastSearchValue')) { //ajax条件
			try {clearTimeout(search_timer)} catch(e) {}
			$seWrapRec.hide();  //点击后先隐藏推荐内容，延迟时间后执行ajax
			window.search_timer = window.setTimeout(function() {
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
								if(v.eps) {
									var epsStr = '<span>共' + v.eps + '集</span>';
								} else { epsStr = ''}
								var searchItem = '<a class="search-item" href="' + v.url + 
								'"><div class="col-lg-2 col-md-2 col-sm-2 col-xs-2 img-wrap"><img src="' + v.poster +
								'"></div><div class="col-lg-10 col-md-10 col-sm-10 col-xs-10"><div class="movie-name">' + v.ch_name + '<span>' + 
								v.year + '</span></div><div class="foreign-name">' + v.foreign_name + '<br>' + epsStr +
								'</div></div></a>';
								$seWrap.append(searchItem).slideDown(100);
							});
						}
						
					}
					
				});
			},400);
		}
		
	});
	
	
	//加上默认推荐影片的排行数字
	$('.img-wrap:eq(0)').append('<span style="background:#e74c3c;">1</span>');
	$('.img-wrap:eq(1)').append('<span style="background:#f39c12;">2</span>');
	$('.img-wrap:eq(2)').append('<span style="background:#1abc9c;">3</span>');
	$('.img-wrap:eq(3)').append('<span style="background:#ccc;">4</span>');
	$('.img-wrap:eq(4)').append('<span style="background:#ddd;">5</span>');
	$('.img-wrap:eq(5)').append('<span style="background:#eee;">6</span>');
	
	$('#more-tags').click(function() {
		$(this).parent().find('.hidden').removeClass('hidden');
		$(this).fadeOut();
	});
});


/*
 * search结果页
 */
/*
$(function() {
	//每页显示条目数
	var items_per_page = $.cookie('page_num');
	if(items_per_page){
		$('#s1').val(items_per_page);
	}
	else{
		$.cookie('page_num', 10, {path: '/'});
	}
	
	//更改每页条目数
	$("#s1").change(function (){
		var value = $(this).val();
		var url = window.location.href
		//设置cookie，键为page_num，值为value，对根目录所有页面起作用
		$.cookie('page_num', value, {path: '/'});
		window.location.href = url;
	});
	
	//筛选栏动作
	$('#focus-bar li a').click(function() {
		var cur_url = window.location.href;
		var pattern_t = /type=(\w+)/;
		var pattern_r = /region=(\w+)/;
		if(cur_url.indexOf('type=')>0){
			var tid = cur_url.match(pattern_t)[1];
		} else{
			var tid = 'at';
		}
		if(cur_url.indexOf('region=')>0){
			var rid = cur_url.match(pattern_r)[1];
		} else{
			var rid = 'ar';
		}
		var fid = $(this).attr('id');
		window.location.href='/movie/?focus='+fid+'&type='+tid+'&region='+rid;
	});
	$('#show-filters').unbind('click');
	$('#region-bar li a').click(function() {
		var cur_url = window.location.href;
		var pattern_f = /focus=(\w+)/;
		var pattern_t = /type=(\w+)/;
		if(cur_url.indexOf('focus=')>0){
			var fid = cur_url.match(pattern_f)[1];
		} else{
			var fid = 'af';
		}
		if(cur_url.indexOf('type=')>0){
			var tid = cur_url.match(pattern_t)[1];
		} else{
			var tid = 'at';
		}	
		var rid = $(this).attr('id');
		window.location.href='/movie/?focus='+fid+'&type='+tid+'&region='+rid;
	});
	$('#type-bar li a').click(function(){
		var cur_url = window.location.href;
		var pattern_f = /focus=(\w+)/;
		var pattern_r = /region=(\w+)/;
		if(cur_url.indexOf('focus=')>0){
			var fid = cur_url.match(pattern_f)[1];
		} else{
			var fid = 'af';
		}
		if(cur_url.indexOf('region=')>0){
			var rid = cur_url.match(pattern_r)[1];
		} else{
			var rid = 'ar';
		}
		var tid = $(this).attr('id');
		window.location.href='/movie/?focus='+fid+'&type='+tid+'&region='+rid;
	});
	
	
	//更多筛选
	var $switch = $('#show-filters');
	var $switchArrow = $('#show-filters span');
	var $regionBar = $('#region-bar');
	var $typeBar = $('#type-bar');
	var $switchState = $.cookie('switch_state');  //读取cookie状态判断筛选栏是否打开
	if($switchState=='on') {
		$regionBar.removeClass('hide');
		$typeBar.removeClass('hide');
		$switch.html('收起筛选&nbsp;<span class="fui-arrow-left"></span>');
	}
	else {
		$switch.html('更多筛选&nbsp;<span class="fui-arrow-right"></span>');
	}
	$switch.click(function() {
		if($regionBar.hasClass('hide')) {
			$regionBar.removeClass('hide');
			$typeBar.removeClass('hide');
			$switch.html('收起筛选&nbsp;<span class="fui-arrow-left"></span>');
			$.cookie('switch_state', 'on', {path:'/'});
		} else {
			$regionBar.addClass('hide');
			$typeBar.addClass('hide');
			$switch.html('更多筛选&nbsp;<span class="fui-arrow-right"></span>');
			$.cookie('switch_state', 'off', {path:'/'});
		}
	});
	//筛选栏变色
	var url = window.location.href;
	var focus_keywords = ['guonei','guowai','gaofen','gengxin','not_released'];
	var num = 0;
	var color = '#fff';
	var focus_color = '#1abc9c';
	var region_color = '#3498db';
	var type_color = '#f39c12';
	$.each(focus_keywords,function(k,v){
		if(url.indexOf(v)>0){
			$('#'+v).css({'background-color': focus_color, 'color': color})
			num ++;
		}
	});
	if(num==0){
		$('#af').css({'background-color': focus_color, 'color': color})
	}
	
	var num = 0;
	var type_keywords = ['juqing','xiju','aiqing','qihuan','guzhuang','dongzuo','maoxian','kehuan',
	      	            'xuanyi','jingsong','kongbu','fanzui','zhanzheng','donghua','jilupian',
	      	            'tongxing','qingse','jiating','ertong','lishi','yundong','zhuanji'];
	$.each(type_keywords,function(k,v){
		if(url.indexOf(v)>0){
			$('#'+v).css({'background-color': region_color, 'color': color})
			num ++;
		}
	});
	if(num==0){
		$('#at').css({'background-color': region_color, 'color': color})
	}
	
	var num = 0;
	var type_keywords = ['mainland','hongkong','taiwan','america',
	                     'uk','french','japan','korea','thailand','india','otherregion'];
	$.each(type_keywords,function(k,v){
		if(url.indexOf(v)>0){
			$('#'+v).css({'background-color': type_color, 'color': color})
			num ++;
		}
	});
	if(num==0){
		$('#ar').css({'background-color': type_color, 'color': color})
	}
	
	//显示方式switch
	var $thumbSwitch = $.cookie('switch');
	$('#filter-switch a').click(function(e) {
		var $id = $(e.target).parent().attr('id');
		var $item = $('#da-thumbs li');
		if($id == 't1' && !$(e.target).hasClass('active')) {  //默认排列
			$.cookie('switch', 't1', {path:'/'});
			window.location.reload();
		} else if($id == 't2' && !$(e.target).hasClass('active')) {
			$.cookie('switch', 't2', {path:'/'});
			window.location.reload();
		} else if($id == 't3' && !$(e.target).hasClass('active')) {
			$.cookie('switch', 't3', {path:'/'});
			window.location.reload();
		}
	});
	
});



//加载HoverEffect
$(function() {

	$(' #da-thumbs > li ').each( function() { $(this).hoverdir({
		
	}); } );

});*/
