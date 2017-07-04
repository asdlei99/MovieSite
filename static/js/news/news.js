/*
 * News Index 
 */

if($('.flexslider').length) {
	$(window).load(function() {
		$('.flexslider').flexslider({
			animation: "fade",
			slideshowSpeed: 5000,
			start: function() {
				$('.loading-bg').remove();
			}
		});
	});
}

function getMoreReplies() {
	$('.dmr').click(function() {
		var $_this = $(this);
		var rid = $_this.attr('data-rid');
		var remainder = $_this.attr('data-remainder');
		var originHtml = $_this.html();
		$_this.html('<i class="fa fa-spinner fa-spin mr-10"></i>&nbsp;加载中...');
		$.ajax({
			url: '/news/get_more_replies/',
			data: {'rid':rid, 'remainder':remainder},
			type: 'POST',
			success: function(callback) {
				var obj = $.parseJSON(callback);
				if(!obj.msg) {
					$.each(obj, function(i,e) {
						if(!i==0) {
							var rrHtml = '<li class="media" data-rrid="' + this.id + '">\
							  <a class="media-left" href="/user/home/profile/' + this.user_id + '/"><img class="media-object img-circle avatar-xs" src="' + this.thumb_s + '"></a>\
							  <div class="media-body">\
								<a class="media-heading" href="/user/home/profile/'+ this.user_id +'/">' + this.username + '</a>\
								&nbsp;&nbsp;<time>' + this.create_date + '</time>\
								<div class="rr-content">' + this.content + '</div></div></li>';
							var $rrWrap = $_this.parent().find('.rr-wrap');
							$(rrHtml).hide().appendTo($rrWrap).fadeIn();
						}
					});
					//更改条数显示
					if(!obj[0]) {
						$_this.remove();
					} else {
						$_this.attr('data-remainder',obj[0]);
						$_this.html('还有'+obj[0]+'条回复&nbsp;&nbsp;<i class="fa fa-angle-down"></i>');
					}
				} else {
					$_this.html('加载失败，请重试')
				}
			},
			error: function() {
				$_this.html(originHtml);
			}
		});
	});
}

function getMoreComments($target) {
	$target.click(function() {
		$_this = $(this);
		var nid = $_this.attr('data-nid');
		var remainder = $_this.attr('data-remainder');
		$('#dmc').html('<img src="/static/images/common/loading/ajax-spinner.gif">');
		$.ajax({
			url: '/news/get_more_comments/',
			data: {'nid':nid, 'remainder':remainder},
			type: 'POST',
			success: function(callback) {
				var obj = $.parseJSON(callback);
				var new_remainder = obj[0];
				$.each(obj, function(i,e) {
					if(!i==0) {
						var rrHtml = '<ul class="media-list rr-wrap">';
						var rrObj = this.rr;
						for(var i=0; i<rrObj.length; i++) {
							var rrTempHtml = '<li class="media" data-rrid="' + rrObj[i].id + '"><div class="media-left">\
							<a href="/user/profile/' + rrObj[i].user_id + '/" target="_blank"><img class="media-object img-circle avatar-xs" src="' + rrObj[i].thumb_s + '"></a></div>\
							<div class="media-body"><div class="media-heading"><a href="/user/profile/' + rrObj[i].user_id + '/" target="_blank">' + rrObj[i].uname + '</a>&nbsp;&nbsp;<time>' + rrObj[i].create_date + '</time></div>\
							<div class="rr-content text-content">' + rrObj[i].content + '</div></div></li>';
							rrHtml += rrTempHtml;
						}
						rrHtml += '</ul>';
						if(this.rr_counts>5) {
							var rmd = this.rr_counts - 5;
							var moreRRHtml = '<a class="dmr text-smaller pull-left" data-remainder="' + rmd + '" data-rid="' + this.id + '" role="button">还有' + rmd + '条回复&nbsp;&nbsp;<i class="fa fa-angle-down"></i></a><div class="clearfix"></div>';
							rrHtml += moreRRHtml;
						}
						
						var commentHtml = '<li class="list-group-item"><div class="media-left">\
			            	<a href="/user/profile/' + this.user_id + '/" target="_blank"><img class="media-object img-circle avatar-s" src="' + this.thumb_s + '"></a></div>\
			                <div class="media-body"><div class="media-heading">\
			                <a href="/user/profile/' + this.user_id + '/">' + this.uname + '</a><span class="rr-btn-group" data-rid="' + this.id + '">\
			                <button class="btn btn-xs btn-thumbs-up"><i class="fa fa-thumbs-o-up"></i>&nbsp;' + this.like_counts + '&nbsp;</button>\
			                <button class="btn btn-xs btn-display-rr">回复</button>\
			                </span>&nbsp;&nbsp;<time>' + this.create_date + '</time></div><div class="r-content text-content">' + this.content + '</div>' + rrHtml + '</div></li>';
			            
						$(commentHtml).hide().appendTo($('#comment-list')).fadeIn();
					}
				});
				if(!new_remainder) {
					$('#dmc').html('<span style="color:#999">没有更多了~</span>');
				} else {
					$('#dmc').html('<button class="btn btn-primary btn-xs" data-nid="' + nid + '" data-remainder="' + new_remainder + '">还有' + new_remainder + '条评论&nbsp;&nbsp;<i class="fa fa-angle-down"></i></button>');
					getMoreComments($('#dmc>.btn'));
				}
				$('.dmr').unbind();
				getMoreReplies($('.dmr'));
				initRR($('#comment-list>li.list-group-item'));
			},
			error: function() {
				
			}
		});
	});
}


//回复按钮初始化绑定
function initRR($target) {
	$target.find('.btn-display-rr').unbind();
	$target.find('.btn-display-rr').click(function() {
		if(!checkLogin()) {
			return false;
		}
		var $_this = $(this);
		var $ra = $('.reply-area');
		if(typeof($ra.find('.text-wrapper').val()) == 'undefined') {
			var textVal = '';
		} else {
			var textVal = $ra.find('.text-wrapper').val();
		}
		
		if($ra.length && textVal) {
			var $modalEC = $('#editCancelModal');
			$modalEC.modal();
			$('#cancel-ce').click(function() {
				$modalEC.modal('hide');
			});
			$('#confirm-ce').unbind();
			$('#confirm-ce').click(function() {
				$ra.find('.text-wrapper').val('');
				$modalEC.modal('hide');
				$_this.unbind('click');
				initRR($_this);
				$_this.trigger('click');

			});
			//return false;
		} else {
			var rid = $_this.parent().attr('data-rid');
			var textareaHtml = '<div class="form-group reply-area submit-area">\
				  <div class="input-group">\
				    <textarea class="form-control text-wrapper" placeholder="我来说一句" rows="4" maxlength="200"></textarea>\
				  </div>\
				  <div class="submit-btn-group">\
				  <span class="emotion-icon-rr" role="button"><i class="fa fa-smile-o"></i></span>\
				    <div class="btn-group">\
				      <button class="btn btn-primary btn-sm btn-reply btn-submit">回复</button>\
				    </div>\
				  </div>\
				</div>';
			var $wrap = $_this.parent().parent().parent();
			//var $replyArea = $wrap.find('.reply-area');
			//增加回复框
			if($('.reply-area').length) {
				$('.reply-area').remove();
			}
			$wrap.append(textareaHtml);
			var $textarea = $wrap.find('.text-wrapper');
			var $area = $wrap.find('.reply-area');
			ChangeTextareaState($wrap, 100);
			$textarea.focus();

			var $replyBtn = $wrap.find('.btn-reply');
			//回复绑定
		
			$replyBtn.bind('click', function() {
				var tip = checkReplyContent($textarea);
				if(tip) {
					showTip(tip, 'warning', $area);
					return;
				}
				var rrContent = $textarea.val();
				var rrContent = AnalyticEmotion(rrContent);
				//var rrContent = rrContent.replace(/<[^i].*?>/,'')
				if(!$wrap.find('.rr-wrap').length) {
					$wrap.find('.r-content').after('<ul class="media-list rr-wrap"></ul>');
					
				}
				var $rrWrap = $wrap.find('.rr-wrap');
				$area.prepend(loadingCoverHtml);
				$.ajax({
					url: '/news/submit_reply_reply/',
					data: {'rid':rid, 'content':rrContent},
					type: 'POST',
					success: function(callback) {
						itemFadeOut($wrap, '.loading-cover')
						obj = jQuery.parseJSON(callback);
						if(obj.success) {
							$textarea.val('');
							var rrHtml = '<li class="media" data-rrid="' + obj.rrid + '">\
							  <a class="media-left" href="/user/home/profile/' + obj.new_uid + '/"><img class="media-object img-circle avatar-xs" src="' + obj.new_avatar + '"></a>\
							  <div class="media-body">\
								<a class="media-heading" href="/user/home/profile/'+ obj.new_uid +'/">' + obj.new_username + '</a>\
								&nbsp;&nbsp;<time>刚刚</time>\
								<div class="rr-content">' + obj.content + '</div></div></li>';
							$(rrHtml).hide().appendTo($rrWrap).fadeIn();

							var $newComment = $('#comment-list').children('li:first');
							console.log($newComment.length);
							initRR($newComment.find('.btn-display-rr'));
						} else {
							if(obj.msg=='901') {
								var tip = '请输入回复的内容';
							} else if(obj.msg=='902') {
								var tip = '回复内容不能全部为空格';
							} else {
								var tip = obj.msg;
							}
							showTip(tip, 'warning', $area);
						}
						
					}
				});
				
			}); //reply-btn bind
		}
			

	});
	
	
	//点赞
	$target.find('.btn-thumbs-up').click(function() {
		if(!checkLogin()) {
			return false;
		} else {
			var $_this = $(this);
			var clsRefresh = 'fa fa-circle-o-notch fa-spin';
			var clsThumbsUp = 'fa fa-thumbs-o-up';
			$_this.children('.fa').attr('class',clsRefresh);
			$_this.attr('disabled',true);
			var rid = $_this.parent().attr('data-rid');
			var like_counts = $_this.text().trim();
			$.ajax({
				url: '/news/reply_like/',
				data: {'rid': rid},
				type: 'POST',
				success: function(callback) {
					$('.btn-thumbs-up').children('.fa').attr('class',clsThumbsUp);
					$('.btn-thumbs-up').removeAttr('disabled');
					var obj = $.parseJSON(callback);
					var msg = obj.msg;
					if(msg) {
						if(msg=='910') {  //已点赞
							$_this.attr({'data-toggle':'tooltip','data-trigger':'click','data-original-title':'你已经赞过这条评论啦'});
							$_this.tooltip('show');
							setTimeout(function() {
								$_this.tooltip('destroy');
							},800);
						} else if(msg=='401') {
							$('#loginModal').modal();
							$.cookie('logined', 'no');
						} else if(msg=='success') {  //成功
							console.log(like_counts)
							var new_counts = like_counts*1 + 1*1
							console.log(new_counts)
							var new_html = '<i class="fa fa-thumbs-o-up"></i>&nbsp;' + new_counts + '&nbsp;';
							$_this.html(new_html);
						}
					} else {
						$_this.attr({'data-toggle':'tooltip','data-trigger':'click','data-original-title':msg});
						$_this.tooltip('show');
						setTimeout(function() {
							$_this.tooltip('destroy');
						},800);
					}
				}
			});
		}
	});
}

function InitBtnPublish($target) {
	$target.click(function() {
		$_this = $(this);
		var nid = $(this).attr('data-nid');
		var $text = $('.publish-area .text-wrapper');
		var $this = $(this);
		var $area = $('.publish-area');
		var tip = checkReplyContent($text);
		if(tip) {
			showTip(tip, 'warning', $area);
			return;
		}
		$area.prepend(loadingCoverHtml);
		var $defaultBanner = $('#comment-list>div.text-center');
		if($defaultBanner.length) {
			$defaultBanner.remove();
		}
		var submitContent = $text.val();
		var submitContent = AnalyticEmotion(submitContent);
		var submitContent = replaceWithBr(submitContent);  //换行替换为<br>
		$.ajax({
			url: '/news/submit_reply/',
			data: {'id':nid, 'content':submitContent},
			type: 'POST',
			success: function(callback) {
				itemFadeOut($area, '.loading-cover');
				obj = jQuery.parseJSON(callback);
				if(obj.success) {
					$text.val('');
					
					var replyHTML = '<li class="list-group-item">\
		                <div class="media-left"><a href="/user/profile/' + obj.uid + '" target="_blank"><img class="media-object img-circle avatar-s" src="' + obj.avatar_s + '"></a></div>\
		                <div class="media-body">\
		                  <div class="media-heading"><a href="/user/home/profile/70/" target="_blank">' + obj.uname + '</a>\
		                  <span class="rr-btn-group" data-rid="' + obj.new_rid + '">\
		                    <button class="btn btn-xs btn-thumbs-up"><i class="fa fa-thumbs-o-up"></i>&nbsp;0&nbsp;</button>\
		                    <button class="btn btn-xs btn-display-rr">回复</button>\
		                  </span>&nbsp;&nbsp;<time>刚刚</time></div>\
		                  <div class="r-content text-content">' + obj.content + '</div>\
		                </div></li>';
                    //修改comment数量显示
                    var $commentCounts = $('#comment > .panel-heading > span');
                	var counts = $commentCounts.text();
                	var newCounts = counts*1 + 1;
                	$commentCounts.text(newCounts);

                	var $commentList = $('#comment-list');

                	//动态添加评论并滚动到#comment
					$('html,body').animate({scrollTop:$('#comment').offset().top},300);
					$(replyHTML).hide().prependTo($commentList).fadeIn();
					var $newComment = $commentList.children('li:first');
					initRR($newComment);
					
				} else {
					if(obj.msg=='901') {
						showTip('回复内容不能为空', 'danger' ,$area)
					} else if(obj.msg=='902') {
						showTip('回复内容不能全部为空格', 'warning' ,$area)
					} else if(obj.msg=='401') {
						showTip('', 'danger' ,$area)
					} else {
						var tip = obj.msg + '错误，请联系管理员';
						showTip(tip, 'danger' ,$area)
					}
				}
				
			}

		});
	
	});
}



/*
 * Templates
 */

$(function() {
	if($('#comment').length) {
		var $box = $('.publish-area');
		ChangeTextareaState($box, 250);
		//显示更多回复
		getMoreReplies();
		//显示更多评论
		getMoreComments($('#dmc>.btn'));
		//检查登录
		$('.submit-area .text-wrapper').focus(checkLogin);
		$('.rr-btn-group > btn').click(checkLogin);
		
		//发表评论
		InitBtnPublish($('.btn-publish'));
		initRR($('#comment-list>li.list-group-item'));
	} else {
		var $showMore = $('.btn-get-more');
		$showMore.click(function() {
			var $_this = $(this);
			$_this.hide();
			var $btnWrap = $_this.parent();
			var loadingHtml = '<img class="loading-img" src="/static/images/common/loading/ajax-spinner.gif">';
			$(loadingHtml).hide().prependTo($btnWrap).fadeIn();
			var newsCounts = $('.news-list-item').length;
			$.ajax({
				url: '/news/get_more_news/',
				data: {'cur_news_counts': newsCounts},
				type: 'POST',
				success: function(callback) {
					$btnWrap.find('img').remove();
					$_this.fadeIn();
					var obj = $.parseJSON(callback);
					$.each(obj.more_news, function(idx, sobj) {
						var itemHtml = '<div class="col-lg-3 col-md-4 col-sm-4 col-xs-6 news-list-item">\
					          <a class="news-img-wrap" href="/news/' + this.id + '/" target="_blank"><img class="img-rounded" src="' + this.news_image + '" alt="' + this.title + '"></a>\
					          <h3 class="news-title"><a href="/news/' + this.id + '/" target="_blank">' + this.title + '</a></h3>\
					          <p class="subtitle"><a href="/news/' + this.id + '/" target="_blank">' + this.subtitle + '</a></p>\
					          <time><i class="fa fa-calendar-o"></i> ' + this.create_date + '</time></div>'
						$(itemHtml).hide().appendTo('.news-list').fadeIn();
					});
					console.log(obj.more_news.length)
					if (obj.more_news.length < 12) {
						
						$btnWrap.html('<span style="color:#888;line-height:37px;">已经没有更多了 ...</span>')
					}
				},
				error: function() {
					$('.loading-img').remove();
					$_this.html('加载失败');
				}
			});
		});
	}
	
	
});

