import os
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_mongoengine import MongoEngine
# from pymongo import MongoClient
from bson.objectid import ObjectId
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
# db.init_app(app)

socketio = SocketIO(app)


# Настройка подключения к БД и таблиц
# client = MongoClient('localhost', 27017, username='flaskAdmin', password='password')
# db = client.flask_db
# todos = db.todos
# tasks = db.tasks

class User(db.Document):
    user_id = db.IntField(primary_key=True)
    username = db.StringField(required=True)
    email = db.EmailField(required=True)
    is_active = db.BooleanField(default=True)
    is_staff = db.BooleanField(default=False)
    created_at = db.DateTimeField()
    updated_at = db.DateTimeField()


@app.route('/', methods=('GET', 'POST'))
def tasks():
    return render_template('tasks.html')



# @app.route("/users", methods=["POST"])
# def register():
#     new_user = request.get_json() # store the json body request
#     new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt password
#     doc = User.find_one({"username": newha256(_user["username"]}) # check if user exist
#     if not doc:
#         User.insert_one(new_user)
#         return jsonify({'msg': 'User created successfully'}), 201
#     else:
#         return jsonify({'msg': 'Username already exists'}), 409
#
#
# @app.route("/login", methods=["post"])
# def login():
#     login_details = request.get_json() # store the json body request
#     user_from_db = User.find_one({'username': login_details['username']})  # search for user in database
#
#     if user_from_db:
#         encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
#         if encrpted_password == user_from_db['password']:
#             access_token = create_access_token(identity=user_from_db['username']) # create jwt token
#             return jsonify(access_token=access_token), 200
#
#     return jsonify({'msg': 'The username or password is incorrect'}), 401

# Тестовые данные для настройки запсии с БД и работой с тодо листом
# @app.route('/todo', methods=('GET', 'POST'))
# def todo():
#     if request.method == 'POST':
#         content = request.form['content']
#         degree = request.form['degree']
#         todos.insert_one({'content': content, 'degree': degree})
#         return redirect(url_for('index'))
#
#     all_todos = todos.find()
#     return render_template('todo.html', todos=all_todos)
#
#
# @app.post('/todo/<id>/delete/')
# def todo_delete(id):
#     todos.delete_one({"_id": ObjectId(id)})
#     return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app)
