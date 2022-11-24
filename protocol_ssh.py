# completed
import time
import paramiko
from paramiko import SSHException

host = '13.50.18.243'
user = 'bandit0'
secret = 'bandit0'
port = 2220
session = False

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(hostname=host,
                   username=user,
                   password=secret,
                   port=port)
    channel_1 = client.invoke_shell()
    channel_1.send('ls -l\n')
    time.sleep(2)
    output = channel_1.recv(5000)
    print(output.decode())
    session = True
except (Exception, SSHException) as error:
    print("Something wrong!!!")
finally:
    if session:
        client.close()
        print("---------------------")
        print("Session has closed!!!")
