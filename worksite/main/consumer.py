import json
import os
import sys

import pika
from .mongo_models import UserMongodb


def work_consumer():
    credentials = pika.PlainCredentials(username='admin', password='admin')
    mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
    mq_channel = mq_connection.channel()
    mq_channel.queue_declare(queue='user_queue', durable=True)

    def callback(ch, method, properties, body):
        jsonInstance = json.loads(body.decode('utf-8'))

        print(jsonInstance)

        user = UserMongodb.objects.using('mongo_database').filter(user_id=jsonInstance['id'])
        if user.first() is None:
            UserMongodb.objects.using('mongo_database').create(
                        user_id=jsonInstance['id'],
                        username=jsonInstance['username'],
                        password=jsonInstance['password'],
                        email=jsonInstance['email'],
                        is_active=jsonInstance['is_active'],
                        is_staff=jsonInstance['is_staff'],
                        created_at=jsonInstance['created_at'],
                        updated_at=jsonInstance['updated_at'],
                    )

    mq_channel.basic_consume(queue='user_queue', on_message_callback=callback, auto_ack=True)

    mq_channel.start_consuming()

work_consumer()

# if __name__ == '__main__':
#     try:
#         work_consumer()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)
