/**
 * 
 */

$(function() {
	
	//将本周TOP10显示出的panel标题背景变色
	var $panel = $('.panel-collapse');
	$.each($panel, function(e) {
		if($(this).hasClass('in')) {
			$(this).parent().addClass('panel-info');
		}
		else {
			$(this).parent().addClass('panel-closed');
		}
	});
	var $panelTitle = $('#accordion1 .panel-title a');
	$panelTitle.bind('click',function(event) {  //先将已有的颜色去掉
		$.each($panel, function() {
			if($(this).parent().hasClass('panel-info')) {  
				$(this).parent().removeClass('panel-info').addClass('panel-closed');
			}
			$(event.target).parent().parent().parent().removeClass('panel-closed').addClass('panel-info');
		});

	});
	
	
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
		//设置cookie，键为page_num，值为value，对根目录所有页面起作用
		$.cookie('page_num', value, {path: '/'});
		window.location.reload();
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
		window.location.href='/tv/?focus='+fid+'&type='+tid+'&region='+rid;
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
		window.location.href='/tv/?focus='+fid+'&type='+tid+'&region='+rid;
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
		window.location.href='/tv/?focus='+fid+'&type='+tid+'&region='+rid;
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
		$switch.html('收起筛选&nbsp;<span class="fui-arrow-left"></span>')
	}
	else {
		$switch.html('更多筛选&nbsp;<span class="fui-arrow-right"></span>')
	}
	$switch.click(function() {
		if($regionBar.hasClass('hide')) {
			$regionBar.removeClass('hide');
			$typeBar.removeClass('hide');
			$switch.html('收起筛选&nbsp;<span class="fui-arrow-left"></span>')
			$.cookie('switch_state', 'on', {path:'/'});
		} else {
			$regionBar.addClass('hide');
			$typeBar.addClass('hide');
			$switch.html('更多筛选&nbsp;<span class="fui-arrow-right"></span>')
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
/*
function RemoveKeyword(){
	var cur_url = window.location.href;
	var fid = 'af';
	var tid = 'at';
	var rid = 'ar';
	$.ajax({
		url:'/movie/',
		type:'GET',
		data:{'focus':fid,'type':tid,'region':rid},
		success:function(callback){
			window.location.href='/movie/?focus='+fid+'&type='+tid+'&region='+rid;
		}
	});
}*/




// For Demo purposes only (show hover effect on mobile devices)
/*
[ ].slice.call(document.querySelectorAll('a[href="#"')).forEach(function (el) {
    el.addEventListener('click', function (ev) { ev.preventDefault(); });
});*/