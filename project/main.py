import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
import datetime
import hashlib

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


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('my event')
def handler_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)

