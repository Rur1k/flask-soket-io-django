import json

import pika
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import User


@receiver(post_save, sender=User, weak=False)
def update_mongodb(sender, instance, **kwargs):
    credentials = pika.PlainCredentials(username='admin', password='admin')
    mq_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))

    mq_channel = mq_connection.channel()
    mq_channel.queue_declare(queue='user_queue', durable=True)

    jsonInstance = json.dumps(model_to_dict(instance)).encode('utf-8')

    mq_channel.basic_publish(exchange='', routing_key='user_queue', body=jsonInstance)

    mq_connection.close()


