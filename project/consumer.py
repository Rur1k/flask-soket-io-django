import json

import pika
from main import User


credentials = pika.PlainCredentials(username='admin', password='admin')
mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
mq_channel = mq_connection.channel()
mq_channel.queue_declare(queue='user_queue', durable=True)


def callback(ch, method, properties, body):
    jsonInstance = json.loads(body.decode('utf-8'))

    user = User.objects(user_id=jsonInstance['id']).first()

    if user is None:
        create_user = User(
            user_id=jsonInstance['id'],
            username=jsonInstance['username'],
            password=jsonInstance['password'],
            email=jsonInstance['email'],
            is_active=jsonInstance['is_active'],
            is_staff=jsonInstance['is_staff'],
        )

        create_user.save()


mq_channel.basic_consume(queue='user_queue', on_message_callback=callback, auto_ack=True)

mq_channel.start_consuming()

