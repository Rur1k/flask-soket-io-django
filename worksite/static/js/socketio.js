$(document).ready(function(){
    var socket = io.connect('http://127.0.0.1:5000');

//    socket.on('connect', function() {
//        console.log('Работает')
//        socket.send('User has connected!');
//    });
//
//    socket.on('message', function(msg){
//        $('#chat-id').append(
//            '<li class="chat-left"><div class="chat-avatar"><img src="https://www.bootdey.com/img/Content/avatar/avatar3.png" alt="Retail Admin">'
//            +'<div class="chat-name">'+msg.user_name+'</div></div><div class="chat-text">'+msg.message+'</div><div class="chat-hour">08:55</div></li>'
//        )
//    })
//
//    $('#send-message').on('click', function(e){
//        e.preventDefault();
//        console.log('Сообщение отправлено!');
//
//        let user_name = $('#username').val();
//        console.log('user_name');
//        let user_input = $('#message-text').val();
//        console.log('user_input');
//
//        socket.send('message', {
//            user_name: user_name,
//            message: user_input
//        });
//
//        $('#message-text').val('').focus();
//    });



    socket.on('connect', function() {
        socket.emit('message', {data: 'User Connected'});
        var send_message = $('#send-message').on('click', function(e){
            e.preventDefault();
            console.log('Сообщение отправлено!');

            socket.emit('message', {
                user_name: $('#username').val(),
                message: encodeURIComponent($('#message-text').val())
            });


            $('#message-text').val('').focus();
        });
    });

    socket.on('send_message', function(msg){
        var date = new Date()

        if(typeof msg.user_name !== 'undefined'){
            $('#chat-id').append(
                '<li class="chat-right">'
                +'<div class="chat-hour">'+date.getHours()+':'+date.getMinutes()+':'+date.getSeconds()+'</div>'
                +'<div class="chat-text">'+decodeURIComponent(msg.message)+'</div>'
                +'<div class="chat-avatar">'
                +'<img src="https://www.bootdey.com/img/Content/avatar/avatar4.png" alt="Retail Admin">'
                +'<div class="chat-name">'+msg.user_name+'</div>'
                +'</div>'
                +'</li>'
            )
        }
    })

});


