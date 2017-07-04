/*
 * 
 */


//收藏电影
function collect() {
	$('.btn-collect').click(function() {
		if(!checkLogin()) {
			return false;
		} else {
			$_this = $(this);
			$_this.unbind('click');
			var xid = $_this.attr('data-id');
			$_this.attr('disabled',true);
			$.ajax({
				url: '/user/collect/',
				data: {'cate':cate, 'xid':xid},
				type: 'POST',
				complete: function() {
					$_this.removeAttr('disabled');
				},
				success: function(callback) {
					var obj = $.parseJSON(callback);
					console.log(obj.msg)
					if(obj.msg=='success') {
						$_this.html('<i class="fa fa-check"></i> 已藏');
						$_this.removeClass('btn-collect').addClass('btn-collected');
						$_this.attr({'data-toggle':'tooltip','data-trigger':'click','data-original-title':'收藏成功'});
						$_this.tooltip('show');
						setTimeout(function() {
							$_this.tooltip('destroy');
						},800);
						cancelCollect(); //重新绑定
					} else if(obj.msg=='104' || obj.msg=='401') {
						$_this.tooltip('hide');
						if(obj.msg=='104') {
							$_this.html('<i class="fa fa-check"></i> 已藏');
							$_this.attr({'data-toggle':'tooltip','data-trigger':'click','data-original-title':'你已经收藏过这部电影啦'});
						} else if(obj.msg=='401') {
							$_this.attr({'data-toggle':'tooltip','data-trigger':'click','data-original-title':'请登录后进行收藏'});
						}
						$_this.tooltip('show');
						var timeout1 = setTimeout(function() {
							clearTimeout(timeout1);
							$_this.tooltip('hide');
							$_this.removeAttr('data-toggle','data-original-title','data-trigger')
						},800)
					} else {
						$_this.html('<i class="fa fa-star-o"></i> 重试');
					}
				},
				error: function() {
					$_this.html('<i class="fa fa-star-o"></i> 收藏');
				}
			});
		}			
	});	
}
//取消收藏
function cancelCollect() {
	
	var $cancel = $('.btn-collected');
	$cancel.click(function() {
		console.log('cancel-collect')
		$_this = $(this);
		$_this.unbind('click');
		var xid = $_this.attr('data-id');
		$_this.attr('disabled',true);
		$.ajax({
			url: '/user/cancel_collect/',
			data: {'cate':cate, 'xid':xid},
			type: 'POST',
			complete: function() {
				$_this.removeAttr('disabled');
			},
			success: function(callback) {
				var obj = $.parseJSON(callback);
				console.log(obj)
				console.log(obj.msg)
				if(obj.msg=='success') {
					$_this.html('<i class="fa fa-star-o"></i> 收藏');
					$_this.removeClass('btn-collected').addClass('btn-collect');
					$_this.attr({'data-toggle':'tooltip','data-trigger':'click','data-original-title':'取消收藏成功'});
					$_this.tooltip('show');
					setTimeout(function() {
						$_this.tooltip('destroy');
					},800);
					collect(); //添加收藏class后重新绑定
				} else {
					$_this.html('<i class="fa fa-check"></i> 重试');
				}
			},
			error: function() {
				$_this.html('<i class="fa fa-check"></i> 已藏');
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
			url: '/'+cate+'/get_more_replies/',
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
		var xid = $_this.attr('data-xid');
		var remainder = $_this.attr('data-remainder');
		$('#dmc').html('<img src="/static/images/common/loading/ajax-spinner.gif">');
		$.ajax({
			url: '/' + cate + '/get_more_comments/',
			data: {'xid':xid, 'remainder':remainder},
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
					$('#dmc').html('<button class="btn btn-primary btn-xs" data-xid="' + xid + '" data-remainder="' + new_remainder + '">还有' + new_remainder + '条评论&nbsp;&nbsp;<i class="fa fa-angle-down"></i></button>');
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
					url: '/'+cate+'/submit_reply_reply/',
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
				url: '/'+cate+'/reply_like/',
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
		var xid = $(this).attr('data-xid');
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
		if(typeof(window.selected_rating)=='undefined') {
			window.selected_rating = 0;
		}

		$.ajax({
			url: '/'+cate+'/submit_reply/',
			data: {'id':xid, 'content':submitContent, 'rating':selected_rating},
			type: 'POST',
			success: function(callback) {
				itemFadeOut($area, '.loading-cover');
				obj = jQuery.parseJSON(callback);
				if(obj.success) {
					$text.val('');
					
					if(!selected_rating == 0) {
						var ratingHTML = '<div class="rating-container theme-krajee-fa rating-xxs">\
		                    <div class="rating">\
		                      <span class="empty-stars"><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span></span>\
		                      <span class="filled-stars" style="width: ' + selected_rating + '0%;"><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span></span>\
		                    </div>\
		                    </div>&nbsp;&nbsp;';
					} else {
						var ratingHTML = '';
					}
					var replyHTML = '<li class="list-group-item">\
		                <div class="media-left"><a href="/user/profile/' + obj.uid + '" target="_blank"><img class="media-object img-circle avatar-s" src="' + obj.avatar_s + '"></a></div>\
		                <div class="media-body">\
		                  <div class="media-heading"><a href="/user/home/profile/70/" target="_blank">' + obj.uname + '</a>\
		                  <span class="rr-btn-group" data-rid="' + obj.new_rid + '">\
		                    <button class="btn btn-xs btn-thumbs-up"><i class="fa fa-thumbs-o-up"></i>&nbsp;0&nbsp;</button>\
		                    <button class="btn btn-xs btn-display-rr">回复</button>\
		                  </span>&nbsp;&nbsp;' + ratingHTML + '<time>刚刚</time></div>\
		                  <div class="r-content text-content">' + obj.content + '</div>\
		                </div></li>'
					var ratedHTML = '<div class="rating" data-toggle="tooltip" data-placement="top" title="" data-original-title="你已经评过分啦">\
                          <span class="empty-stars"><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span></span>\
                          <span class="filled-stars" style="width: ' + selected_rating + '0%;"><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span><span class="star"><i class="fa fa-star"></i></span></span>\
                        </div>\
                        <div class="caption"><span class="label label-default">' + selected_rating + '分</span></div>'

					if(!selected_rating == 0) {
						console.log('rating_clear');
						$('.publish-area .rating').tooltip({'container':'body','data-toggle':'tooltip','data-placement':'top', 'data-original-title':'你已经评过分啦'}); //加载tooltip
						$('.publish-area .rating').tooltip('show');
						$('.publish-area .rating-container').removeClass('rating-animate').html('').append(ratedHTML);  //打分input替换为已打分状态
						window.selected_rating = 0;
					}
                    //修改comment数量显示
                    var $commentCounts = $('#comment > .panel-heading > span');
                	var counts = $commentCounts.text();
                	var newCounts = counts*1 + 1;
                	$commentCounts.text(newCounts);

					
                	var $commentList = $('#comment-list');

                	/*var $explicitCom = $commentList.find('li.media:not([class="media myhide"])');
					var $allCom = $('#comment-list > .media');
					if($allCom.length==5) {  //已经有5个，需加上显示更多按钮
						$commentList.after('<button class="btn btn-default-outline btn-sm btn-block" id="dmc">加载更多&nbsp;<i class="fa fa-angle-down"></i></button>');
						showMoreCom();
						$('#comment-list > .media:last').addClass('myhide');
					}
					if($explicitCom.length>4) {
						$explicitCom.eq($explicitCom.length-1).addClass('myhide');
					}*/
                	//动态添加评论并滚动到#comment
					$('html,body').animate({scrollTop:$('#comment').offset().top},300);
					$(replyHTML).hide().prependTo($commentList).fadeIn();
					var $newComment = $commentList.children('li:first');
					initRR($newComment);
					//($('.btn-thumbs-up'), $('.btn-display-rr')).unbind('click');  //先解除再绑定
					
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

$(function() {
	
	//改变下载的input状态
	var $downInput = $('#download input');
	var $totalWidth = $('#download').width();
	$.each($downInput, function() {
		var $aWidth = $(this).prev().width();
		var inputWidth = parseInt($totalWidth - $aWidth - 102) + 'px';
		$(this).css('width', inputWidth);
	});
	$downInput.focus(function() {
		$(this).select();
	});
	

	//ZeroClipboard
	var clip = new ZeroClipboard($('.clip-btn'));
	clip.on( 'copy', function(event) {
		$downLink = $(event.target).prev().val();
        event.clipboardData.setData('text/plain', $downLink);
      } );

	//点击2秒后清除tooltip
	$('.clip-btn').click(function() {
		$_this = $(this);
		if(typeof(st)=='undefined') {} 
		else {
			clearTimeout(st);
		}
		
		$('.tooltip').tooltip('destroy');
		$_this.attr({'data-toggle':'tooltip', 'data-trigger':'click', 'data-placement':'left', 'data-original-title':'复制成功'});
		$_this.tooltip('show');
		st = window.setTimeout(function() {
			$_this.tooltip('destroy');
		}, 800);
	});

	
	var $box = $('.publish-area');
	ChangeTextareaState($box, 250);

	//绑定收藏
	cancelCollect();	
	collect();
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
	


});

/*!
 * bootstrap-star-rating v4.0.2
 * http://plugins.krajee.com/star-rating
 *
 * Author: Kartik Visweswaran
 * Copyright: 2014 - 2016, Kartik Visweswaran, Krajee.com
 *
 * Licensed under the BSD 3-Clause
 * https://github.com/kartik-v/bootstrap-star-rating/blob/master/LICENSE.md
 */!function(e){"use strict";"function"==typeof define&&define.amd?define(["jquery"],e):"object"==typeof module&&module.exports?module.exports=e(require("jquery")):e(window.jQuery)}(function(e){"use strict";e.fn.ratingLocales={},e.fn.ratingThemes={};var t,a,n,r,i,l,s,o,c,u,h;t=".rating",a=0,n=5,r=.5,i=function(t,a){return null===t||void 0===t||0===t.length||a&&""===e.trim(t)},l=function(e,t){return e?" "+t:""},s=function(e,t){e.removeClass(t).addClass(t)},o=function(e){var t=(""+e).match(/(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/);return t?Math.max(0,(t[1]?t[1].length:0)-(t[2]?+t[2]:0)):0},c=function(e,t){return parseFloat(e.toFixed(t))},u=function(e,a,n,r){var i=r?a:a.split(" ").join(t+" ")+t;e.off(i).on(i,n)},h=function(t,a){var n=this;n.$element=e(t),n._init(a)},h.prototype={constructor:h,_parseAttr:function(e,t){var l,s,o,c,u=this,h=u.$element,d=h.attr("type");if("range"===d||"number"===d){switch(s=t[e]||h.data(e)||h.attr(e),e){case"min":o=a;break;case"max":o=n;break;default:o=r}l=i(s)?o:s,c=parseFloat(l)}else c=parseFloat(t[e]);return isNaN(c)?o:c},_setDefault:function(e,t){var a=this;i(a[e])&&(a[e]=t)},_listenClick:function(e,t){return e.stopPropagation(),e.preventDefault(),e.handled===!0?!1:(t(e),void(e.handled=!0))},_starClick:function(e){var t,a=this;a._listenClick(e,function(e){return a.inactive?!1:(t=a._getTouchPosition(e),a._setStars(t),a.$element.trigger("change").trigger("rating.change",[a.$element.val(),a._getCaption()]),void(a.starClicked=!0))})},_starMouseMove:function(e){var t,a,n=this;!n.hoverEnabled||n.inactive||e&&e.isDefaultPrevented()||(n.starClicked=!1,t=n._getTouchPosition(e),a=n.calculate(t),n._toggleHover(a),n.$element.trigger("rating.hover",[a.val,a.caption,"stars"]))},_starMouseLeave:function(e){var t,a=this;!a.hoverEnabled||a.inactive||a.starClicked||e&&e.isDefaultPrevented()||(t=a.cache,a._toggleHover(t),a.$element.trigger("rating.hoverleave",["stars"]))},_clearClick:function(e){var t=this;t._listenClick(e,function(){t.inactive||(t.clear(),t.clearClicked=!0)})},_clearMouseMove:function(e){var t,a,n,r,i=this;!i.hoverEnabled||i.inactive||!i.hoverOnClear||e&&e.isDefaultPrevented()||(i.clearClicked=!1,t='<span class="'+i.clearCaptionClass+'">'+i.clearCaption+"</span>",a=i.clearValue,n=i.getWidthFromValue(a)||0,r={caption:t,width:n,val:a},i._toggleHover(r),i.$element.trigger("rating.hover",[a,t,"clear"]))},_clearMouseLeave:function(e){var t,a=this;!a.hoverEnabled||a.inactive||a.clearClicked||!a.hoverOnClear||e&&e.isDefaultPrevented()||(t=a.cache,a._toggleHover(t),a.$element.trigger("rating.hoverleave",["clear"]))},_resetForm:function(e){var t=this;e&&e.isDefaultPrevented()||t.inactive||t.reset()},_setTouch:function(e,t){var a,n,r,l,s,o,c,u=this,h="ontouchstart"in window||window.DocumentTouch&&document instanceof window.DocumentTouch;h&&!u.inactive&&(a=e.originalEvent,n=i(a.touches)?a.changedTouches:a.touches,r=u._getTouchPosition(n[0]),t?(u._setStars(r),u.$element.trigger("change").trigger("rating.change",[u.$element.val(),u._getCaption()]),u.starClicked=!0):(l=u.calculate(r),s=l.val<=u.clearValue?u.fetchCaption(u.clearValue):l.caption,o=u.getWidthFromValue(u.clearValue),c=l.val<=u.clearValue?o+"%":l.width,u._setCaption(s),u.$filledStars.css("width",c)))},_initTouch:function(e){var t=this,a="touchend"===e.type;t._setTouch(e,a)},_initSlider:function(e){var t=this;i(t.$element.val())&&t.$element.val(0),t.initialValue=t.$element.val(),t._setDefault("min",t._parseAttr("min",e)),t._setDefault("max",t._parseAttr("max",e)),t._setDefault("step",t._parseAttr("step",e)),(isNaN(t.min)||i(t.min))&&(t.min=a),(isNaN(t.max)||i(t.max))&&(t.max=n),(isNaN(t.step)||i(t.step)||0===t.step)&&(t.step=r),t.diff=t.max-t.min},_initHighlight:function(e){var t,a=this,n=a._getCaption();e||(e=a.$element.val()),t=a.getWidthFromValue(e)+"%",a.$filledStars.width(t),a.cache={caption:n,width:t,val:e}},_getContainerCss:function(){var e=this;return"rating-container"+l(e.theme,"theme-"+e.theme)+l(e.rtl,"rating-rtl")+l(e.size,"rating-"+e.size)+l(e.animate,"rating-animate")+l(e.disabled||e.readonly,"rating-disabled")+l(e.containerClass,e.containerClass)},_checkDisabled:function(){var e=this,t=e.$element,a=e.options;e.disabled=void 0===a.disabled?t.attr("disabled")||!1:a.disabled,e.readonly=void 0===a.readonly?t.attr("readonly")||!1:a.readonly,e.inactive=e.disabled||e.readonly,t.attr({disabled:e.disabled,readonly:e.readonly})},_addContent:function(e,t){var a=this,n=a.$container,r="clear"===e;return a.rtl?r?n.append(t):n.prepend(t):r?n.prepend(t):n.append(t)},_generateRating:function(){var t,a,n,r=this,i=r.$element;a=r.$container=e(document.createElement("div")).insertBefore(i),s(a,r._getContainerCss()),r.$rating=t=e(document.createElement("div")).attr("class","rating").appendTo(a).append(r._getStars("empty")).append(r._getStars("filled")),r.$emptyStars=t.find(".empty-stars"),r.$filledStars=t.find(".filled-stars"),r._renderCaption(),r._renderClear(),r._initHighlight(),a.append(i),r.rtl&&(n=Math.max(r.$emptyStars.outerWidth(),r.$filledStars.outerWidth()),r.$emptyStars.width(n))},_getCaption:function(){var e=this;return e.$caption&&e.$caption.length?e.$caption.html():e.defaultCaption},_setCaption:function(e){var t=this;t.$caption&&t.$caption.length&&t.$caption.html(e)},_renderCaption:function(){var t,a=this,n=a.$element.val(),r=a.captionElement?e(a.captionElement):"";if(a.showCaption){if(t=a.fetchCaption(n),r&&r.length)return s(r,"caption"),r.html(t),void(a.$caption=r);a._addContent("caption",'<div class="caption">'+t+"</div>"),a.$caption=a.$container.find(".caption")}},_renderClear:function(){var t,a=this,n=a.clearElement?e(a.clearElement):"";if(a.showClear){if(t=a._getClearClass(),n.length)return s(n,t),n.attr({title:a.clearButtonTitle}).html(a.clearButton),void(a.$clear=n);a._addContent("clear",'<div class="'+t+'" title="'+a.clearButtonTitle+'">'+a.clearButton+"</div>"),a.$clear=a.$container.find("."+a.clearButtonBaseClass)}},_getClearClass:function(){return this.clearButtonBaseClass+" "+(this.inactive?"":this.clearButtonActiveClass)},_getTouchPosition:function(e){var t=i(e.pageX)?e.originalEvent.touches[0].pageX:e.pageX;return t-this.$rating.offset().left},_toggleHover:function(e){var t,a,n,r=this;e&&(r.hoverChangeStars&&(t=r.getWidthFromValue(r.clearValue),a=e.val<=r.clearValue?t+"%":e.width,r.$filledStars.css("width",a)),r.hoverChangeCaption&&(n=e.val<=r.clearValue?r.fetchCaption(r.clearValue):e.caption,n&&r._setCaption(n+"")))},_init:function(t){var a=this,n=a.$element.addClass("hide");return a.options=t,e.each(t,function(e,t){a[e]=t}),(a.rtl||"rtl"===n.attr("dir"))&&(a.rtl=!0,n.attr("dir","rtl")),a.starClicked=!1,a.clearClicked=!1,a._initSlider(t),a._checkDisabled(),a.displayOnly&&(a.inactive=!0,a.showClear=!1,a.showCaption=!1),a._generateRating(),a._listen(),n.removeClass("rating-loading")},_listen:function(){var t=this,a=t.$element,n=a.closest("form"),r=t.$rating,i=t.$clear;return u(r,"touchstart touchmove touchend",e.proxy(t._initTouch,t)),u(r,"click touchstart",e.proxy(t._starClick,t)),u(r,"mousemove",e.proxy(t._starMouseMove,t)),u(r,"mouseleave",e.proxy(t._starMouseLeave,t)),t.showClear&&i.length&&(u(i,"click touchstart",e.proxy(t._clearClick,t)),u(i,"mousemove",e.proxy(t._clearMouseMove,t)),u(i,"mouseleave",e.proxy(t._clearMouseLeave,t))),n.length&&u(n,"reset",e.proxy(t._resetForm,t)),a},_getStars:function(e){var t,a=this,n='<span class="'+e+'-stars">';for(t=1;t<=a.stars;t++)n+='<span class="star">'+a[e+"Star"]+"</span>";return n+"</span>"},_setStars:function(e){var t=this,a=arguments.length?t.calculate(e):t.calculate(),n=t.$element;return n.val(a.val),t.$filledStars.css("width",a.width),t._setCaption(a.caption),t.cache=a,n},showStars:function(e){var t=this,a=parseFloat(e);return t.$element.val(isNaN(a)?t.clearValue:a),t._setStars()},calculate:function(e){var t=this,a=i(t.$element.val())?0:t.$element.val(),n=arguments.length?t.getValueFromPosition(e):a,r=t.fetchCaption(n),l=t.getWidthFromValue(n);return l+="%",{caption:r,width:l,val:n}},getValueFromPosition:function(e){var t,a,n=this,r=o(n.step),i=n.$rating.width();return a=n.diff*e/(i*n.step),a=n.rtl?Math.floor(a):Math.ceil(a),t=c(parseFloat(n.min+a*n.step),r),t=Math.max(Math.min(t,n.max),n.min),n.rtl?n.max-t:t},getWidthFromValue:function(e){var t,a,n=this,r=n.min,i=n.max,l=n.$emptyStars;return!e||r>=e||r===i?0:(a=l.outerWidth(),t=a?l.width()/a:1,e>=i?100:(e-r)*t*100/(i-r))},fetchCaption:function(e){var t,a,n,r,l,s=this,u=parseFloat(e)||s.clearValue,h=s.starCaptions,d=s.starCaptionClasses;return u&&u!==s.clearValue&&(u=c(u,o(s.step))),r="function"==typeof d?d(u):d[u],n="function"==typeof h?h(u):h[u],a=i(n)?s.defaultCaption.replace(/\{rating}/g,u):n,t=i(r)?s.clearCaptionClass:r,l=u===s.clearValue?s.clearCaption:a,'<span class="'+t+'">'+l+"</span>"},destroy:function(){var t=this,a=t.$element;return i(t.$container)||t.$container.before(a).remove(),e.removeData(a.get(0)),a.off("rating").removeClass("hide")},create:function(e){var t=this,a=e||t.options||{};return t.destroy().rating(a)},clear:function(){var e=this,t='<span class="'+e.clearCaptionClass+'">'+e.clearCaption+"</span>";return e.inactive||e._setCaption(t),e.showStars(e.clearValue).trigger("change").trigger("rating.clear")},reset:function(){var e=this;return e.showStars(e.initialValue).trigger("rating.reset")},update:function(e){var t=this;return arguments.length?t.showStars(e):t.$element},refresh:function(t){var a=this,n=a.$element;return t?a.destroy().rating(e.extend(!0,a.options,t)).trigger("rating.refresh"):n}},e.fn.rating=function(t){var a=Array.apply(null,arguments),n=[];switch(a.shift(),this.each(function(){var r,l=e(this),s=l.data("rating"),o="object"==typeof t&&t,c=o.theme||l.data("theme"),u=o.language||l.data("language")||"en",d={},g={};s||(c&&(d=e.fn.ratingThemes[c]||{}),"en"===u||i(e.fn.ratingLocales[u])||(g=e.fn.ratingLocales[u]),r=e.extend(!0,{},e.fn.rating.defaults,d,e.fn.ratingLocales.en,g,o,l.data()),s=new h(this,r),l.data("rating",s)),"string"==typeof t&&n.push(s[t].apply(s,a))}),n.length){case 0:return this;case 1:return void 0===n[0]?this:n[0];default:return n}},e.fn.rating.defaults={theme:"",language:"en",stars:5,filledStar:'<i class="glyphicon glyphicon-star"></i>',emptyStar:'<i class="glyphicon glyphicon-star-empty"></i>',containerClass:"",size:"md",animate:!0,displayOnly:!1,rtl:!1,showClear:!0,showCaption:!0,starCaptionClasses:{.5:"label label-danger",1:"label label-danger",1.5:"label label-warning",2:"label label-warning",2.5:"label label-info",3:"label label-info",3.5:"label label-primary",4:"label label-primary",4.5:"label label-success",5:"label label-success"},clearButton:'<i class="glyphicon glyphicon-minus-sign"></i>',clearButtonBaseClass:"clear-rating",clearButtonActiveClass:"clear-rating-active",clearCaptionClass:"label label-default",clearValue:null,captionElement:null,clearElement:null,hoverEnabled:!0,hoverChangeCaption:!0,hoverChangeStars:!0,hoverOnClear:!0},e.fn.ratingLocales.en={defaultCaption:"{rating} 分",starCaptions:{.5:"1分",1:"2分",1.5:"3分",2:"4分",2.5:"5分",3:"6分",3.5:"7分",4:"8分",4.5:"9分",5:"满分"},clearButtonTitle:"清除",clearCaption:"未评分"},e.fn.rating.Constructor=h,e(document).ready(function(){var t=e("input.rating");t.length&&t.removeClass("rating-loading").addClass("rating-loading").rating()})});
 /*!
  * Krajee Font Awesome Theme configuration for bootstrap-star-rating.
  * This file must be loaded after 'star-rating.js'.
  *
  * @see http://github.com/kartik-v/bootstrap-star-rating
  * @author Kartik Visweswaran <kartikv2@gmail.com>
  */!function(a){"use strict";a.fn.ratingThemes["krajee-fa"]={filledStar:'<i class="fa fa-star"></i>',emptyStar:'<i class="fa fa-star"></i>',clearButton:'<i class="fa fa-lg fa-minus-circle"></i>'}}(window.jQuery);
  $(function() {
	  $('#kv-fa').rating({
	      theme: 'krajee-fa',
	      //filledStar: '<i class="fa fa-star"></i>',
	      //emptyStar: '<i class="fa fa-star-o"></i>',
	      //readonly: 'true',
	      showClear: false,
	      size: 'xxs',
	      hoverEnabled: 'false',
	      step: '0.5',
	      max: '5',
	      
	  });
	  $('#kv-fa').on('change', function() {  
		  window.selected_rating = $(this).val()*2;
		  console.log('选择评级: ' + selected_rating);
	  });

  });
  
 
 
