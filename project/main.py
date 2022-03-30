import os
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_socketio import SocketIO
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('TOKEN')
socketio = SocketIO(app)

# Настройка подключения к БД и таблиц
client = MongoClient('localhost', 27017, username='flaskAdmin', password='password')
db = client.flask_db
# todos = db.todos
tasks = db.tasks


@app.route('/', methods=('GET', 'POST'))
def tasks():
    return render_template('tasks.html')


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