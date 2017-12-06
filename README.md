@author Sagar Kar

## A RabbitMq based job queying system to run docker as jobs.

Todo:
- [x] Make the function to passs messages
- [x] Make the docker command take basic arguments and run
- [x] Make the entire pipeline work
- [ ] Pretty print the output from PIPE
- [x] Make the MEMORY requirement check
- [ ] Make the CPU requirement check
- [ ] Make sure about the CPU and CMD examples
- [ ] Make the process work with decoding the '\n' as arbitary blank symbol from pipe.
- [ ] Remove Dependency from shlex

Requirements:
-python3
-pika (pip)
-rabbitmq (unix)

Remarks:
1. Learned about RabbitMQ
2. Made the docker run work wihout docker compose and understood the underying concept
3. Difficulty in the Popen Output. Pretty nasty.

File Structure:

    .
    ├── job_desc (all sample job description holds here)
    │   ├── job_desc_1.json
    │   └── job_desc_2.json
    ├── notebooks (scrap notebooks for testing)
    │   └── rabbitmqSample.ipynb
    ├── README.md
    └── scripts (the fileterd scripts)
        ├── cpu_usage.sh
        ├── mem_check.sh
        ├── receive.py (worker)
        └── send.py (client)


# Project Description:
## Job Queue

Create a job queue. It consists of two parts: **a worker** and **a client**.

Each job consists of:
1. a docker image
1. an array of cmd parameters to pass to the image
1. a dictionary of environment variables to pass to the image
1. a dictionary of cpu and memory requirements

The client takes the above details and enqueues the job.

A worker then pops the jobs from the queue and runs them.

Notes:
- There are no restrictions on how long a task can run; Some may finish in weeks while others may run for weeks.
- Assume jobs are idempotent; Each job should be run at least once.
- Each worker should take cpu and memory available as inputs when it's started.
- A worker should simultaneously run as many jobs as possible without overrunning either the cpu or the memory available
- We must be able to run multiple workers with different cpu and memory availability simultaneously.
