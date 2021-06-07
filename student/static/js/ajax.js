$(document).ready(function() {
    console.log('ready')
    $('.vote').click(function(){

        $.ajax({
            type:'GET',
            url: '/students/ajax/vote',
            success: function(data) {
                for(i=0; i < data.length; i++) {
                    $('.votes').append('ppp')
                }
            }
        });

    });
});