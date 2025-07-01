# app/producer.py
import pika
import json
import os

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.exchange_declare(exchange='domain_events', exchange_type='topic', durable=True)

def publish_user_created(event: dict):
    routing_key = "user.created"
    message = json.dumps(event)
    channel.basic_publish(
        exchange='domain_events',
        routing_key=routing_key,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2  # make message persistent
        )
    )
