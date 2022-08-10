import pika
import main


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='AIOPS')

def callback(ch, method, properties, body):
   print("Received %r" % body)

channel.basic_consume(
   queue='AIOPS', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()