

$(function () {
    $('#ss-form').submit(function (e) {
        e.preventDefault();
        var $this = $(this);
        var $input = $('#answer-input');
        var $inputGroup = $input.parent();
        if (!$input.val()) {
            return false;
        }
        $inputGroup.find('button').attr('disabled');
        $.ajax({
            url: $this.attr('action'),
            data: {'name': $input.val()},
            type: $this.attr('method'),
            success: function (callback) {
                var obj = $.parseJSON(callback);
                $inputGroup.css('width', '100%').css('color', 'white').css('font-size', '32px');
                var password;
                if (obj.success) {
                    password = obj.data.password;
                } else {
                    password = 'Incorrect answer!'
                }
                $inputGroup.html('<div>' + password +'</div>')
            }
        });
    });
});