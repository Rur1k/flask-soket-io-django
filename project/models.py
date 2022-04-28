import mongoengine as me


class User(me.Document):
    user_id = me.IntField(primary_key=True)
    username = me.StringField(required=True)
    password = me.StringField(max_length=255)
    email = me.EmailField(required=True)
    is_active = me.BooleanField(default=True)
    is_staff = me.BooleanField(default=False)

