$(document).ready(function(){

    var scroll_obj = document.getElementById("chat-id");
    scroll_obj.scrollTop = scroll_obj.scrollHeight;

    var socket = io.connect('http://127.0.0.1:5000');
    var customer_id = $('#customer_id').val();
    var executor_id = $('#executor_id').val();
    var room = 'c_'+customer_id+'e_'+executor_id;

    socket.on('connect', function() {
        socket.emit('join', {
            'username': $('#username').val(),
            'room': room
        })


        var send_message = $('#send-message').on('click', function(e){
            e.preventDefault();

            socket.emit('message', {
                user_name: $('#username').val(),
                message: encodeURIComponent($('#message-text').val()),
                room: room,
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
        scroll_obj.scrollTop = scroll_obj.scrollHeight;
    });

    socket.on('join_message', function(msg){
        $('#chat-id').append(
                '<li class="text-center"><div>'+'Пользователь <b>'+msg['username']+'</b>, подключился к чату.'+'</div></li>'
            );

        var chat_users = document.getElementsByClassName('chat-username')
        var name_list = []


        for (var i=0; i<chat_users.length; i++){
            name_list.push(chat_users[i].innerText)
        }

        if(name_list.includes(msg['username']) == false){
            $('#users').append(
                        '<li id="'+msg['username']+'" class="person" data-chat="person1">'
                        +'<div class="user">'
                        +'<img src="https://www.bootdey.com/img/Content/avatar/avatar1.png" alt="Retail Admin">'
                        +'</div>'
                        +'<p class="name-time">'
                        +'<span class="name">'+msg['username']+'</span>'
                        +'</p>'
                        +'</li>'
                    );
        }

        scroll_obj.scrollTop = scroll_obj.scrollHeight;
    });


    socket.on('leave_message', function(msg){
        $('#chat-id').append(
                '<li class="text-center"><div>'+'Пользователь <b>'+msg['username']+'</b>, покинул чат.'+'</div></li>'
            );

        document.getElementById(msg['username']).remove()

        scroll_obj.scrollTop = scroll_obj.scrollHeight;
    });

    window.onbeforeunload = function(e){
        socket.emit('leave', {
                'username': $('#username').val(),
                'room': room,
            })
    }

});
