import subprocess as s
import shlex
cmd="sudo docker run -it ubuntu /bin/sh -c 'env'"
process = s.Popen(shlex.split(cmd),stdout=s.PIPE,universal_newlines=True)
output = ''
print("a\nb")
while True:
    op = process.stdout.readline()
    print(op,end="")
    print('a\nb')
    if process.poll() is not None:
        break

