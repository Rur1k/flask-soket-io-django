import os
import datetime
from flask import Flask, jsonify, session
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO, send, join_room, leave_room
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from urllib.parse import unquote
from models import ChatHistory, User, Chat, ChatUser

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('TOKEN')
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['MONGODB_SETTINGS'] = {
    'db': 'flask_db',
    'host': 'localhost',
    'port': 27017,
    'username': 'flaskAdmin',
    'password': 'password'
}

db = MongoEngine(app)
jwt = JWTManager(app)

socketio = SocketIO(app, cors_allowed_origins="*")

ROOMS = ['General']
users = {}


def generate_chat(roomname):
    if roomname == 'General':
        chat = Chat.objects(is_general=True).first()
        if chat:
            return chat
        else:
            create_chat = Chat(is_general=True)
            create_chat.save()
            generate_chat(roomname)
    else:
        chat = Chat.objects(chat_name=roomname).first()
        if chat:
            return chat
        else:
            create_chat = Chat(chat_name=roomname)
            create_chat.save()
            generate_chat(roomname)


def add_user_to_chat(chat, user):
    if chat and user:
        is_chat_user = ChatUser.objects(chat=chat, user=user).first()
        if is_chat_user is None:
            create_chat_user = ChatUser(chat=chat, user=user)
            create_chat_user.save()


def delete_user_in_chat(chat, user):
    if chat and user:
        is_chat_user = ChatUser.objects(chat=chat, user=user).first()
        if is_chat_user:
            is_chat_user.delete()


@app.route('/chat_history')
def chatHistory():
    chat = generate_chat('General')
    objects = ChatHistory.objects(chat=chat)

    message_list = []
    for obj in objects:
        message = {
            'message_id': obj['message_id'],
            'author_id': obj['author'].user_id,
            'author': obj['author'].username,
            'message': obj['message']
        }
        message_list.append(message)
    return jsonify(message_list)


@app.route('/chat_history/customer=<int:customer>&executor=<int:executor>')
def privateChatHistory(customer, executor):
    room = f'c_{customer}e_{executor}'
    chat = generate_chat(room)

    objects = ChatHistory.objects(chat=chat)

    message_list = []
    for obj in objects:
        message = {
            'message_id': obj['message_id'],
            'author_id': obj['author'].user_id,
            'author': obj['author'].username,
            'message': obj['message']
        }
        message_list.append(message)
    return jsonify(message_list)


@app.route('/chat_users/customer=<int:customer>&executor=<int:executor>')
def privateChatUser(customer, executor):
    room = f'c_{customer}e_{executor}'
    chat = generate_chat(room)
    objects = ChatUser.objects(chat=chat)

    message_list = []
    for obj in objects:
        message = {
            'user_id': obj['user'].user_id,
            'user': obj['user'].username,
        }
        message_list.append(message)
    return jsonify(message_list)


@socketio.on('message')
def handle_message(json):
    user = User.objects(username=json.get('user_name')).first()
    chat = generate_chat(json.get('room'))

    if user:
        create_message = ChatHistory(author=user, message=unquote(str(json.get('message'))), chat=chat)
        create_message.save()

    socketio.emit('send_message', json, room=json.get('room'))


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']

    user = User.objects(username=username).first()
    chat = generate_chat(room)
    add_user_to_chat(chat, user)

    join_room(room)
    socketio.emit('join_message', data, room=room)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']

    user = User.objects(username=username).first()
    chat = generate_chat(room)
    delete_user_in_chat(chat, user)

    leave_room(room)
    socketio.emit('leave_message', data, room=data['room'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
