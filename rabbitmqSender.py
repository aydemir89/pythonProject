import sys
import time,os

import pika
import json

SenderisChanged = False
data = {}

def main():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue="hello11")
        with open('data.json') as file:
            data = json.load(file)
        global SenderisChanged
        SenderisChanged = True
        channel.basic_publish(exchange='', routing_key='hello11', body=json.dumps(data))
        print(" [x] Sent 'Hello World!'")
        connection.close()

def whileFunctionSender():
    global SenderisChanged
    while True:
        if(SenderisChanged):
            SenderisChanged=False
        else:
            time.sleep(0.2)

    t1 = threading.Thread(target=whileFunctionSender, args=(lambda: SenderisChanged,))
    t1.start()

""""React ta soket yapısı olacak."""

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
