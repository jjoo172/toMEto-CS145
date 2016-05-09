$(function() {
    $('#searchButton').click(function() {
        alert('donezo');
        $.ajax({
            url: '/landingSignUp',
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