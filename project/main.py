import os
import datetime
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO, send, join_room, leave_room
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from urllib.parse import unquote
from models import ChatHistory, User


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


@app.route('/chat_history')
def chatHistory():
    messages = ChatHistory.objects()
    print(messages)
    return jsonify(messages)


@socketio.on('message')
def handle_message(json):
    print(unquote(str(json)))
    print(json.get('user_name'))

    user = User.objects(username=json.get('user_name')).first()
    if user:
        create_message = ChatHistory(author=user, message=unquote(str(json.get('message'))))
        create_message.save()

    socketio.emit('send_message', json)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send({'msg': username + 'has joined the'+room+'room'}, room=room)


@socketio.on('leave')
def on_leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + 'has left the'+data['room']+'room'}, room=data['room'])




if __name__ == '__main__':
    socketio.run(app, debug=True)

