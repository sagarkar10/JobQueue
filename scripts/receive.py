#!/usr/bin/env python
import pika
import shlex
import subprocess
import re
import pprint
import argparse

parser = argparse.ArgumentParser('Arguments for The receive.py')
parser.add_argument('-d','--deamonize', help='Detach the job dockers to background and return the ID', action='store_true', dest='is_daemon')
args =  parser.parse_args()

def run_command(command):
    try:
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, universal_newlines=True)
    except FileNotFoundError as e:
        print(e)
        return (-1)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc

def env_str(env_dic):
    env_string=""
    for x,y in env_dic.items():
        env_string =env_string+" --env "+x+"="+y 
    return env_string.strip()

def generate_cmd(job_description,is_daemon=True):

    if is_daemon:
        print("The receiving dockers would be daemonised and the Container ID would be returned")
        command = 'docker run -d '
    else:
        command = 'docker run '

    req_keys = ['image', 'cmd']
    mem_req = None
    invalid = False
    
    for k in req_keys:
        if k not in job_description.keys():
            print("Job description not valid.")
            print("Missing",k)
            invalid=True
    
    if 'res_req' in job_description.keys():
        if 'memory' in job_description['res_req'] and type(job_description['res_req']['memory'])==int:
            mem_req = job_description['res_req']['memory']
        else:
            print("No memory reqirement mentioned, checking againt difined buffer only.")
            print("Check memory representation must be an number in kb")
            print("Continuing...")
            
    if invalid==True or is_mem_available(mem_req)==False:
        print('Failed to generate Command...')
        if is_mem_available(mem_req)==False:
            print('Not suffuciant Memory Available. Note buffer is 10000kb by default')
        return None
    
    if 'env' in job_description.keys():
        command = command + env_str(job_description['env'])
    command =command+ " -i "+job_description['image']+" /bin/bash -c \""+ str(' '.join(e for e in job_description['cmd']))+"\" " 
    return command

def is_mem_available(r_mem_kb, buffer_kb=100000):
    if r_mem_kb==None:
        r_mem_kb = 0
    meminfo = open('/proc/meminfo').read()
    match = re.findall('MemFree:.*',meminfo)[0]
    a_mem_kb = int(match.split()[1])
    if r_mem_kb+buffer_kb < a_mem_kb:
        return True
    else:
        return False

is_daemon = args.is_daemon
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tasks')

def callback(ch, method, properties, body):
    global is_daemon
    job_desc = eval(body.decode("utf-8"))
    print(" [x] Job description:")
    command = generate_cmd(job_desc, is_daemon)
    print(command)
    if command:
        run_command(command)
#         print()
    print("Finished...")

channel.basic_consume(callback,
                      queue='tasks',
                      no_ack=True)

print(' [*] Waiting for New Job. To exit press CTRL+C')
channel.start_consuming()
