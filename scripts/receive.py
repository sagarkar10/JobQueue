#!/usr/bin/env python
import pika
import shlex
import subprocess

def run_command(command):
    try:
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    except FileNotFoundError as e:
        print(e)
        return (-1)
        
    while True:
        output = process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            break
        if output:
            print (output.strip())
    rc = process.poll()
    return rc

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Command to Run %r" % body)
    run_command(body.decode("utf-8") )
    print("Finished...")

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()