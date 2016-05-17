$(function() {
    $('#btnSearch').click(function() {
        $('#loading_img').show();
        $.ajax({
            url: '/simplesearch',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $('#loading_img').hide();
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

