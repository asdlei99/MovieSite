
$(function() {
	/* 头像裁剪上传 */
	"use strict";
	(function (factory) {
	    if (typeof define === 'function' && define.amd) {
	        define(['jquery'], factory);
	    } else {
	        factory(jQuery);
	    }
	}(function ($) {
	    var cropbox = function(options, el){
	        var el = el || $(options.imageBox),
	            obj =
	            {
	                state : {},
	                ratio : 1,
	                options : options,
	                imageBox : el,
	                thumbBox : el.find(options.thumbBox),
	                spinner : el.find(options.spinner),
	                image : new Image(),
	                getDataURL: function ()
	                {
	                    var width = this.thumbBox.width(),
	                        height = this.thumbBox.height(),
	                        canvas = document.createElement("canvas"),
	                        dim = el.css('background-position').split(' '),
	                        size = el.css('background-size').split(' '),
	                        dx = parseInt(dim[0]) - el.width()/2 + width/2,
	                        dy = parseInt(dim[1]) - el.height()/2 + height/2,
	                        dw = parseInt(size[0]),
	                        dh = parseInt(size[1]),
	                        sh = parseInt(this.image.height),
	                        sw = parseInt(this.image.width);

	                    canvas.width = width;
	                    canvas.height = height;
	                    var context = canvas.getContext("2d");
	                    context.drawImage(this.image, 0, 0, sw, sh, dx, dy, dw, dh);
	                    var imageData = canvas.toDataURL('image/png');
	                    return imageData;
	                },
	                getBlob: function()
	                {
	                    var imageData = this.getDataURL();
	                    var b64 = imageData.replace('data:image/png;base64,','');
	                    var binary = atob(b64);
	                    var array = [];
	                    for (var i = 0; i < binary.length; i++) {
	                        array.push(binary.charCodeAt(i));
	                    }
	                    return  new Blob([new Uint8Array(array)], {type: 'image/png'});
	                },
	                zoomIn: function ()
	                {
	                    this.ratio*=1.1;
	                    setBackground();
	                },
	                zoomOut: function ()
	                {
	                    this.ratio*=0.9;
	                    setBackground();
	                }
	            },
	            setBackground = function()
	            {
	                /*
	        		var w =  parseInt(obj.image.width)*obj.ratio;
	                var h =  parseInt(obj.image.height)*obj.ratio;
	                
	                var pw = (el.width() - w) / 2;
	                var ph = (el.height() - h) / 2;

	                el.css({
	                    'background-image': 'url(' + obj.image.src + ')',
	                    'background-size': w +'px ' + h + 'px',
	                    'background-position': pw + 'px ' + ph + 'px',
	                    'background-repeat': 'no-repeat'});
	                */
	        	
	                if(parseInt(obj.image.width) < el.width()) {
	                	var w =  parseInt(obj.image.width)*obj.ratio;
	                	var h =  parseInt(obj.image.height)*obj.ratio;
	                	
	                } else {
	                	var w = parseInt(el.width())*obj.ratio;
	                	var h = (parseInt(obj.image.height) / (parseInt(obj.image.width) / parseInt(el.width())))*obj.ratio;
	                }
	                var pw = (el.width() - w) / 2;
	                var ph = (el.height() - h) / 2;
	                el.css({
	                    'background-image': 'url(' + obj.image.src + ')',
	                    'background-size': w +'px ' + h + 'px',
	                    'background-position': pw + 'px ' + ph + 'px',
	                    'background-repeat': 'no-repeat'});
	              
	            },
	            imgMouseDown = function(e)
	            {
	                e.stopImmediatePropagation();

	                obj.state.dragable = true;
	                obj.state.mouseX = e.clientX;
	                obj.state.mouseY = e.clientY;
	            },
	            imgMouseMove = function(e)
	            {
	                e.stopImmediatePropagation();

	                if (obj.state.dragable)
	                {
	                    var x = e.clientX - obj.state.mouseX;
	                    var y = e.clientY - obj.state.mouseY;

	                    var bg = el.css('background-position').split(' ');

	                    var bgX = x + parseInt(bg[0]);
	                    var bgY = y + parseInt(bg[1]);

	                    el.css('background-position', bgX +'px ' + bgY + 'px');

	                    obj.state.mouseX = e.clientX;
	                    obj.state.mouseY = e.clientY;
	                }
	            },
	            imgMouseUp = function(e)
	            {
	                e.stopImmediatePropagation();
	                obj.state.dragable = false;
	            },
	            zoomImage = function(e)
	            {
	                e.originalEvent.wheelDelta > 0 || e.originalEvent.detail < 0 ? obj.ratio*=1.1 : obj.ratio*=0.9;
	                setBackground();
	            }

	        obj.spinner.show();
	        obj.image.onload = function() {
	            obj.spinner.hide();
	            setBackground();

	            el.bind('mousedown', imgMouseDown);
	            el.bind('mousemove', imgMouseMove);
	            $(window).bind('mouseup', imgMouseUp);
	            el.bind('mousewheel DOMMouseScroll', zoomImage);
	        };
	        obj.image.src = options.imgSrc;
	        el.on('remove', function(){$(window).unbind('mouseup', imgMouseUp)});

	        return obj;
	    };

	    jQuery.fn.cropbox = function(options){
	        return new cropbox(options, this);
	    };
	}));


	 $(window).load(function() {
        var options =
        {
            thumbBox: '.thumbBox',
            spinner: '.spinner',
            imgSrc: 'avatar.png'
        }
        var cropper;
        $('#file').on('change', function(){
            var reader = new FileReader();
            reader.onload = function(e) {
                options.imgSrc = e.target.result;
                cropper = $('.imageBox').cropbox(options);
            }
            reader.readAsDataURL(this.files[0]);
            //this.files = [];
        })
        $('#btnCrop').on('click', function(){
        	if(!cropper) {return;}
            var img = cropper.getDataURL();
            //$('.cropped').append('<img src="'+img+'">');
            $('#btnCrop').attr('disabled', true);
            var $area = $('.imageBox')
            $area.append(loadingCoverHtml);
            $.ajax({
            	url: '/user/avatar/upload/',
            	data: {'avatar': img},
            	type: 'POST',
            	complete: function() {
            		$('#btnCrop').removeAttr('disabled');
            	},
            	success: function(callback) {
            		$area.find('.loading-cover').fadeOut().remove();
            		showTip('修改成功', 'success', $area);
            		$area.removeAttr('style');
            		var obj = jQuery.parseJSON(callback);
            		if(obj.success) {
            			var $avatar_l = $('#avatar-preview .avatar-l');
            			$avatar_l.attr('src', obj.avatar_l+'?r='+Math.random());
            			$('#navUserPhoto>img').attr('src', obj.avatar_s+'?r='+Math.random());
            		} else if(obj.error) {
            			
            		}
            	}
            });
        })
        $('#btnZoomIn').on('click', function(){
        	if(!cropper) {return;}
            cropper.zoomIn();
        })
        $('#btnZoomOut').on('click', function(){
        	if(!cropper) {return;}
            cropper.zoomOut();
        })
	 });
	 
});

function EditProfile($inputs) {
	$.each($inputs, function() {
		var $_this = $(this);
		var $icon = $_this.next();
		$icon.click(function() {
			$_this.focus();
		});
	})
}

$(function() {
	//点击头像修改
	$('#renew-avatar, #avatar-preview>img').click(function() {
		$('#avatar-wrap').children('.media-body').removeClass('hidden');
		$('#avatar-preview>p').text('当前头像');
	});
	
	//性别选项
	$genderRadio = $('input[name="gender-radios"]');
	$genderRadio.click(function() {
		$_this = $(this);
		if(!$_this.attr('checked')) {
			var $wrap = $('#profile-wrap');
			$wrap.prepend(loadingCoverHtml);
			$genderRadio.radiocheck('uncheck');
			$genderRadio.removeAttr('checked');
			$_this.radiocheck('check');
			$_this.attr('checked', true);
			if($_this.attr('id')=='gender-radios1') {
				var genderSelect = 'male';
			} else if($_this.attr('id')=='gender-radios2') {
				var genderSelect = 'female';
			}
			$.ajax({
				url: '/user/modify_settings/',
				type: 'POST',
				data: {'gender':genderSelect},
				success: function(callback) {
					var obj = $.parseJSON(callback);
					itemFadeOut($wrap, '.loading-cover')
					showTip('修改成功', 'success', $wrap);
				},
				error: function() {
					itemFadeOut($wrap, '.loading-cover')
					showTip('未知错误，请重试', 'danger', $wrap);
				}
			})
		} else {
			return false;  //点击已选的目标
		}

	});
	
	var $profileInputs = $('#profile-wrap').find('input');
	//点击图标编辑
	EditProfile($profileInputs);
	
	//更改签名
	$profileInputs.focus(function() {
		$_this = $(this);
		var val = $_this.val();
		var tag = $_this.attr('data-tag');
		$_this.unbind('blur');
		$_this.blur(function() {
			var newVal = $_this.val();
			if(newVal==val) {
				return false;
			}
			console.log(newVal);
			console.log(tag);
			var $wrap = $('#profile-wrap');
			$wrap.prepend(loadingCoverHtml);
			$.ajax({
				url: '/user/modify_settings/',
				type: 'POST',
				data: {'new_val': newVal, 'tag': tag},
				success: function(callback) {
					var obj = $.parseJSON(callback);
					itemFadeOut($wrap, '.loading-cover');
					if(obj.msg=='success') {
						showTip('修改成功', 'success', $wrap);
					} else {
						showTip(obj.msg, 'warning', $wrap);
					}
				},
				error: function() {
					itemFadeOut($wrap, '.loading-cover');
					showTip('未知错误', 'danger', $wrap);
				}
			});
		});
	});
	
	//偏好设置
	var $hSwitch = $('#habit-wrap .switch');
	$hSwitch.on('switchChange.bootstrapSwitch', function(e, state) {
		var $_this = $(this);
		var tag = $_this.find('input').attr('data-tag');
		
		if(state) {
			newVal = 1;
		} else {
			newVal = 0;
		}
		var $wrap = $('#habit-wrap');
		$wrap.prepend(loadingCoverHtml);
		$.ajax({
			url: '/user/modify_settings/',
			type: 'POST',
			data: {'tag':tag, 'new_val':newVal},
			success: function(callback) {
				itemFadeOut($wrap, '.loading-cover');
				if(newVal==0) {
					$.cookie('recvpush', 'no', {path:'/'});
				} else if(newVal==1) {
					$.cookie('recvpush', 'yes', {path:'/'});
				}
			}
		});
	});
	var $hRadio = $('#habit-wrap [type=radio]');
	$hRadio.click(function() {
		var $_this = $(this);
		var res = $_this.is(':checked');
		var tag = $_this.attr('data-tag');
		var newVal = $_this.attr('data-new-val');
		var $wrap = $('#habit-wrap');
		$wrap.prepend(loadingCoverHtml);
		$.ajax({
			url: '/user/modify_settings/',
			type: 'POST',
			data: {'tag':tag, 'new_val':newVal},
			success: function(callback) {
				itemFadeOut($wrap, '.loading-cover');
				//showTip('修改成功', 'success', $wrap);
			}
		});
	});
	

	
	
	
	//背景图片上传
	window.firstUpload = true;
	var manualUploader = new qq.FineUploader({
        element: document.getElementById('fine-uploader-gallery'),
        template: 'qq-template-gallery',
        request: {
            endpoint: '/user/upload_bg/'
        },
        callbacks: {
        	onAllComplete: function(success,error) {
        		if(success) {
        			manualUploader.reset();
        			showTip('更换背景成功', 'success', $('#fine-uploader-gallery>.qq-uploader-selector'));
        		} else {
        			showTip(error, 'danger', $('#fine-uploader-gallery>.qq-uploader-selector'));
        		}
        	}
        },
        
        thumbnails: {
            placeholders: {
                waitingPath: '/static/css/plugs/fineuploader/placeholders/waiting-generic.png',
                notAvailablePath: '/static/css/plugs/fineuploader/placeholders/not_available-generic.png'
            }
        },
        validation: {
            allowedExtensions: ['jpeg', 'jpg', 'png'],
        	sizeLimit: 10240000, // 10M
        	itemLimit: 1,
        	image: {
        		minWidth: 1920,
        		minHeight: 1080,
        	},
        	
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
        classes: {
            retrying: "qq-upload-retrying",
            retryable: "qq-upload-retryable",
            success: "qq-upload-success alert alert-success",
            fail: "qq-upload-fail alert alert-danger",
            editable: "qq-editable",
            hide: "qq-hide",
            dropActive: "qq-upload-drop-area-active"
        },
        text: {
            formatProgress: "进度：{percent}% / {total_size}",
            failUpload: "上传失败",
            waitingForResponse: "处理中..",
            paused: "已暂停"
        },
        autoUpload: false,
        debug: false,
    });
	
	qq(document.getElementById("trigger-upload")).attach("click", function() {
        manualUploader.uploadStoredFiles();
    });

});