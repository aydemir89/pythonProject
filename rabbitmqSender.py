import pika
import json
import main

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue="AIOPS")
dictionary = {
        "id" : "62f3575ab51f8a773cde8ed1",
        "SPH" : 103,
        "PDF" : 1

}
channel.basic_publish(exchange='', routing_key='AIOPS', body=json.dumps(dictionary))
print(" [x] Sent 'Hello World!'")
connection.close()