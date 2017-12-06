#!/usr/bin/env python
import pika
import sys

job_description =''

if len(sys.argv)<2:
    print("Please Specify the job descriptor json file to run as argument to this script.")
    exit(1)
else:
    job_description = open(sys.argv[1],'r').read()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tasks')

channel.basic_publish(exchange='',
                      routing_key='tasks',
                      body=job_description)
print(" [x] Sending 'Job Description' to execute.")
print("Details:\n",str(job_description))
print("Success.")
connection.close()