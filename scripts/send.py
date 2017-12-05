
#!/usr/bin/env python
import pika
import sys

command =''

if len(sys.argv)<2:
    print("Please Specify the command (as a single string) to run as argument to this script.")
    exit(1)
else:
    command = ' '.join(str(x) for x in sys.argv[1:])

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=command)
print(" [x] Sent 'Hello World!'")
connection.close()