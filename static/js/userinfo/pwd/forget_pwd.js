/**
 * 
 */

function GetbackPwd(doc){
	var username = $('#username').val();
	var email = $('#email').val();
	$(this).removeAttr('onclick');
	$(this).css('background','#eee');
	$.ajax({
		url:'/user/forgetpwd/submit/',
		type:'POST',
		data:{'username':username,'email':email},
		success:function(callback){
			var obj = jQuery.parseJSON(callback);
			var status = obj['status']
			if(status == 0){
				$('#tip_box').text('用户名不能为空');
			}
			if(status == 1){
				$('#tip_box').text('邮箱格式错误');
			}
			if(status == 2){
				$('#tip_box').text('用户名不存在');
			}
			if(status == 3){
				$('.login_button').css('display','none');
				$('.login_fieldset').css('display','none');
				$('.login_input').css('display','none');
				var max_width = parseInt($(window).width());
				if(max_width > 450){
					$('.login_frame').css({'width':'610px'});
					$('#tip_box').html('<div id="tip_box" class="tip_box" style="font-size: 18px;color:#333;margin-top: 8px;padding: 10px 50px;"><p style="color:#333;">正在发送验证邮件至您的邮箱…… '+' <i class="fa fa-spinner fa-pulse fa-2x fa-fw margin-bottom"></i></p></div>');
				}
				else{
				$('#tip_box').html('<div id="tip_box" class="tip_box" style="font-size: 18px;color:#333;margin-top: 8px;padding: 10px 50px;border: 1px solid #eee;box-shadow: 0 0 5px #bebebe;"><p style="color:#333;">正在发送验证邮件至您的邮箱…… '+' <i class="fa fa-spinner fa-pulse fa-3x fa-fw margin-bottom"></i></p></div>');
				}
				$.ajax({
					url:'/user/forgetpwd/sendmail/',
					type:'POST',
					data:{'username':username,'email':email},
					success:function(callback){
						var obj = jQuery.parseJSON(callback);
						var status = obj['status']
						if(status==8){
							if(max_width > 450){
							html_content = '<h2 style="color:#e36229;">发送成功</h2><p style="margin:10px;color:#333;">亲爱的 '+username+
								'：</p><p style="text-indent:2em;margin:10px;color:#333;">找回密码的邮件已成功发送到你的邮箱，快去查看吧~</p><p style="margin:10px;color:#333;"><img src="/static/images/cartoon_face1/face11.jpg"></img></p>' +
								'<a href="/" title="点击返回首页" style="color:#333;margin:20px auto;padding:10px;">点击返回首页</a>'+
                                '<a href="/" title="点击返回首页"><img src="/static/images/common/logo/bigedianying_logo_black.png" style="margin-left:370px;"></img></a>'
							}
							else{
							html_content = '<h2 style="color:#e36229;">发送成功</h2><p style="margin:10px;color:#333;">亲爱的 '+username+
								'：</p><p style="text-indent:2em;margin:10px;color:#333;">找回密码的邮件已成功发送到你的邮箱，快去查看吧~</p><p style="margin:10px;color:#333;"><img src="/static/images/cartoon_face1/face11.jpg"></img></p>' +
                                    '<a href="/" title="点击返回首页" style="margin:20px auto;color:#333;padding:10px;">点击返回首页</a>'+
                                    '<a href="/" title="点击返回首页"><img src="/static/images/common/logo/bigedianying_logo_black.png" style="margin-left:120px;"></img></a>'
							}
							$('#tip_box').html(html_content);
							$('#tip_box').css({'background':'#FFF','font-size':'18px'});
						}
						else if(status==0){
							if(max_width > 450){
							html_content = '<h2 style="color:#e36229;">系统错误</h2><p style="margin:10px;color:#333;">亲爱的 '+username+
								'：</p><p style="text-indent:2em;margin:10px;color:#333;">非常抱歉，由于系统原因发送邮件失败，请稍后再试，或者联系管理员：bigedianying@gmail.com。</p><p style="margin:10px;color:#333;"><img src="/static/images/cartoon_face1/face11.jpg"></img></p>' +
								'<a href="/" title="点击返回首页" style="margin:20px auto;padding:10px;">点击返回首页</a>'+
								'<img src="/static/images/common/logo/bigedianying_logo_black.png" style="margin-left:370px;"></img>'
							}
							else{
							html_content = '<h2 style="color:#e36229;">系统错误</h2><p style="margin:10px;color:#333;">亲爱的 '+username+
								'：</p><p style="text-indent:2em;margin:10px;color:#333;">非常抱歉，由于系统原因发送邮件失败，请稍后再试，或者联系管理员：bigedianying@gmail.com。</p><p style="margin:10px;color:#333;"><img src="/static/images/cartoon_face1/face11.jpg"></img></p>' +
                                    '<a href="/" title="点击返回首页" style="margin:20px auto;padding:10px;">点击>返回首页</a>'+
                                    '<img src="/static/images/common/logo/bigedianying_logo_black.png" style="margin-left:120px;"></img>'
							$('.login_button').css('display','none');
							$('.login_input').css('display','none');
							$('#tip_box').html(html_content);
							$('#tip_box').css('background','#FFF');
							}
						}
					}
				});
			}
			if(status == 5){
				$('#tip_box').text('邮箱与密码不匹配');
			}
		}
	});
}
