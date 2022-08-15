import pika
import json
import main


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue="SenderMessage")

dictionary = {
    "id": "62f3575ab51f8a773cde8ed1",
    "SPH": main.SPH,
    "UOM": main.prediction_pdf1[0][0],
    "UOC": main.prediction_pdf[0][0],
    "IsPdfSend": main.IsPdfSend
}
channel.basic_publish(exchange='', routing_key='SenderMessage', body=json.dumps(dictionary))
print(" [x] Sent 'Hello World!'")
connection.close()