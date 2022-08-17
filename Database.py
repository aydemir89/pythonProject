import mysql.connector
from mysql.connector import Error
import json
import sys
import time,os

SenderisChanged = False
def main():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='aiopsdb',
                                             user='root',
                                             password='root')
        if connection.is_connected():


            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            # Opening JSON file
            f = open('data.json')

            # returns JSON object as
            # a dictionary
            data = json.load(f)
            print(data)

            add_usageofserver = ("INSERT INTO usageserver "
                            "(id, SPH, UOM, UOC, IsPdfSend) "
                            "VALUES (%(id)s, %(SPH)s, %(UOM)s, %(UOC)s, %(IsPdfSend)s)")

            cursor.execute(add_usageofserver, data)
            connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

            print("MySQL connection is closed")
def whileFunctionSender():
    global SenderisChanged
    while True:
        if(SenderisChanged):
            SenderisChanged=False
        else:
            time.sleep(0.2)

    t1 = threading.Thread(target=whileFunctionSender, args=(lambda: SenderisChanged,))
    t1.start()

if __name__ == 'main':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)