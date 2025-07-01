import pika, json, os
from pymongo import MongoClient

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")

client = MongoClient(f"mongodb://{MONGO_HOST}:27017/")
db = client["query_db"]
users = db["users"]

def callback(ch, method, properties, body):
    event = json.loads(body)
    if event["type"] == "user.created":
        payload = event["payload"]
        users.insert_one({
            "_id": payload["email"],
            "name": payload["name"],
            "email": payload["email"]
        })
        print(f"[x] Usuario proyectado: {payload['email']}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

channel.exchange_declare(exchange='domain_events', exchange_type='topic', durable=True)
channel.queue_declare(queue='query_user_created', durable=True)
channel.queue_bind(exchange='domain_events', queue='query_user_created', routing_key='user.created')

channel.basic_consume(queue='query_user_created', on_message_callback=callback, auto_ack=True)
print("[*] Esperando eventos...")
channel.start_consuming()
