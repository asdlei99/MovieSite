


/*
 * search结果页
 */
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
	var cur_url = window.location.href;
	var pat_t = /type=(\w+)/;
	var pat_r = /region=(\w+)/;
	var pat_f = /focus=(\w+)/;
	var pat_c = /category=(\w+)/;
	var pat_k = /keyword=([^&]+)/;
	//关键词拆分
	if(cur_url.match(pat_k)) {
		var k = cur_url.match(pat_k)[1];
	}
	if(!k && k.match(/^\s$/)) {  //关键字为空或者全为不可见字符
		return false;
	} else {
		
	}
	
	$('#focus-bar li a:not("#more-filters")').click(function() {
		if(cur_url.match(pat_t)){var t = cur_url.match(pat_t)[1]} else{var t = 'at'}
		if(cur_url.match(pat_r)){var r = cur_url.match(pat_r)[1]} else{var r = 'ar'}
		if(cur_url.match(pat_c)){var c = cur_url.match(pat_c)[1]} else{var c = 'ac'}
		var f = $(this).attr('id');
		window.location.href='/search/result/?category='+c+'&focus='+f+'&type='+t+'&region='+r+'&keyword='+k;
	});
	$('#region-bar>li>a').click(function() {
		if(cur_url.match(pat_f)){var f = cur_url.match(pat_f)[1]} else{var f = 'af'}
		if(cur_url.match(pat_t)){var t = cur_url.match(pat_t)[1]} else{var t = 'at'}
		if(cur_url.match(pat_c)){var c = cur_url.match(pat_c)[1]} else{var c = 'ac'}
		var r = $(this).attr('id');
		window.location.href='/search/result/?category='+c+'&focus='+f+'&type='+t+'&region='+r+'&keyword='+k;
	});
	$('#type-bar>li>a').click(function() {
		if(cur_url.match(pat_f)){var f = cur_url.match(pat_f)[1]} else{var f = 'af'}
		if(cur_url.match(pat_r)){var r = cur_url.match(pat_r)[1]} else{var r = 'ar'}
		if(cur_url.match(pat_c)){var c = cur_url.match(pat_c)[1]} else{var c = 'ac'}
		var t = $(this).attr('id');
		window.location.href='/search/result/?category='+c+'&focus='+f+'&type='+t+'&region='+r+'&keyword='+k;
	});
	$('#category-bar>li>a').click(function() {
		if(cur_url.match(pat_f)){var f = cur_url.match(pat_f)[1]} else{var f = 'af'}
		if(cur_url.match(pat_r)){var r = cur_url.match(pat_r)[1]} else{var r = 'ar'}
		if(cur_url.match(pat_t)){var t = cur_url.match(pat_t)[1]} else{var t = 'at'}
		var c = $(this).attr('id');
		window.location.href='/search/result/?category='+c+'&focus='+f+'&type='+t+'&region='+r+'&keyword='+k;
	});
	
	
	//更多筛选
	var $switch = $('#more-filters');
	var $switchArrow = $('#more-filters span');
	var $regionBar = $('#region-bar');
	var $typeBar = $('#type-bar');
	var $switchState = $.cookie('switch_state');
	if($switchState=='on') {
		$regionBar.removeClass('hide');
		$typeBar.removeClass('hide');
		$switch.html('收起筛选&nbsp;<i class="fa fa-chevron-up"></i>');
	}
	else {
		$switch.html('更多筛选&nbsp;<i class="fa fa-chevron-down"></i>');
	}
	$switch.click(function(event) {
		if($regionBar.hasClass('hide')) {
			$regionBar.removeClass('hide');
			$typeBar.removeClass('hide');
			$switch.html('收起筛选&nbsp;<i class="fa fa-chevron-up"></i>');
			$.cookie('switch_state', 'on', {path:'/'});
		} else {
			$regionBar.addClass('hide');
			$typeBar.addClass('hide');
			$switch.html('更多筛选&nbsp;<i class="fa fa-chevron-down"></i>');
			$.cookie('switch_state', 'off', {path:'/'});
		}
		event.preventDefault;
	});
	//筛选栏变色
	var url = window.location.href;
	var focus_keywords = ['guonei','guowai','gaofen','gengxin','not_released'];
	var num = 0;
	$.each(focus_keywords,function(k,v){
		if(url.indexOf(v)>0){
			$('#'+v).addClass('focus-active')
			num ++;
		}
	});
	if(num==0){$('#af').addClass('focus-active')}
	
	var num = 0;
	var type_keywords = ['juqing','xiju','aiqing','qihuan','guzhuang','dongzuo','maoxian','kehuan',
	      	            'xuanyi','jingsong','kongbu','fanzui','zhanzheng','donghua','jilupian',
	      	            'tongxing','qingse','jiating','ertong','lishi','yundong','zhuanji','yinyue',
	      	            'gewu','xiqu'];
	$.each(type_keywords,function(k,v){
		if(url.indexOf(v)>0){
			$('#'+v).addClass('type-active');
			num ++;
		}
	});
	if(num==0){$('#at').addClass('type-active')}
	
	var num = 0;
	var region_keywords = ['mainland','hongkong','taiwan','america',
	                     'uk','french','japan','korea','thailand','india','otherregion'];
	$.each(region_keywords,function(k,v){
		if(url.indexOf(v)>0){
			$('#'+v).addClass('region-active');
			num ++;
		}
	});
	if(num==0){$('#ar').addClass('region-active')}
	
	var num = 0;
	var category_keywords = {'all':'全部','movie':'电影','tv':'电视剧','anime':'动漫','show':'综艺'};
	$.each(category_keywords,function(k,v){
		if(url.indexOf(k)>0){
			$('#'+k).addClass('category-active');
			/*if($('.t3-wrapper').length>0) {
				$('.t3-wrapper table > thead > tr > th:first').text(v+'名')
			}*/
			num ++;
		}
	});
	if(num==0){$('#all').addClass('category-active')}

	
	
	//显示方式switch
	var $thumbSwitch = $.cookie('switch');
	/*
	if(!$thumbSwitch || $thumbSwitch == 't1') {  //若无cookies，默认排序
		$('#filter-switch #t1 a').addClass('active');
	} else if($thumbSwitch == 't2') {
		$('#filter-switch #t2 a').addClass('active');
	} else if($thumbSwitch == 't3') {
		$('#filter-switch #t3 a').addClass('active');
	}*/
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

});
