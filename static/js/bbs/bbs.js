/*
 * COMMON
 */

window.firstInitPa = true;
function checkLoginForNote() {
	$logined_cookie = $.cookie('logined');
	if(!$logined_cookie) {  //cookie不存在
		$.ajax({
			url: '/user/reply_check_login/',
			type: 'POST',
			success: function(callback) {
				obj = $.parseJSON(callback);
				if(!obj.logined) {
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
			return false;
		} else {
			return true;
		}
	}
}


$(function() {
	if($('#newpost-title').length) {
		$('#newpost-title').bind('click', function() {
			if(!checkLogin()) {
				return false;
			}
		});
	}
		
	//summernote初始化
	if($('#summernote').length>0 || $('#summernote-board').length>0) {
		if($('#summernote').length>0) {
			var $summernote = $('#summernote');  //回帖
			var submit_url = '/bbs/submit_reply/';
			$('#op .btn-r').click(function(event) {
				$summernote.summernote('focus');
				$('html,body').animate({scrollTop:$('#publish-reply').offset().top},500);
				event.preventDefault();
			});
			
		} else if ($('#summernote-board').length>0) {  //发帖
			var $summernote = $('#summernote-board');
			var submit_url = '/bbs/submit_post/';
			var $postTitle = $('#newpost-title');
			var $titlePH = $('.newpost-title-placeholder');
			var $title = $postTitle;
			$postTitle.focus(function() {
				$(this).css('border-color','#1abc9c');
			});
			$postTitle.blur(function() {
				$(this).css('border-color','#a9a9a9');
			});
			$titlePH.click(function() {
				$('#newpost-title').focus();
			});
			$postTitle.bind('input propertychange', function() {
				if($(this).val().length>0) {
					$titlePH.addClass('hidden');
				} else {
					$titlePH.removeClass('hidden');
				}
			});
			
			
		}
		$summernote.summernote(
	        {
	    	    lang: 'zh-CN',
	    	    placeholder: '说点什么吧',
	    	    height: '150',
	    	    toolbar: [
	                ['insert', ['picture','link','video']],
	                ['misc', ['fullscreen']]
	    	    ],
	    	    callbacks: {
	    	        onImageUpload: function(files) {
	    	        	$.each(files, function() {
	    	        		sendFile(this);
	    	        	});
	    	        },
	    	        onInit: function() {
	    	        	$summernote.on('summernote.init', function() {
    	        			if(!checkLoginForNote()) {
    	        				$('.note-toolbar button').attr('disabled', true);
    	        				return false;
    	        			}
	    	        		
	    	        	});
	    	        },
	    	        onFocus: function() {
	    	        	$('.note-editor.note-frame').css('border-color','#1abc9c');
	    	        	if(!checkLogin()) {
	    	    			return false;
	    	    		}
	    	        },
	    	        onBlur: function() {
	    	        	$('.note-editor.note-frame').css('border-color','#a9a9a9');
	    	        },
	    	        onPaste: function (e) {
	    	            
	    	            var bufferText = ((e.originalEvent || e).clipboardData || window.clipboardData).getData('Text');
	    	            e.preventDefault();
	    	            setTimeout( function(){
	    	                document.execCommand( 'insertText', false, bufferText );
	    	            }, 10 );
	    	            
	    	        },
	    	    }
	        }
	    );

		/*$summernote.on('summernote.focus', function() {
	    });*/
		function sendFile(file) {
		    data = new FormData();  
		    data.append("file", file);  
		    $.ajax({  
		        data: data,  
		        type: "POST",  
		        url: '/bbs/upload_img/',  
		        cache: false,  
		        contentType: false,  
		        processData: false,  
		        success: function(url) {
		        	$summernote.summernote('insertImage', url);
		        }  
		    });  
		} 
		
		
		$publishBtn = $('.btn-publish');
		$publishBtn.bind('click submit', function() {
			$('.publish').prepend(loadingCoverHtml);
			//$editFrame = $('.note-editor.note-frame');
			$publishReplyFrame = $('#publish-reply');
			$_this = $(this);
			if ($summernote.summernote('isEmpty')) {
				$summernote.summernote('focus');
				console.log('123')
				showTip('请输入要发表的内容', 'warning', $('.text-wrapper'));
		    } else {  //内容不为空
		    	var htmlContent = $('.note-editable').html();
		    	console.log(htmlContent);
		    	console.log($('#summernote').summernote('code'));
		    	if($('#summernote').length>0) {
		    		$publishReplyFrame.prepend(loadingCoverHtml);
		    		var pid = $_this.attr('id').replace('p','');
		    		
			    	$.ajax({
			    		url: submit_url,
			    		data: {'html_content': htmlContent, 'pid':pid},
			    		type: 'POST',
			    		success: function(callback) {
			    			$publishReplyFrame.find('.loading-cover').remove();
			    			var obj = $.parseJSON(callback);
			    			if(obj.msg) {
			    				if(obj.msg=='success') {
			    					window.location.reload();
			    				} else {
			    					var content = '错误' + obj.msg;
			    					showTip(content, 'danger', $publishReplyFrame);
			    				}
			    			}
			    			
			    		}
			    	});
		    	} else if ($('#summernote-board').length>0) {
		    		var $publishPostFrame = $('#publish-post');
		    		var result = /^\s+$/.test($title.val());
			    	if(result) {
			    		showTip('标题不能全为空格', 'warning', $publishReplyFrame);
			    		$title.focus();
			    		return false;
			    	}
			    	if(!$title.val()) {
			    		showTip('请填写标题内容', 'warning', $publishReplyFrame);
			    		$title.focus();
			    		return false;
			    	}
			    	$publishPostFrame.prepend(loadingCoverHtml);
		    		var cur_url = window.location.href;
		    		var board = /.*?\?b=(\w+)/.exec(cur_url);
		    		$.ajax({
			    		url: submit_url,
			    		data: {'html_content': htmlContent, 'title':$title.val(), 'board':board[1]},
			    		type: 'POST',
			    		success: function(callback) {
			    			$publishPostFrame.find('.loading-cover').remove();
			    			var obj = $.parseJSON(callback);
			    			if(obj.msg) {
			    				if(obj.msg=='success') {
			    					window.location.reload();
			    				} else {
			    					var content = '错误' + obj.msg;
			    					showTip(content, 'danger', $publishReplyFrame);
			    				}
			    			}
			    			
			    		}
			    	});
		    	}
		    	
		    }
			
		});
	}
});



/*
 *  BBS POST DETAIL
 */

function initLayerPa($paWrap, action) { //initialize pagination and bind click
	$.each($paWrap, function() {
		var $_this = $(this);  //.layer-pagination
		var $wrap = $_this.parent();  //.layer-reply-wrap

		var itemsPerPage = 5;
		//var $allItems = $wrap.children('.media');
		var len = parseInt($_this.attr('data-len'));  //在增加和删除的函数中已经改变
		console.log('len: ' + len)
		var prid = parseInt($_this.attr('data-prid'));
		console.log('prid: ' + prid)
		var pages = Math.ceil(len / itemsPerPage);
		if(action=='default') {  //add,delete
			console.log('action: default');
			sPage = 1;
		} else {
			console.log('other_action: ' + action)
			
			//$_this.twbsPagination('destory');
			if(action=='del') {
				console.log('del...')
				var sPage = parseInt($_this.find('li.active').children('a').text());
				console.log('len/5: '+len/5)
				if(/^\d+$/.test(len/5) && len>0) {  //如果len为5的倍数
					sPage = len/5;
				} else if(len==0) {  //如果len为0，清空
					//$wrap.remove();
					itemSlideUp($wrap, 'item_self')
					return;
				}
				
				console.log('sPage: ' + sPage)
				
			} else if(action=='add') {
				console.log('add...')
				var sPage = pages;
			}
			$_this.empty();
			$_this.removeData("twbs-pagination");
			$_this.unbind('page');
		}
		
		$_this.twbsPagination({
		    totalPages: pages,
		    startPage: sPage,
		    visiblePages: 7,
		    //hideOnlyOnePage: true,
		    //initiateStartPageClick: false,
		    first: '首页',
		    last: '尾页',
		    prev: '上一页',
		    next: '下一页',
		    paginationClass: 'pagination-simple',
		    onPageClick: function (event, page) {
		    	if(!firstInitPa) {
		    		
		    		//$wrap.append(loadingCoverHtml);
		    		$.ajax({
			    		url: '/bbs/get_layer_reply_items/',
			    		data: {'page':page, 'items_per_page':itemsPerPage, 'prid':prid},
			    		type: 'POST',
			    		success: function(callback) {
			    			//itemFadeOut($_this.parent(), '.loading-cover');
			    			var obj = $.parseJSON(callback);
			    			$wrap.children('.media').remove();
			    			console.log(obj)
			    			$.each(obj, function() {
			    				if(this.focused==2) { //如果是自己
			    					var rrBottomBtnHtml = '<div class="rr-bottom" data-prid="' + prid + '" data-uid="' + this.user_id + '" data-lrid="' + this.id + '"><a class="btn-del del-lr" role="button">删除</a>&nbsp;&nbsp;<time>' + this.create_date + '</time></div>';
			    				} else {
			    					var rrBottomBtnHtml = '<div class="rr-bottom" data-prid="' + prid + '" data-uid="' + this.user_id + '" data-lrid="' + this.id + '"><time>' + this.create_date + '</time>&nbsp;&nbsp;<a class="btn-lr" role="button">回复</a></div>';
			    				}
			    				if(this.user_id==this.target_user_id) {
			    					var rtHtml = '';
			    				} else {
			    					var rtHtml = '&nbsp;回复&nbsp;<a class="username" href="/user/profile/' + this.target_user_id + '/" target="_blank">' + this.target_uname + '</a>';
			    				}
			    				var itemHtml = '<div class="media"><div class="media-left">\
			                        <a class="username" href="/user/profile/' + this.user_id + '/" data-uname="' + this.uname + '" data-uid="' + this.user_id + '" data-ulevel="' + this.ulevel + '" data-posted-counts="' + this.posted_counts + '" data-fans-counts="' + this.fans_counts + '" data-usign="' + this.usign + '" data-focused="' + this.focused + '" data-bg="' + this.ubg + '" data-avatar="' + this.uthumb_l + '" data-toggle="popover" data-placement="top" data-original-title="" title=""><img class="media-object avatar-xs" src="' + this.uthumb_s + '" alt="avatar"></a></div>\
			                        <div class="media-body"><div class="media-heading lr-content">\
			                        <a class="username" href="/user/profile/' + this.user_id + '/" target="_blank">' + this.uname + '</a>' + rtHtml + '&nbsp;:&nbsp;' + this.content + '</div>'
			                        + rrBottomBtnHtml + '</div>';

			    				$_this.before($(itemHtml)); //隐藏加载
			    			});
			    			
			    			var newPop = $wrap.find('[data-toggle=popover]');
			    			initUserCard(newPop); //初始化用户卡
			    			layerReplyDel($wrap.find('.del-lr')); //初始化删除
			    			initLayerRR($wrap.find('.btn-lr'));
			    			//滚动到锚点
			    			if(action=='default') {
			    				$("html,body").stop(true);
				    			$("html,body").animate({scrollTop: $wrap.offset().top -100}, 0);
			    			}
			    			
			    		}
			    	});
		    	}
	    		

		    	//$allItems.addClass('hidden');
		    	//window.cur_page = page;
		    	if(page==1) {
		    		$_this.find('li.first').hide();
		    		$_this.find('li.prev').hide();
		    	} else if(page==pages) {
		    		$_this.find('li.last').hide();
		    		$_this.find('li.next').hide();
		    	}
		    	
		    	
		    }
		});
		if(len<=itemsPerPage) {
			$_this.hide();
		} else {
			$_this.show();
		}
	});
	
	window.firstInitPa = false;
	
}

function initLayerReply($target) {
	
	$target.click(function() {
		console.log('initLayerReply')
		$_this = $(this);
		var prid = $_this.parent().attr('data-prid');
		var targetUID = $_this.parent().attr('data-uid');
		var $wrap = $_this.parent().parent(); //outer media-body
		//生成回复框
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
				initLayerReply($_this);
				$_this.trigger('click');
			});

		} else {
			$('.reply-area, .reply-wrapper').remove();  //移除已存在回复区域
			var textHtml = '<div class="form-group reply-area submit-area" style="margin:20px 0 0"><div class="input-group">\
			    <textarea class="form-control text-wrapper" placeholder="我也说一句" rows="4" maxlength="200"></textarea></div>\
				<div class="submit-btn-group"><span class="emotion-icon-rr" role="button"><i class="fa fa-smile-o"></i></span>\
				<div class="btn-group"><button class="btn btn-primary btn-sm btn-reply btn-submit">回复</button></div></div></div>';
			
			var $lrWrap = $wrap.find('.layer-reply-wrap');
			if($lrWrap.length==0) {  //分页wrap不存在则先创建
				var rrWrapHtml = '<div class="layer-reply-wrap panel-body"><div class="layer-pagination" data-prid="' + $_this.parent().attr('data-prid') + '" data-len="0"></div></div>';
				$wrap.find('.layer-bottom').after(rrWrapHtml);
				$lrWrap = $wrap.find('.layer-reply-wrap');
			}
			
			$wrap.find('.layer-reply-wrap').append(textHtml);
			console.log($wrap.find('.layer-reply-wrap').length)
			console.log('APPENDTEXT')
			$box = $wrap.find('.reply-area');  //reply-area
			ChangeTextareaState($box, 100);
			var $textarea = $wrap.find('.text-wrapper');
			$textarea.focus();
			$replyBtn = $wrap.find('.btn-reply');//点击发布
			$replyBtn.click(function() {
				var tip = checkReplyContent($textarea);
				console.log('submitting...')
				if(tip) {
					showTip(tip, 'warning', $box);
					return;
				}
				var replyContent = $textarea.val();
				var replyContent = replaceWithBr(replyContent);
				var replyContent = AnalyticEmotion(replyContent);
				
				$box.append(loadingCoverHtml);
				
				$.ajax({
					url: '/bbs/submit_layer_reply/',
					data: {'prid':prid, 'content':replyContent, 'target_uid':targetUID},
					type: 'POST',
					success: function(callback) {
						itemFadeOut($box, '.loading-cover');
						var obj = jQuery.parseJSON(callback);
						if(obj.msg=='success') {
							$textarea.val('');

							/*var rrHtml = '<div class="media hidden"><div class="media-left"><a href="/user/profile/' + obj.uid + '/">\
							<img class="media-object avatar-xs" src="' + obj.uthumb + '" alt="avatar"></a></div>\
							    <div class="media-body"><a class="username" href="/user/profile/' + obj.uid + '/" target="_blank">' 
							    + obj.uname + '</a>：' + obj.new_content + '<div class="rr-bottom" data-lrid="' + obj.lrid + '">\
							    <a class="btn-del del-lr" role="button">删除</a>&nbsp;&nbsp;<time>刚刚</time>&nbsp;&nbsp;<a class="btn-r" role="button">回复</a></div></div></div>';
							*/

							//分页初始化
							$lp = $wrap.find('.layer-pagination');
							$lp.attr('data-len', parseInt($lp.attr('data-len'))+1);
							initLayerPa($lp, 'add');
							//$lp.before($(rrHtml).fadeIn());
							//layerReplyDel($lrWrap.find('.del-lr:last'));
							//重新初始化该层评论
							

						} else {
							if(obj.msg=='901') {
								var tip = '请输入要回复的内容';
							} else if(obj.msg=='902') {
								var tip = '回复内容不能全部为空格';
							} else if(obj.msg=='401')  {
								var tip = '请登录后再回复'
							} else if(obj.msg=='103') {
								var tip = '该楼层已被删除'
							} else {
								var tip = obj.msg + '错误，请联系管理员';
							}
							showTip(tip, 'warning', $('.reply-area'));
						}
						
					}
				});
			});
		}
		

	}); //click bind
}


function initLayerRR($target) {
	$target.click(function() {
		console.log('initLayerRR')
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
			var textareaHtml = '<div class="form-group reply-area submit-area" style="margin:20px 0 0"><div class="input-group">\
			    <textarea class="form-control text-wrapper" style="border-top:0;border-top-left-radius:0!important;border-top-right-radius:0!important;" rows="3" maxlength="200"></textarea></div>\
				<div class="submit-btn-group"><span class="emotion-icon-rr" role="button"><i class="fa fa-smile-o"></i></span>\
				<div class="btn-group"><button class="btn btn-primary btn-sm btn-reply btn-submit">回复</button></div></div></div>';
			var temp = $_this.parent().prev().html().trim();
			var pat = /^(<a.*?>.*?<\/a>)/;
			var username = pat.exec(temp);
			var toHtml = '<div class="reply-title alert-success">回复 '+username[1]+' :</div>'
			
			var $lrWrap = $_this.parent().parent().parent().parent(); //楼层回复的wrap，必然存在
			$lrWrap.append('<div class="reply-wrapper"></div>');
			var $box = $lrWrap.find('.reply-wrapper');
			$box.append(toHtml).append(textareaHtml);  //添加回复框，同时添加'回复xxx'的标题样式
			//$box = $('.reply-area');
			$textarea = $box.find('.text-wrapper');
			ChangeTextareaState($box, 100);
			$replyTitle = $('.reply-title');
			$textarea.focus(function() {
				$replyTitle.css({'border-color':'rgb(26,188,156)'});
			});
			$textarea.blur(function() {
				$replyTitle.css({'border-color':'rgb(189,195,199)'});
			});
			$textarea.focus();

			//绑定回复
			var $submitLRBtn = $box.find('.btn-reply');
			$submitLRBtn.click(function() {
				console.log('123')
				var prid = $_this.parent().attr('data-prid');  //回复的target
				//var rid = $_this.parent().attr('data-rid');
				var targetUID = $_this.parent().attr('data-uid');
				var tip = checkReplyContent($textarea);
				if(tip) {
					showTip(tip, 'warning' ,$box);
					$textarea.focus();
					return false;
				}
				
				$box.append(loadingCoverHtml);
				var rrContent = $textarea.val();
				var rrContent = replaceWithBr(rrContent);
				var rrContent = AnalyticEmotion(rrContent);
				$.ajax({
					url: '/bbs/submit_layer_reply/',
					data: {'prid':prid, 'target_uid':targetUID, 'content':rrContent},
					type: 'POST',
					success: function(callback) {
						var obj = $.parseJSON(callback);
						if(obj.msg == 'success') {
							$textarea.val('');
							/*if(obj.uid == targetUID) {
								var headingHtml = '<a class="username" href="/user/profile/' + obj.uid + '/">' + obj.uname + '</a>&nbsp;:&nbsp;';
							} else {
								var headingHtml = '<a class="username" href="/user/profile/' + obj.uid + '/">' + obj.uname + 
								'</a>&nbsp;回复&nbsp;<a class="username" href="/user/profile/' + targetUID + '/">' + obj.target_uname + '</a>&nbsp;:&nbsp;';
							}
							var lrHtml = '<li class="media">\
								<div class="media-left"><a href="/user/profile/' + obj.uid + '/" target="_blank"><img class="media-object avatar-xs" src="' + obj.uthumb + '"></a></div>\
								<div class="media-body">\
								  <div class="media-heading lr-content">' + headingHtml + obj.new_content + '</div>\
								  <div class="rr-bottom" data-uid="' + obj.uid + '" data-prid="' + prid + '" data-lrid="' + obj.lrid + '">\
								     <a class="btn-del del-lr" role="button">删除</a>&nbsp;&nbsp;<time>刚刚</time>\
								  </div></div></li>';*/
							console.log(obj.msg)
							$lp = $lrWrap.find('.layer-pagination');
							$lp.attr('data-len', parseInt($lp.attr('data-len'))+1);
							//$lp.before($(lrHtml).fadeIn());
							//console.log('add_start')
							//var $newlr = $lrWrap.find('.del-lr:last');
							//layerReplyDel($newlr);//新lr绑定删除
							//initLayerRR($newlr);
							initLayerPa($lp, 'add'); //分页初始化
							
						} else {
							if(obj.msg=='901') {
								var tip = '请输入要回复的内容';
							} else if(obj.msg=='902') {
								var tip = '回复内容不能全部为空格';
							} else if(obj.msg=='401')  {
								var tip = '请登录后再回复';
							} else if(obj.msg=='103') {
								var tip = '该楼层已被删除';
							} else {
								var tip = obj.msg + '错误';
							}
							showTip(tip, 'warning', $box);
						}

						itemFadeOut($box, '.loading-cover');
						$textarea.focus();
					},
				});
			});
			
		}
	});
}




function layerReplyDel($target) {
	$target.click(function() {
		$_this = $(this);
		$wrap = $_this.parent().parent().parent(); //.media
		var lrid = $_this.parent().attr('data-lrid');
		if(lrid) {
			$modal = $('#deleteConfirmModal');
			$modal.find('.modal-body .media').remove();
			$modal.modal();
			$('#cancel-delete').click(function() {
				$modal.modal('hide');
			});
			$('#confirm-delete').unbind();
			$('#confirm-delete').click(function() {
				//$wrap.prepend(loadingCoverHtml);
				$.ajax({
					url: '/bbs/delete_lr/',
					type: 'POST',
					data: {'lrid': lrid},
					success: function(callback) {
						//itemFadeOut($wrap, 'loading-cover')
						var obj = $.parseJSON(callback);
						if(obj.msg=='success') {
							$modal.modal('hide');
							$layerWrap = $wrap.parent();  //.layer-reply-wrap
							itemSlideUp($wrap, 'item_self');
							var $lp = $layerWrap.find('.layer-pagination');
							$lp.attr('data-len', parseInt($lp.attr('data-len'))-1); //删除后需修改data-len
							//setTimeout(function() {initLayerPa($lp, 'del')},400);
							initLayerPa($lp, 'del');
							
						} else {
							console.log(obj.msg);
						}
					}
				});
				$('#confirm-delete').unbind();
			});
			
		} else {
			return false;
		}
	});
	
}

function layerDel($target) {
	$target.click(function() {
		$_this = $(this);
		$wrap = $_this.parent().parent().parent();
		var rid = $_this.parent().attr('data-prid');
		if(rid) {
			$modal = $('#deleteConfirmModal');
			var tipHtml = '<div class="media"><div class="media-left"><div class="ccs-tip ccs-tip-warning"></div></div><div class="media-body media-middle"><div class="ccs-desc">此回贴下的回复也会同步删除哦~</div></div></div>';
			$modalBody = $modal.find('.modal-body');
			$modalBody.find('.media').remove();
			$modalBody.prepend(tipHtml);
			$modal.find('h4').html('确认删除回帖');
			$modal.modal();
			console.log(rid)
			$('#cancel-delete', '#confirm-delete').unbind();
			$('#cancel-delete').click(function() {
				$modal.modal('hide');
				$('#cancel-delete').unbind();
			});
			$('#confirm-delete').click(function() {
				$wrap.prepend(loadingCoverHtml);
				$.ajax({
					url: '/bbs/delete_reply/',
					type: 'POST',
					data: {'rid': rid},
					success: function(callback) {
						itemFadeOut($wrap, '.loading-cover');
						var obj = $.parseJSON(callback);
						console.log(obj)
						if(obj.msg=='success') {
							console.log('success');
							$modal.modal('hide');
							itemSlideUp($wrap, 'item_self')
							//初始化pagination
							
						} else {
							console.log(obj.msg);
						}
					}
				});
				$('#confirm-delete').unbind();
				
			});
			
		} else {
			
		}
	});
}

function delPost() {
	$('.del-post').click(function() {
		console.log('delPost')
		var $_this = $(this);
		var pid = $_this.attr('data-pid');
		$modal = $('#deleteConfirmModal');
		var tipHtml = '<div class="media"><div class="media-left"><div class="ccs-tip ccs-tip-warning"></div></div><div class="media-body media-middle"><div class="ccs-desc">此贴下的所有回复都会删除哦~</div></div></div>';
		$modalBody = $modal.find('.modal-body');
		$modalBody.find('.media').remove();
		$modalBody.prepend(tipHtml);
		$modal.find('h4').html('确认删除帖子');
		$modal.modal();

		$('#cancel-delete', '#confirm-delete').unbind();
		$('#cancel-delete').click(function() {
			$modal.modal('hide');
			$('#cancel-delete').unbind();
		});
		$('#confirm-delete').click(function() {
			$.ajax({
				url: '/bbs/delete_post/',
				data: {'pid':pid},
				type: 'POST',
				success: function(callback) {
					var obj = $.parseJSON(callback);
					console.log(obj)
					var msg = obj.msg;
					if(msg=='success') {
						var boardUrl = $('.breadcrumb>a:nth(2)').attr('href');
						console.log(boardUrl)
						window.location.href = boardUrl;
					} else {
						var $wrap = $_this.parent().parent();
						showTip('错误'+msg, 'warning', $wrap)
					}
				}
			});
		});
		
	});
}

function initUserCard($target) { //elems with class popover
	$target.popover({
		//placement: 'right',
		content: function() {
			var profileLink = $(this).attr('href');
			var uname = $(this).attr('data-uname');
			var uavatar = $(this).attr('data-avatar');
			var ulevel = $(this).attr('data-ulevel');
			var usign = $(this).attr('data-usign');
			var postedCounts = $(this).attr('data-posted-counts');
			var fansCounts = $(this).attr('data-fans-counts');
			var popContent = '<div class="pop-content-inside"><a class="usercard-uname" href="'+ profileLink + '" target="_blank">' + uname + '</a>&nbsp;&nbsp;<span class="label label-primary">Lv '+ulevel+'</span><p><small>发帖: ' + postedCounts + '&nbsp;&nbsp;&nbsp;粉丝: ' + fansCounts + '</small></p><p><small>' + usign + '</small></p></div>\
			    <img style="position:absolute;left:10px;bottom:10px;" class="media-object img-thumbnail" src="' + uavatar + '" alt="avatar">'
			return popContent;
		},
		title: function() {
			var ufocused = $(this).attr('data-focused');
			if(ufocused=='1') {
				var popTitle = '<button class="btn btn-primary btn-xs usercard-msg">私信</button><button class="btn btn-warning btn-xs usercard-focus">已粉</button>';
			} else if(ufocused=='0') {
				var popTitle = '<button class="btn btn-primary btn-xs usercard-msg">私信</button><button class="btn btn-warning btn-xs usercard-focus">关注</button>';
			} else if(ufocused=='2') {
				var popTitle = ' ';
			}
			return popTitle;
		},
		html: true,
		trigger: 'manual',
		container: 'body',
		//delay: {show: 400, hide: 200 }
	}).on('mouseenter', function() {
		var usercard_bg = $(this).attr('data-bg');
		var uid = $(this).attr('data-uid');
        var _this = this;
        window.enterTimer = setTimeout(function() {
        	$(_this).popover('show');
            if(usercard_bg) {
    			$('.popover-title').css('background-image', 'url(' + usercard_bg + ')');
    		} else {
    			$('.popover-title').css('background-image', 'url(/static/images/default/userinfo/bg_default/bg1.jpg)');
    		}

            $('.popover').on('mouseleave', function() {
                $(this).popover('hide');
            });
            //绑定focus
            $('.usercard-focus').click(function() {
            	$_this = $(this);
            	var loginRes = checkLogin();
        		if(!loginRes) {
        			$(_this).popover('hide');
        			return false;
        		}
            	$_this.attr('disabled', true);
            	$.ajax({
    				url: '/user/focus/',
    				data: {'target_uid':uid},
    				type: 'POST',
    				success: function(callback) {
    					var obj = $.parseJSON(callback);
    					var msg = obj.msg;
    					console.log(msg)
    					if(msg=='success') {
    						$_this.html('已粉');
    						$('[data-uid="'+uid+'"]').attr('data-focused','1');
    						var content = '关注成功';
    					} if(msg=='cancel_success') {
    						var content = '取消关注成功';
    						$_this.html('关注');
    					} else {
    						if(msg=='101') {
    							var content = '服务器错误';
    						} else if(msg=='911') {
    							var content = '自己不能关注自己';
    						} else if(msg=='402') {
    							var content = '对方设置了不允许任何人关注';
    						}
    					}
    					$('.tooltip').tooltip('destroy');
    					$_this.attr({'data-toggle':'tooltip',
    						'data-trigger':'click',
    						'data-placement':'top',
    						'data-original-title':content});
    					$_this.tooltip('show');
    					st = window.setTimeout(function() {
    						$_this.tooltip('destroy');
    					}, 800);
    					
    				},
    				error: function() {
    					//$_this.html('关注');
    					var content = '未知错误，请重试';
    				}
    			});
            	$_this.removeAttr('disabled');
    		});
            //绑定message
            var $msgTextarea = $('#sendMsgModal .text-wrapper');
        	ChangeTextareaState($('#sendMsgModal'), 250);
        	$('#sendMsgModal').on('shown.bs.modal', function () {
        		$msgTextarea.focus()
        	});
        	var $btnMsg = $('.usercard-msg');
        	$btnMsg.unbind('click');
        	$btnMsg.click(function() {
        		$(_this).popover('hide');
        		var loginRes = checkLogin();
        		if(!loginRes) {
        			return false;
        		}
        		//var uid = $(this).attr('data-uid');
        		$('.modal').modal('hide');
        		var $msgModal = $('#sendMsgModal');
        		$msgModal.modal();
        		var un = $(this).parent().parent().find('.usercard-uname').text();
        		$msgModal.find('.modal-title').html('To: '+un);
        		
        		var $btnSubmit = $msgModal.find('.btn-submit');
        		$btnSubmit.unbind('click');
        		$btnSubmit.click(function() {  //绑定发送
        			var $_this = $(this);
        			var $text = $msgModal.find('.text-wrapper');
        			var $area = $('.send-msg-area');
        			var tip = checkReplyContent($text);
        			if(tip) {
        				showTip(tip, 'warning', $area);
        				$text.focus();
        				return false;
        			}
        			var content = $text.val();
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
        						$text.val('');
        						showTip('发送成功', 'success', $area);
        						
        					} else {
        						showTip('错误'+obj.msg, 'danger', $area);
        					}
        				}
        			});
        		});
        	});
        },400);
        
    }).on('mouseleave', function() {
        var _this = this;
        clearTimeout(enterTimer);
        setTimeout(function() {
            if (!$('.popover:hover').length) {
                $(_this).popover('hide')
            }
        }, 100);
    });
}



$(function() {
	//帖子视频尺寸自适应
	$.each($('iframe'), function() {
		if(!!$(this).parent('p').length) {
			$(this).parent('p').addClass('embed-responsive embed-responsive-16by9');
		}
	});
	
	//删除楼层
	layerDel($('.del-r'))
	//删除楼层的回复
	layerReplyDel($('.del-lr'));
	delPost();
	//用户卡片
	initUserCard($('[data-toggle=popover]'));
	
	//
	initLayerReply($('.btn-pr'));
	initLayerRR($('.btn-lr'));
	
	//层评论分页初始化
	initLayerPa($('.layer-pagination'), 'default');
	
});

