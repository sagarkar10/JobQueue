#!/usr/bin/env python
import pika
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f','--file', action='store',
                    dest='file_name',required=True,
                    help='Specify the job descriptor json file to run as argument to this script.')
args=parser.parse_args()
job_description = open(args.file_name,'r').read()

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
