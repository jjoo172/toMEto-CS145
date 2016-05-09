$(function() {
    $('#btnSearch').click(function() {
        $.ajax({
            url: '/simplesearch',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});