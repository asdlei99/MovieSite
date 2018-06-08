/**
 *
 */

function initSpeakReply($target) {
    $target.click(function() {
        $_this = $(this);
        var speakID = $_this.parent().attr('data-sid');
        $replyArea = $_this.parent().parent().find('.reply-area');
        if(!$replyArea.length) {
            $('.reply-area').remove();
            var textHtml = '<div class="form-group reply-area submit-area" style="margin:20px 0 0"><div class="input-group">\
			    <textarea class="form-control text-wrapper" placeholder="我也说一句" rows="3" maxlength="200"></textarea></div>\
				<div class="submit-btn-group"><span class="emotion-icon-rr" role="button"><i class="fa fa-smile-o"></i></span>\
				<div class="btn-group"><button class="btn btn-primary btn-sm btn-reply btn-submit">回复</button></div></div></div>';
            $_this.parent().parent().append(textHtml);
            var $textarea = $_this.parent().parent().find('.text-wrapper');
            var threshold = 100;
            $box = $_this.parent().parent().find('.reply-area');
            ChangeTextareaState($box, threshold);
            $replyBtn = $_this.parent().parent().find('.btn-reply');//点击发布
            $replyBtn.click(function() {
                var tip = checkReplyContent($textarea);
                if(tip) {
                    showTip(tip, 'warning' ,$('.reply-area'));
                    return;
                }

                var replyContent = $textarea.val();
                replyContent = replaceWithBr(replyContent);
                replyContent = AnalyticEmotion(replyContent);
                var $wrap = $_this.parent().parent().parent();
                $wrap.find('.reply-area').append(loadingCoverHtml);
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
                        if(msg==='success') {
                            $speakReplyList = $_this.parent().parent().find('.speak-reply-list');
                            if(!$speakReplyList.length) {  //评论列表不存在先加列表
                                var replyListHtml = '<ul class="media-list speak-reply-list"></ul>';
                                $_this.parent().after(replyListHtml)
                            }
                            $replyList = $_this.parent().parent().find('.speak-reply-list');
                            var replyHtml = '<li class="media">\
					              <div class="media-left"><a href="/user/profile/' + obj.uid + '/" target="_blank"><img class="avatar-xs img-circle" src="' + obj.uthumb + '"></a></div>\
					              <div class="media-body">\
					                <div class="media-heading"><a class="username mr-10" href="/user/profile/' + obj.uid + '/">' + obj.uname + '</a>: ' + obj.ucontent + '</div>\
					                <div class="media-bottom" data-uid="' + obj.uid + '" data-rid="' + obj.rid + '">\
					                  <time class="mr-20">' + '刚刚' + '</time>\
					                  <a class="btn-reply-r mr-10" role="button" title="回复"><i class="fui-chat"></i></a>\
					                  <a class="btn-del btn-del-reply" role="button" title="删除"><i class="fa fa-trash-o"></i></a></div></div></li>';
                            $(replyHtml).hide().appendTo($replyList).fadeIn();
                            $textarea.val('');
                            $_this.text('评论(' + $replyList.children('.media').length + ')');

                            var $newReply = $replyList.children('li:last');
                            initSpeakReply($newReply.find('.btn-reply-r')); //初始化回复
                            delSpeakReply($newReply.find('.btn-del-reply')); //初始化删除
                        } else if(msg) {
                            var tip = msg+'错误';
                            showTip(tip, 'danger' ,$('.reply-area'));
                        }
                    }
                });
            });

        } else {
            //$('.reply-area').remove();
            $_this.parent().parent().find('.text-wrapper').focus();
        }
        $textarea.focus();

    });
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
            $('.reply-area').remove();
            $('.alert').remove();
            var $_this = $(this);
            var textareaHtml = '<div class="form-group reply-area submit-area" style="margin:20px 0 0"><div class="input-group">\
			    <textarea class="form-control text-wrapper" placeholder="我也说一句" rows="3" maxlength="200"></textarea></div>\
				<div class="submit-btn-group"><span class="emotion-icon-rr" role="button"><i class="fa fa-smile-o"></i></span>\
				<div class="btn-group"><button class="btn btn-primary btn-sm btn-reply btn-submit">回复</button></div></div></div>';
            var $temp = $_this.parent().prev().html().trim();
            var pat = /^(<a.*?>.*?<\/a>)/;
            var username = pat.exec($temp);
            var toHtml = '<div class="alert alert-warning" style="margin-bottom:-20px;margin-top:5px;font-size:12px;padding:10px;">回复 '+username[1]+' :</div>'
            if(typeof($_this.parent().attr('data-rrid')) == 'undefined') {  //对回复进行回复
                $_this.parent().parent().append(toHtml).append(textareaHtml);  //添加回复框
                $speakRRList = $_this.parent().parent().find('.speak-rr-list');
                if(!$speakRRList.length) {
                    $_this.parent().after('<ul class="media-list speak-rr-list"></ul>');
                    $speakRRList = $_this.parent().parent().find('.speak-rr-list');
                }
            } else {  //对回复的回复进行回复
                $speakRRList = $_this.parent().parent().parent().parent();
                $speakRRList.after(textareaHtml).after(toHtml);
            }
            var $box = $('.reply-area');
            var $textarea = $box.find('.text-wrapper');
            var threshold = 100;
            ChangeTextareaState($box, threshold);
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
                    showTip(tip, 'warning' ,$('.reply-area'));
                    $textarea.focus();
                    return false;
                }

                $(this).parent().parent().parent().append(loadingCoverHtml);
                var rrContent = $textarea.val();
                rrContent = replaceWithBr(rrContent);
                rrContent = AnalyticEmotion(rrContent);
                $.ajax({
                    url: '/user/submit_speak_rr/',
                    data: {'rid':rid, 'target_uid':targetUid, 'content':rrContent},
                    type: 'POST',
                    success: function(callback) {
                        var obj = $.parseJSON(callback);
                        if(obj.msg === 'success') {
                            if(obj.uid == targetUid) {
                                var headingHtml = '<a class="username" href="/user/profile/' + obj.uid + '/">' + obj.uname + '</a>&nbsp;:&nbsp;';
                            } else {
                                var headingHtml = '<a class="username" href="/user/profile/' + obj.uid + '/">' + obj.uname +
                                    '</a>&nbsp;回复&nbsp;<a class="username" href="/user/profile/' + targetUid + '/">' + obj.target_uname + '</a>&nbsp;:&nbsp;';
                            }
                            var rrHtml = '<li class="media">\
								<div class="media-left"><a href="/user/profile/' + obj.uid + '/" target="_blank"><img class="avatar-xs img-circle" src="' + obj.uthumb + '"></a></div>\
								<div class="media-body">\
								  <div class="media-heading">' + headingHtml + obj.rr_content + '</div>\
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
    //滚动加载
    var $speakWrap = $('#speak>.media-list');
    var $commentWrap = $('#comment>.media-list');
    var $postWrap = $('#post>.media-list');
    $speakWrap.infinitescroll(
        {
            navSelector  : '#speak-next-page',
            nextSelector : '#speak-next-page>a',
            itemSelector : '#speak>.media-list>.speak-item',
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
            }
        },
        function(newadd) {
            initSpeakReply($(newadd).find('.btn-speak-reply'));
            initSpeakRR($(newadd).find('.btn-reply-r'));
            delSpeak($(newadd).find('.btn-del-speak'));
            delSpeakReply($(newadd).find('.btn-del-reply'));
            delSpeakRR($(newadd).find('.btn-del-rr'));
            initLike($(newadd).find('.btn-speak-like'));
            $(newadd).find('.comment-fade-cover').click(function() {
                $(this).parent().css('max-height','initial');
                $(this).remove();
            });
        }
    );
    $commentWrap.infinitescroll(
        {
            navSelector  : '#comment-next-page',
            nextSelector : '#comment-next-page>a',
            itemSelector : '#comment>.media-list>.media',
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
            }
        },
        function (newadd) {
            $(newadd).find('.comment-fade-cover').click(function() {
                $(this).parent().css('max-height','initial');
                $(this).remove();
            });
        }
    );
    $postWrap.infinitescroll(
        {
            navSelector  : '#post-next-page',
            nextSelector : '#post-next-page>a',
            itemSelector : '#post>.media-list>.media',
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
            }
        },
        function (newadd) {
            $(newadd).find('.comment-fade-cover').click(function() {
                $(this).parent().css('max-height','initial');
                $(this).remove();
            });
        }
    );

    $('#speak-tab-btn').click(function() {
        $commentWrap.infinitescroll('unbind');
        $postWrap.infinitescroll('unbind');
        $speakWrap.infinitescroll('bind');
    });
    $('#comment-tab-btn').click(function() {
        $postWrap.infinitescroll('unbind');
        $speakWrap.infinitescroll('unbind');
        $commentWrap.infinitescroll('bind');
    });
    $('#post-tab-btn').click(function() {
        $commentWrap.infinitescroll('unbind');
        $speakWrap.infinitescroll('unbind');
        $postWrap.infinitescroll('bind');
    });

    $('.msg-img-wrap .gallery-img').click(function (e) {
        e.preventDefault();
        $(this).ekkoLightbox({
            'loadingMessage': '<div class="well text-center"><i class="fa fa-spinner fa-spin"></i> 图片加载中……</div>'
        });
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

    //评论等查看全文
    $('.comment-content > .comment-fade-cover').click(function() {
        $(this).parent().css('max-height','initial');
        $(this).remove();
    });


    //收藏页内部导航初始化
    var $cm = $('#c-movie');
    var $ct = $('#c-tv');
    var $ca = $('#c-anime');
    var $cs = $('#c-show');
    var is_clicking = '0';
    $.each([$cm, $ct, $ca, $cs], function() {
        $(this).click(function() {
            var $_this = $(this);
            var $area = $('#collect > .list-group .media-list');

            if(!$_this.parent().hasClass('active')) {  //没有active时触发
                if(is_clicking=='0') {  //没有点击时触发
                    is_clicking = '1';
                    $('#collect ul>li').removeClass('active');
                    $_this.parent().addClass('active');
                    $area.prepend(loadingCoverHtml);
                    var cate = $_this.attr('data-cate');
                    var d_url = window.location.href + 'collection/' + cate + '/';

                    $.ajax({
                        url: d_url,
                        data: {'cate':cate},
                        type: 'POST',
                        success: function(callback) {
                            itemFadeOut($area, '.loading-cover')
                            var obj = $.parseJSON(callback);
                            $area.empty();
                            if(obj.msg) {
                                var msg = obj.msg;
                                if(msg=='501') {
                                    var tipHtml = '<div class="p-20 text-center"><div class="ccs-tip ccs-tip-no"></div><div class="ccs-desc">空间主人设置了权限，只有自己可以查看哦~</div></div>';
                                } else if(msg=='502') {
                                    var tipHtml = '<div class="p-20 text-center"><div class="ccs-tip ccs-tip-no"></div><div class="ccs-desc">空间主人设置了权限，只有Ta关注的人可以查看哦~</div></div>';
                                } else if(msg=='401') {
                                    var tipHtml = '<div class="p-20 text-center"><div class="ccs-tip ccs-tip-please"></div><div class="ccs-desc">空间主人设置了权限，请登录后查看哦~</div></div>';
                                }
                                $area.append(tipHtml);
                            } else {  //没有msg
                                if(obj.length > 1) {
                                    $.each(obj, function(i) {
                                        if(!i==0) {
                                            var intro_len = this.intro.length;
                                            if(intro_len > 50) {
                                                var sliced_intro = this.intro.slice(0,50) + '...';
                                            } else {
                                                var sliced_intro = this.intro;
                                            }
                                            if(this.is_owner) {
                                                var cancelBtnHtml = '<a class="btn-del pull-right text-smaller" role="button" data-cate="' + cate + '" data-id="' + this.id + '"><i class="fa fa-trash-o"></i></a>'
                                            } else {
                                                var cancelBtnHtml = ''
                                            }
                                            var itemHtml = '<div class="media col-lg-6">\
												<div class="media-left"><a href="/' + cate + '/' + this.id + '/" target="_blank"><img src="' + this.poster + '"></a></div>\
												  <div class="media-body">\
												  <h3 class="media-heading"><a href="/' + cate + '/' + this.id + '/" target="_blank">' + this.ch_name + ' <span class="douban-color ">' + this.score + '</span></a></h3>\
												  <div class="collect_date"><i class="fa fa-star-o"></i> ' + this.c_date + cancelBtnHtml +'</div>\
												  <p class="media-intro">' + sliced_intro + '</p></div></div>';
                                            $(itemHtml).hide().prependTo($area).fadeIn();
                                        }

                                    });
                                    $area.append('<div class="clearfix"></div><div class="layer-pagination text-center p-10"></div>');
                                    PaInit();
                                    ccInit();
                                } else {  //长度等于1
                                    var temp_dict = {'movie':'电影','tv':'电视剧','anime':'动漫','show':'综艺'};
                                    $.each(temp_dict, function(k,v) {
                                        if(k==cate) {
                                            trans_res = v;
                                            return true;
                                        }
                                    });
                                    var isOwner = obj[0]

                                    if(isOwner) {
                                        var address = '我';
                                    } else {
                                        var address = '空间主人';
                                    }
                                    var tipHtml = '<div class="p-20 text-center"><div class="ccs-tip ccs-tip-sad"></div><div class="ccs-desc">' + address + '暂时没有收藏任何' + trans_res + '哦~</div></div>';
                                    //$area.append(tipHtml);
                                    $(tipHtml).hide().appendTo($area).fadeIn();
                                }
                            }

                            is_clicking = '0';
                        }

                    });
                }
            }

        });

    });

    //收藏内容删除初始化
    ccInit();

    //ajax分页初始化
    PaInit();

    //模态发送消息和关注
    var $msgModal = $('#sendMsgModal');
    var $msgTextarea = $msgModal.find('.text-wrapper');
    ChangeTextareaState($msgModal, 250);
    $msgModal.on('shown.bs.modal', function () {
        $msgTextarea.focus()
    });

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
            //var $text = $msgModal.find('.text-wrapper');
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
    var $btnFocus = $('.btn-focus');
    $btnFocus.click(function() {
        var loginRes = checkLogin();
        if(!loginRes) {
            return false;
        }
        var $_this = $(this);
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
                    var content = '关注成功';
                } else if(msg=='cancel_success') {
                    $_this.html('关注');
                    var content = '取消关注成功';
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
            error: function() {
                $_this.html(originHtml);
            }
        });
    });
});


//收藏内容删除初始化
function ccInit() {
    var $cancelBtn = $('#collect .btn-del');
    if($cancelBtn.length) {
        $cancelBtn.click(function() {
            var $_this = $(this);
            $modal = $('#ccConfirmModal');
            $modal.modal();

            $('#cancel-cc').click(function() {
                $modal.modal('hide');
            });
            $('#confirm-cc').unbind();  //取消确认绑定
            $('#confirm-cc').click(function() {  //重新绑定
                var $area = $_this.parent().parent().parent();
                $area.prepend(loadingCoverHtml);
                var cate = $_this.attr('data-cate');
                var xid = $_this.attr('data-id')
                $.ajax({
                    url: '/user/cancel_collect/',
                    type: 'POST',
                    data: {'xid':xid, 'cate':cate},
                    success: function(callback) {
                        itemFadeOut($area, '.loading-cover')
                        $wrap = $_this.parent().parent().parent().parent();
                        var obj = $.parseJSON(callback);
                        if(obj.msg=='success') {
                            $modal.modal('hide');
                            itemFadeOut($area, 'item_self');
                            initLayerPa($wrap, 'delete'); //初始化分页
                            var cur_counts = obj.cur_counts;
                            var tempDict = {'movie':'电影','tv':'电视剧','anime':'动漫','show':'综艺'};
                            var navBtnID = 'c-'+cate;
                            $.each(tempDict, function(k,v) {

                                if(k==cate) {
                                    $('#'+navBtnID).text(v + ' (' + cur_counts + ')')
                                }
                            });

                        } else {
                            $_this.text('重试');
                        }
                    },
                });
            });

        });
    } else {
        return false;
    }
}

//分页初始化
function PaInit() {
    $pa = $('.layer-pagination');
    $.each($pa, function() {
        var $this = $(this);
        var itemsPerPage = 10;
        var $allItems = $this.parent().children('.media');
        $allItems.addClass('hidden');
        var len = $allItems.length;
        var pages = Math.ceil(len / itemsPerPage);
        if(pages==0) {
            return;
        } else if(pages==1) {
            $pa.hide();
        }
        $this.twbsPagination({
            totalPages: pages,
            visiblePages: 7,
            first: '首页',
            last: '尾页',
            prev: '上一页',
            next: '下一页',
            paginationClass: 'pagination-simple',
            onPageClick: function (event, page) {
                $allItems.addClass('hidden');
                window.cur_page = page;
                for(var i=(page-1)*itemsPerPage; i<page*itemsPerPage; i++) {
                    $this.parent().children('.media:eq('+ i +')').removeClass('hidden');
                }
                if(page==1) {
                    $this.find('li.first').hide();
                    $this.find('li.prev').hide();
                } else if(page==pages) {
                    $this.find('li.last').hide();
                    $this.find('li.next').hide();
                }
            }
        });

    });
}

window.firstInitPa = true;
function initLayerPa($wrap, action) {
    $pgWrap = $wrap.find('.layer-pagination')
    $pgWrap.empty();
    $pgWrap.removeData("twbs-pagination");
    $pgWrap.unbind('page');
    var itemsPerPage = 10;
    var $allItems = $wrap.find('.media');
    $allItems.addClass('hidden');
    var len = $allItems.length;
    var pages = Math.ceil(len / itemsPerPage);
    $pgWrap.twbsPagination({
        totalPages: pages,
        visiblePages: 7,
        first: '首页',
        last: '尾页',
        prev: '上一页',
        next: '下一页',
        paginationClass: 'pagination-simple',
        onPageClick: function (event, page) {
            if(!firstInitPa) {
                window.cur_page = page;  //非首次初始化时使用这个当前页数
            }
            $wrap.find('.media').addClass('hidden');
            for(var i=(page-1)*itemsPerPage; i<page*itemsPerPage; i++) {
                $wrap.find('.media:eq('+ i +')').removeClass('hidden');
            }
            if(page==1) {
                $wrap.find('li.first').hide();
                $wrap.find('li.prev').hide();
            } else if(page==pages) {
                $wrap.find('li.last').hide();
                $wrap.find('li.next').hide();
            }
        }
    });

    if(len<=10) {
        $wrap.find('.layer-pagination').addClass('hidden');
    } else {
        $wrap.find('.layer-pagination').removeClass('hidden');
    }
    if(action=='add') {
        $wrap.find('li.last>a').trigger('click');
    } else if(action=='delete') {
        var serial = cur_page + 1
        $wrap.find('li:eq('+serial+')').trigger('click');  //通过当前页数来定位click触发页数
        //$wrap.find('li.first>a').trigger('click');
    }

}
