import pika, sys, os
import json
import time
import threading
import pika


isChanged = False
x = 0
y = 0
def main():




    def channel(alive):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='SPHTOPYTHON')



        def callback(ch, method, properties, body):

            json_object = json.loads(body)
            print(json_object["SPH"])
            global x
            global y
            x = json_object["SPH"]
            y = json_object["IsPdfSend"]
            print(y)
            global isChanged
            isChanged = True


        channel.basic_consume(queue='SPHTOPYTHON', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()


    print(' [*] Waiting for messages. To exit press CTRL+C')


    def whileFunction(x,y):
        global isChanged

        while True:
            if(isChanged):
                print("test ", x(),y())
                isChanged = False
            else:

                time.sleep(0.2)


    t1 = threading.Thread(target=channel,args=(lambda: isChanged,))
    t2 = threading.Thread(target=whileFunction,args=(lambda: x,lambda :y,))

    t1.start()
    t2.start()




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
            
