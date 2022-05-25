import mongoengine as me
import datetime


class User(me.Document):
    user_id = me.IntField(primary_key=True)
    username = me.StringField(required=True)
    password = me.StringField(max_length=255)
    email = me.EmailField(required=True)
    is_active = me.BooleanField(default=True)
    is_staff = me.BooleanField(default=False)


class Chat(me.Document):
    chat_id = me.SequenceField()
    customer = me.ReferenceField(User)
    executor = me.ReferenceField(User)
    chat_name = me.StringField()
    date_create = me.DateTimeField(default=datetime.datetime.utcnow)
    is_general = me.BooleanField(default=False)


class ChatHistory(me.Document):
    message_id = me.SequenceField()
    chat = me.ReferenceField(Chat)
    author = me.ReferenceField(User)
    message = me.StringField()
    datetime = me.DateTimeField(default=datetime.datetime.utcnow)


class ChatUser(me.Document):
    chat = me.ReferenceField(Chat)
    user = me.ReferenceField(User)

