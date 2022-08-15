import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue="hello11")

with open('data.json') as file:
    data = json.load(file)

channel.basic_publish(exchange='', routing_key='hello11', body=json.dumps(data))
print(" [x] Sent 'Hello World!'")

connection.close()