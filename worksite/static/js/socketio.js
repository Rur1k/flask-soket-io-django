
var socket = io.connect('http://'+document.domain+':'+5000);
console.log(socket);


socket.on('connect', function() {
    socket.emit('my event', {data: 'User Connected'});
    console.log('Я работаю');
    var send_message = $('#send-message').on('click', function(e){
        e.preventDefault();
        console.log('Сообщение отправлено!');

        let user_name = $('#username').val();
        console.log('user_name');
        let user_input = $('#message-text').val();
        console.log('user_input');

        socket.emit('my event', {
            user_name: user_name,
            message: user_input
        });

        $('#message-text').val('').focus();
    });
});

socket.on('my response', function(msg){
    console.log(msg)
    if(typeof msg.user_name !== 'undefined'){
        $('#chat-id').append(
            '<li class="chat-left"><div class="chat-avatar"><img src="https://www.bootdey.com/img/Content/avatar/avatar3.png" alt="Retail Admin">'
            +'<div class="chat-name">'+msg.user_name+'</div></div><div class="chat-text">'+msg.message+'</div><div class="chat-hour">08:55</div></li>'
        )
    }
})
