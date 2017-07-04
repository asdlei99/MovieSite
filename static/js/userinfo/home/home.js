/**
 * 
 */


function initSpeakReply($target) {
	$target.click(function() {
		$_this = $(this);
		var speakID = $_this.parent().attr('data-sid');
		var $wrap = $_this.parent().parent(); //outer media-body
		//var $replyArea = $wrap.find('.reply-area');
		//生成回复框
		var $ra = $('.reply-area');
		var $_this = $(this);
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
				initSpeakReply($_this);
				$_this.trigger('click');

			});
			//return false;
		} else {
			$('.reply-area, .reply-title').remove();
			var textHtml = '<div class="form-group reply-area submit-area" style="margin:20px 0 0"><div class="input-group">\
			    <textarea class="form-control text-wrapper" placeholder="我也说一句" rows="4" maxlength="200"></textarea></div>\
				<div class="submit-btn-group"><span class="emotion-icon-rr" role="button"><i class="fa fa-smile-o"></i></span>\
				<div class="btn-group"><button class="btn btn-primary btn-sm btn-reply btn-submit">回复</button></div></div></div>';
			$wrap.append(textHtml);
			$box = $wrap.find('.reply-area');  //reply-area
			var $textarea = $wrap.find('.text-wrapper');
			ChangeTextareaState($box, 100);
			$textarea.focus();
			$replyBtn = $wrap.find('.btn-reply');//点击发布
			$replyBtn.click(function() {
				var tip = checkReplyContent($textarea);
				if(tip) {
					showTip(tip, 'warning', $box);
					return;
				}
				var replyContent = $textarea.val();
				var replyContent = replaceWithBr(replyContent);
				var replyContent = AnalyticEmotion(replyContent);
				
				$box.append(loadingCoverHtml);
				$.ajax({
					url: '/user/submit_speak_reply/',
					data: {'content':replyContent, 'sid':speakID},
					type: 'POST',
					complete: function() {
						itemFadeOut($wrap, '.loading-cover');
					},
					success: function(callback) {
						var obj = $.parseJSON(callback);
						var msg = obj.msg;
						if(msg=='success') {
							$speakReplyList = $wrap.find('.speak-reply-list');
							if(!$speakReplyList.length) {  //评论列表不存在先加列表
								var replyListHtml = '<ul class="media-list speak-reply-list"></ul>';
								$_this.parent().after(replyListHtml)
							}
							$replyList = $_this.parent().parent().find('.speak-reply-list');
							var replyHtml = '<li class="media">\
					              <div class="media-left"><a href="/user/profile/' + obj.uid + '/" target="_blank"><img class="avatar-xs img-circle" src="' + obj.uthumb + '"></a></div>\
					              <div class="media-body">\
					                <div class="media-heading text-content"><a class="username mr-10" href="/user/profile/' + obj.uid + '/">' + obj.uname + '</a>: ' + obj.ucontent + '</div>\
					                <div class="media-bottom" data-uid="' + obj.uid + '" data-rid="' + obj.rid + '">\
					                  <time class="mr-20">' + '刚刚' + '</time>\
					                  <a class="btn-reply-r mr-10" role="button" title="回复"><i class="fui-chat"></i></a>\
					                  <a class="btn-del btn-del-reply" role="button" title="删除"><i class="fa fa-trash-o"></i></a></div></div></li>';
							$(replyHtml).hide().appendTo($replyList).fadeIn();
							$textarea.val('');
							$_this.text('评论(' + $replyList.children('.media').length + ')');
							
							var $newReply = $replyList.children('li:last');
							initSpeakRR($newReply.find('.btn-reply-r')); //初始化回复
							delSpeakReply($newReply.find('.btn-del-reply')); //初始化删除
						} else if(msg) {
							var tip = msg+'错误';
							showTip(tip, 'danger' ,$('.reply-area'));
						}
					},
				});
			});
		}
		

	}); //click bind
}

function initSpeakRR($target) {
	$target.click(function() {
		//生成回复框
		var $ra = $('.reply-area');
		var $_this = $(this);
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
				initSpeakRR($_this);
				$_this.trigger('click');

			});
			//return false;
		} else {
			$('.reply-area, .reply-wrapper').remove();
			//var $_this = $(this);
			var textareaHtml = '<div class="form-group reply-area submit-area" style="margin:20px 0 0"><div class="input-group">\
			    <textarea class="form-control text-wrapper" style="border-top:0;border-top-left-radius:0!important;border-top-right-radius:0!important;" rows="3" maxlength="200"></textarea></div>\
				<div class="submit-btn-group"><span class="emotion-icon-rr" role="button"><i class="fa fa-smile-o"></i></span>\
				<div class="btn-group"><button class="btn btn-primary btn-sm btn-reply btn-submit">回复</button></div></div></div>';
			var temp = $_this.parent().prev().html().trim();
			var pat = /^(<a.*?>.*?<\/a>)/;
			var username = pat.exec(temp);
			var toHtml = '<div class="reply-title alert-success">回复 '+username[1]+' :</div>'
			if(typeof($_this.parent().attr('data-rrid')) == 'undefined') {  //对回复进行回复
				$_this.parent().parent().append('<div class="reply-wrapper"></div>');
				$_this.parent().parent().find('.reply-wrapper').append(toHtml).append(textareaHtml);  //添加回复框，同时添加'回复xxx'的标题样式
				$speakRRList = $_this.parent().parent().find('.speak-rr-list');
				if(!$speakRRList.length) {
					$_this.parent().after('<ul class="media-list speak-rr-list"></ul>');
					$speakRRList = $_this.parent().parent().find('.speak-rr-list');
				}
			} else {  //对回复的回复进行回复
				$speakRRList = $_this.parent().parent().parent().parent();
				$speakRRList.after('<div class="reply-wrapper"></div>');
				//$speakRRList.after(textareaHtml).after(toHtml);
				$('.reply-wrapper').append(toHtml).append(textareaHtml);
			}
			$box = $('.reply-wrapper');
			$textarea = $box.find('.text-wrapper');
			ChangeTextareaState($box, 100);
			$replyTitle = $box.find('.reply-title');
			$textarea.focus(function() {
				$replyTitle.css({'border-color':'rgb(26,188,156)'});
			});
			$textarea.blur(function() {
				$replyTitle.css({'border-color':'rgb(189,195,199)'});
			});
			$textarea.focus();

			//绑定回复
			var $submitRRBtn = $speakRRList.parent().find('.btn-reply');
			$submitRRBtn.click(function() {
				if(typeof($_this.parent().attr('data-rrid')) == 'undefined') {
					var rrid = null;
				} else {
					var rrid = $_this.parent().attr('data-rrid');
				}
				var rid = $_this.parent().attr('data-rid');
				var targetUid = $_this.parent().attr('data-uid');
				var tip = checkReplyContent($textarea);
				if(tip) {
					showTip(tip, 'warning' ,$box);
					$textarea.focus();
					return false;
				}
				
				$(this).parent().parent().parent().append(loadingCoverHtml);
				var rrContent = $textarea.val();
				var rrContent = replaceWithBr(rrContent);
				var rrContent = AnalyticEmotion(rrContent);
				$.ajax({
					url: '/user/submit_speak_rr/',
					data: {'rid':rid, 'target_uid':targetUid, 'content':rrContent},
					type: 'POST',
					success: function(callback) {
						var obj = $.parseJSON(callback);
						if(obj.msg == 'success') {
							if(obj.uid == targetUid) {
								var headingHtml = '<a class="username" href="/user/profile/' + obj.uid + '/">' + obj.uname + '</a>&nbsp;:&nbsp;';
							} else {
								var headingHtml = '<a class="username" href="/user/profile/' + obj.uid + '/">' + obj.uname + 
								'</a>&nbsp;回复&nbsp;<a class="username" href="/user/profile/' + targetUid + '/">' + obj.target_uname + '</a>&nbsp;:&nbsp;';
							}
							var rrHtml = '<li class="media">\
								<div class="media-left"><a href="/user/profile/' + obj.uid + '/" target="_blank"><img class="avatar-xs img-circle" src="' + obj.uthumb + '"></a></div>\
								<div class="media-body">\
								  <div class="media-heading text-content">' + headingHtml + obj.rr_content + '</div>\
								  <div class="media-bottom" data-uid="' + obj.uid + '" data-rrid="' + obj.rrid + '" data-rid="' + rid + '">\
									<time class="mr-20">' + '刚刚' + '</time>\
									<a class="btn-reply-r mr-10" role="button" title="回复"><i class="fui-chat"></i></a>\
									<a class="btn-del btn-del-rr" role="button" title="删除"><i class="fa fa-trash-o"></i></a>\
								  </div></div></li>';
							$(rrHtml).hide().appendTo($speakRRList).fadeIn();
							$textarea.val('');
							var $newRR = $speakRRList.children('li:last');
							initSpeakRR($newRR.find('.btn-reply-r')); //初始化回复
							delSpeakRR($newRR.find('.btn-del-rr')); //初始化删除
							
						} else {
							showTip(obj.msg+'错误', 'danger' ,$('.reply-area'));
						}
						$('.loading-cover').fadeOut().remove();
						$textarea.focus();
					},
				});
			});
			
		}
	});
}

function delSpeak($target) {
	$target.click(function() {
		var $_this = $(this);
		var sid = $_this.parent().attr('data-sid');
		if(sid) {
			$modal = $('#deleteConfirmModal');
			var tipHtml = '<div class="media"><div class="media-left"><div class="ccs-tip ccs-tip-warning"></div></div><div class="media-body media-middle"><div class="ccs-desc">此说说下的回复也会同步删除哦~</div></div></div>';
			$modalBody = $modal.find('.modal-body');
			$modalBody.find('.media').remove();
			$modalBody.prepend(tipHtml);
			$modal.find('h4').html('确认删除说说');
			$modal.modal();
			$('#cancel-delete').unbind();
			$('#cancel-delete').click(function() {
				$modal.modal('hide');
			});
			$('#confirm-delete').unbind();
			var $wrap = $_this.parent().parent().parent();
			$('#confirm-delete').click(function() {
				$modal.modal('hide');
				$wrap.prepend(loadingCoverHtml);
				$.ajax({
					url: '/user/delete_speak/',
					type: 'POST',
					data: {'sid': sid},
					complete: function() {
						itemFadeOut($wrap, '.loading-cover');
					},
					success: function(callback) {
						var obj = $.parseJSON(callback);
						if(obj.msg=='success') {
							itemFadeOut($wrap, 'item_self');
						} else {
							showTip('错误'+obj.msg, 'danger', $wrap);
						}
					}
				});
				$('#confirm-delete').unbind();
			});
		}
	});
}

function delSpeakReply($target) {
	//回复(评论)的删除
	$target.click(function() {
		var $_this = $(this);
		var rid = $_this.parent().attr('data-rid');
		if(rid) {
			$modal = $('#deleteConfirmModal');
			var tipHtml = '<div class="media"><div class="media-left"><div class="ccs-tip ccs-tip-warning"></div></div><div class="media-body media-middle"><div class="ccs-desc">此评论下的回复也会同步删除哦~</div></div></div>';
			$modalBody = $modal.find('.modal-body');
			$modalBody.find('.media').remove();
			if($_this.parent().parent().find('.media').length) {
				$modalBody.prepend(tipHtml);
			}

			$modal.find('h4').html('确认删除评论');
			$modal.modal();
			
			$('#cancel-delete').unbind();
			$('#cancel-delete').click(function() {
				$modal.modal('hide');
			});
			$('#confirm-delete').unbind();
			var $wrap = $_this.parent().parent().parent();
			$('#confirm-delete').click(function() {
				$modal.modal('hide');
				$wrap.prepend(loadingCoverHtml);
				$.ajax({
					url: '/user/delete_speak_reply/',
					type: 'POST',
					data: {'rid': rid},
					complete: function() {
						itemFadeOut($wrap, '.loading-cover');
					},
					success: function(callback) {
						var obj = $.parseJSON(callback);
						if(obj.msg=='success') {
							rBtn = $_this.parent().parent().parent().parent().parent().find('.btn-speak-reply');
							rBtnText = rBtn.text();
							rNumb = /\d+/.exec(rBtnText)[0];
							if(rNumb > 1) {
								newText = rBtnText.replace(rNumb, parseInt(rNumb)-1);
							} else {
								newText = '评论';
							}
							
							rBtn.text(newText);
							itemFadeOut($wrap, 'item_self');
							
						} else {
							showTip('错误'+obj.msg, 'danger', $wrap);
						}
						
					}
				});
				$('#confirm-delete').unbind();
			});
		}
	});
}

function delSpeakRR($target) {
	//回复的回复删除
	$target.click(function() {
		var $_this = $(this);
		var rrid = $_this.parent().attr('data-rrid');
		var $wrap = $_this.parent().parent().parent(); //media
		if(rrid) {
			$modal = $('#deleteConfirmModal');
			$modalBody = $modal.find('.modal-body');
			$modalBody.find('.media').remove();
			$modal.find('h4').html('确认删除回复');
			$modal.modal();

			$('#cancel-delete').click(function() {
				$modal.modal('hide');
			});
			$('#confirm-delete').unbind();
			$('#confirm-delete').click(function() {
				$modal.modal('hide');
				$wrap.prepend(loadingCoverHtml);
				$.ajax({
					url: '/user/delete_speak_rr/',
					type: 'POST',
					data: {'rrid': rrid},
					complete: function() {
						itemFadeOut($wrap, '.loading-cover');
					},
					success: function(callback) {
						var obj = $.parseJSON(callback);
						if(obj.msg=='success') {
							itemFadeOut($wrap, 'item_self');
						} else {
							showTip('错误'+obj.msg, 'danger', $wrap);
						}
					}
				});
				$('#confirm-delete').unbind();
			});
		} else {
			showTip('未知错误，请刷新页面', 'danger', $wrap);
		}
	});
}

function initLike($target) {
	$target.click(function() {
		$_this = $(this);
		var text = $_this.text();
		//$_this.html('<i class="fa fa-circle-o-notch fa-spin"></i>');
		var sid = $_this.parent().attr('data-sid');
		$.ajax({
			url: '/user/like_speak/',
			data: {'sid':sid},
			type: 'POST',
			success: function(callback) {
				var obj = $.parseJSON(callback);
				if(obj.msg == 'success') {
					$_this.html('赞('+ obj.counts + ')');
				} else if(obj.msg == '910') {
					$_this.text(text);
					$('.btn-speak-like').tooltip('destroy');
					$_this.attr({'data-toggle':'tooltip','data-trigger':'click', 'data-placement':'left', 'data-original-title':'你已经赞过这条说说啦'});
					$_this.tooltip('show');
					setTimeout(function() {
						$_this.tooltip('hide');
					}, 800);
				} else {
					$_this.text(text);
					showTip('错误'+obj.msg, 'danger', $_this.parent());
				}
			}
		});
	});
}

$(function() {
	if($('#speak').length>0) {
		//light box
		$('.msg-img-wrap .gallery-img').click(function (e) {
		    e.preventDefault();
		    $(this).ekkoLightbox({
		    	'loadingMessage': '<div class="well text-center"><i class="fa fa-spinner fa-spin"></i> 图片加载中……</div>'
		    });
		});
		
		//scroll
		$('#speak').infinitescroll({
		    navSelector  : '#next-page',            
		    nextSelector : '#next-page>a',    
		    itemSelector : '#speak > .speak-item',
		    //animate: true,
		    loading: {
		        finished: undefined,
		        finishedMsg: '<div class="well text-center">好厉害，已经全部加载完了呢！</div>',
		        img: '/static/images/common/loading/ajax-spinner.gif',
		        msg: null,
		        msgText: '<div style="margin-top:5px;color:#888;">加载中 ...</div>',
		        selector: null,
		        speed: 'fast',
		        start: undefined
		    },
		},
		function(newadd) {
			initSpeakReply($(newadd).find('.btn-speak-reply'));
			initSpeakRR($(newadd).find('.btn-reply-r'));
			delSpeak($(newadd).find('.btn-del-speak'));
			delSpeakReply($(newadd).find('.btn-del-reply'));
			delSpeakRR($(newadd).find('.btn-del-rr'));
			initLike($(newadd).find('.btn-speak-like'));
		});
		
		//模态发送消息和关注
		var $msgModal = $('#sendMsgModal');
		var $msgTextarea = $msgModal.find('.text-wrapper');
		ChangeTextareaState($msgModal, 250);
		$msgModal.on('shown.bs.modal', function () {
			$msgTextarea.focus()
		});
		var $btnFocus = $('.btn-focus');
		var $btnMsg = $('.btn-msg');
		$btnMsg.unbind('click');
		$btnMsg.click(function() {
			var loginRes = checkLogin();
			if(!loginRes) {
				return false;
			}
			var uid = $(this).attr('data-uid');
			$('.modal').modal('hide');

			$msgModal.modal();
			var un = $(this).parent().parent().find('.username').text();
			if(!un) {un = '空间主人'}
			$msgModal.find('.modal-title').html('To: '+un);
			
			var $btnSubmit = $msgModal.find('.btn-submit');
			$btnSubmit.unbind('click');
			$btnSubmit.click(function() {  //绑定发送
				var $_this = $(this);
				var $area = $('.send-msg-area');
				var tip = checkReplyContent($msgTextarea);
				if(tip) {
					showTip(tip, 'warning', $area);
					$text.focus();
					return false;
				}
				var content = $msgTextarea.val();
				var content = replaceWithBr(content);
				var content = AnalyticEmotion(content);
				$area.prepend(loadingCoverHtml);
				$.ajax({
					url: '/user/send_message/',
					data: {'content': content, 'receiver_id': uid},
					type: 'POST',
					success: function(callback) {
						$('.loading-cover').fadeOut().remove();
						var obj = $.parseJSON(callback);
						if(obj.msg=='success') {
							$msgTextarea.val('');
							showTip('发送成功', 'success', $area);
							
						} else {
							showTip('错误'+obj.msg, 'danger', $area);
						}
					}
				});
			});
		});

		$btnFocus.click(function() {
			var loginRes = checkLogin();
			if(!loginRes) {
				return false;
			}
			$_this = $(this);
			var originHtml = $_this.html();
			$_this.html('<i class="fa fa-circle-o-notch fa-spin"></i> ...');
			$_this.attr('disabled',true);
			var uid = $_this.attr('data-uid');
			$.ajax({
				url: '/user/focus/',
				data: {'target_uid':uid},
				type: 'POST',
				complete: function() {
					$_this.removeAttr('disabled');
				},
				success: function(callback) {
					var obj = $.parseJSON(callback);
					var msg = obj.msg;
					if(msg=='success') {
						$_this.html('已粉');
						var content = '关注成功'
					} else if(msg=='cancel_success') {
						$_this.html('关注');
						var content = '取消关注成功'
					} else {
						if(msg=='911') {
							var content = '自己不能关注自己';
						} else if(msg=='402') {
							var content = '对方设置了不允许任何人关注';
						} else {
							var content = msg+'错误';
						}
						$_this.html(originHtml);
					}
					$('.tooltip').tooltip('destroy');
					$_this.attr({'data-toggle':'tooltip',
						'data-trigger':'click',
						'data-placement':'top',
						'data-container':'body',
						'data-original-title':content});
					$_this.tooltip('show');
					st = window.setTimeout(function() {
						$_this.tooltip('destroy');
					}, 1000);
				},
			});
		});

		
		//图片上传
		var $pt = $('.publish-area');
		var $text = $('.publish-area .text-wrapper');
		var $speakPubBtn = $('#btn-publish');
		
		$pt.find('.btn-photo').click(function() {
			$('#fine-uploader-gallery').removeClass('hidden');
			$('.qq-upload-button > input').trigger('click');
		});
		window.firstUpload = true;
		var galleryUploader = new qq.FineUploader({
	        element: document.getElementById('fine-uploader-gallery'),
	        template: 'qq-template-gallery',
	        request: {
	            endpoint: '/user/upload_speak_img/'
	        },
	        deleteFile: {
	            enabled: true,
	            forceConfirm: true,
	            method: 'POST',
	            endpoint: '/user/delete_speak_img/'
	        },
	        thumbnails: {
	            placeholders: {
	                waitingPath: '/static/css/plugs/fineuploader/placeholders/waiting-generic.png',
	                notAvailablePath: '/static/css/plugs/fineuploader/placeholders/not_available-generic.png'
	            }
	        },
	        validation: {
	            allowedExtensions: ['jpeg', 'jpg', 'png'],
	        	sizeLimit: 5120000, // 5M
	        	itemLimit: 9,
	        },
	        failedUploadTextDisplay: {
	            mode: 'custom'
	        },
	        messages: {
	        	emptyError: "图片{file}是空的，请重新选择一个。",
	            noFilesError: "没有选择任何图片。",
	        	typeError: "{file}的后缀名不可用，可用后缀如下：{extensions}。",
	        	tooManyItemsError: "每次只能上传{itemLimit}张图片。",  //你选择了 {netItems} 张图片，请重新选择。
	            minHeightImageError: "图片高度不够（最小宽度1920，最小高度1080）。",
	            minWidthImageError: "图片宽度不够（最小宽度1920，最小高度1080）。",
	            onLeave: "图片正在上传中，现在离开的话上传会中断哦。",
	        },
	        text: {
	            defaultResponseError: "未知原因，上传失败",
	            fileInputTitle: "选择文件",
	            sizeSymbols: [ "kB", "MB", "GB", "TB", "PB", "EB" ]
	        },
	        
	        autoUpload: true,
	        debug: false,
	        
	    });
		
		//说说回复
		initSpeakReply($('.btn-speak-reply'));
		//说说回复的回复
		initSpeakRR($('.btn-reply-r'));
		//说说删除
		delSpeak($('.btn-del-speak'));
		//回复删除
		delSpeakReply($('.btn-del-reply'));
		//回复的回复删除
		delSpeakRR($('.btn-del-rr'));
		initLike($('.btn-speak-like'));
	    
		//发布说说
		$speakPubBtn.bind('click', function() {
			$wrap = $('.publish-area');
			$wrap.prepend(loadingCoverHtml);
			var speakContent = $text.val();
			var speakContent = replaceWithBr(speakContent);
			var speakContent = AnalyticEmotion(speakContent);
			$.ajax({
				url: '/user/publish_speak/',
				type: 'POST',
				data: {'content': speakContent},
				success: function(callback) {
					itemFadeOut($wrap, '.loading-cover');
					var obj = $.parseJSON(callback);
					if(obj.msg=='901') {
						var tip = '请输入内容';
						showTip(tip, 'warning', $wrap);
					} else if(obj.msg=='success') {
						$wrap.find('.text-wrapper').val('');
						$speakPubBtn.unbind('click');
						window.location.reload();
					} else {
						var tip = obj.msg + '错误';
						showTip(tip, 'danger', $wrap);
					}
				}
			});
		});
		
		
		$text.focus(function() {
			$text.css({'height':'120px','border-bottom':'none'});
			$text.next().remove();
			$text.parent().css('width','100%');
			$pt.find('.publish-btn-group').removeClass('hidden');
		});
		$text.next().children('button').click(function() {
			$text.trigger('focus');
			$('#fine-uploader-gallery').removeClass('hidden');
			$('.qq-upload-button > input').trigger('click');
		});
		
		
		ChangeTextareaState($('.publish-area'), 250)
	}
	
	/*
	 * messages
	 */
	if($('#messages').length>0) {
		var $msgList = $('#messages > .message-list');
		var $msgListTitle = $('#message-list-title')
		var $msgItem = $msgList.children('a.list-group-item');
		var $msgMenu = $('#message-menu');
		var $sendmsgArea = $('#messages .sendmsg-area');
		ChangeTextareaState($sendmsgArea, 250);
		//点击打开私信详情
		$msgItem.click(function() {
			$sendmsgArea.find('.btn-sendmsg').unbind('click');  //取消之前绑定
			var $msgLoadMore = $('#messages .load-more>small');
			$msgList.addClass('hidden');
			$msgListTitle.addClass('hidden');
			var $_this = $(this);
			var msgID = $_this.attr('data-msgid');
			var targetID = 'md'+ msgID;
			
			$('#messages').children('#'+targetID).removeClass('hidden');
			$sendmsgArea.removeClass('hidden');
			$msgMenu.removeClass('hidden');
			
			$badge = $_this.find('span.badge');
			if($badge.length) {
				$badge.remove();//移除新消息数目，应该有ajax请求
				$.ajax({
					url: '/user/home/messages/remove_badge/',
					data: {'msg_id':msgID},
					type: 'POST'
				});
			}
			
			var $textarea = $sendmsgArea.find('.text-wrapper')
			$textarea.focus();
			
			var $curMsg = $('#messages>.message-item:not(.hidden)');  //滚动窗口
			
			var $wrapper = $curMsg.children('.media-list');
			$curMsg.scrollTop($wrapper.height());
			//绑定回复
			$sendmsgArea.find('.btn-sendmsg').click(function() {

				var tip = checkReplyContent($textarea);
				if(tip) {
					showTip(tip, 'warning', $sendmsgArea);
					return false;
				}
				$_this = $(this);
				$sendmsgArea.prepend(loadingCoverHtml);
				var content = $textarea.val();
				var content = replaceWithBr(content);
				var content = AnalyticEmotion(content);
				if($curMsg.length==1) {
					var curID = $curMsg.attr('id').replace('md','');
				} else {
					var curID = null;
					showTip('Wrong MsgID', 'danger', $sendmsgArea);
				}
				$.ajax({
					url: '/user/send_message/',
					type: 'POST',
					data: {'content': content, 'msg_id': curID},
					success: function(callback) {
						itemFadeOut($sendmsgArea, '.loading-cover');
						var obj = $.parseJSON(callback);
						if(obj.msg=='901') {
							var tip = '请输入内容';
							showTip(tip, 'warning', $sendmsgArea);
						} else if(obj.msg=='success') {
							$textarea.val('');
							
							var msgHtml = '<div class="media">\
								<div class="media-left"><div class="avatar-s"></div></div>\
								<div class="media-body"><div class="bubble bubble-dark">' + content + '</div></div>\
								<div class="media-right"><a href="/user/profile/' + obj.receiver_id + '/"><img class="media-object img-circle avatar-s" src="' + obj.thumb_s + '"></a></div>\
								<time class="text-right pt-10 btn-block">' + obj.reply_date + '</time></div>'
							$(msgHtml).hide().appendTo($wrapper).fadeIn();
							$curMsg.animate({scrollTop: $wrapper.height()}, 800);
						} else {
							var tip = obj.msg + '错误';
							showTip(tip, 'danger', $sendmsgArea);
						}
					}
				});
			});
			
			//加载更多
			if($msgLoadMore.length>0) {
				$msgLoadMore.unbind('click');
				$msgLoadMore.click(function() {
					var $_this = $(this);
					$_this.parent().append(loadingCoverHtml);
					$_this.hide();
					var targetID = $_this.parent().parent().parent().attr('id').replace('md','');
					var loadedItemCounts = $_this.parent().parent().children('.media').length;
					$.ajax({
						url: '/user/home/get_more_msg/',
						data: {'msg_id':targetID, 'loaded_counts':loadedItemCounts},
						type: 'POST',
						success: function(callback) {
							$_this.parent().children('.loading-cover').remove();
							$_this.show();
							var obj = $.parseJSON(callback);
							var remainder = obj[0];
							if(remainder<=0) {
								$_this.parent().remove();
							}
							var previousHeight = $wrapper.height();
							$.each(obj, function(i) {
								if(!i==0) {
									if(this.cur_uid == this.receiver_id) {
										var itemHtml = '<div class="media">\
											<div class="media-left"><a href="/user/profile/' + this.sender_id + '/"><img class="media-object img-circle avatar-s" src="' + this.sender_thumb_s + '"></a></div>\
											<div class="media-body">\<div class="bubble bubble-light">' + this.content + '</div></div>\
											<div class="media-right"><div class="avatar-s"></div></div>\
											<time class="text-left pt-10 btn-block">' + this.create_date + '</time></div>'
									} else if(this.cur_uid == this.sender_id) {
										var itemHtml = '<div class="media">\
											<div class="media-left"><div class="avatar-s"></div></div>\
											<div class="media-body"><div class="bubble bubble-dark">' + this.content + '</div></div>\
											<div class="media-right"><a href="/user/profile/' + this.sender_id + '/"><img class="media-object img-circle avatar-s" src="' + this.sender_thumb_s + '"></a></div>\
											<time class="text-right pt-10 btn-block">' + this.create_date + '</time></div>'
									}
									
									$(itemHtml).hide().prependTo($wrapper).fadeIn();
								}
							});
							$curMsg.scrollTop($wrapper.height() - previousHeight - 200)
						},
					});
				});
			}
			
		});
		
		//返回私信列表
		var $backBtn = $('#back-to-message-list');
		$backBtn.click(function() {
			$msgMenu.addClass('hidden');
			$sendmsgArea.addClass('hidden');
			$('#messages').children('.message-item').addClass('hidden');
			$msgList.removeClass('hidden');
			$msgListTitle.removeClass('hidden');
		});
		
	}

	/*
	 * notification
	 */
	if($('#notice-list').length>0) {
		$noticeWrap = $('#notice-list');
		$noticeWrap.infinitescroll({
		    navSelector  : '#next-page',          
		    nextSelector : '#next-page>a',    
		    itemSelector : '#notice-list > .list-group-item',
		    //animate: true,
		    loading: {
		        finished: undefined,
		        finishedMsg: '<div class="well text-center">好厉害，已经全部加载完了呢！</div>',
		        img: '/static/images/common/loading/ajax-spinner.gif',
		        msg: null,
		        msgText: '<div style="margin-top:5px;color:#888;">加载中 ...</div>',
		        selector: null,
		        speed: 'fast',
		        start: undefined
		    },
		});
	}

	
});