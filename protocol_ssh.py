import time
import colorama
import paramiko
from paramiko import SSHException
from colorama import Fore, init

init(autoreset=True)


def con_ssh(host, user, secret):
    port = 2220
    s = False
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host,
                       username=user,
                       password=secret,
                       port=port)
        print(Fore.LIGHTGREEN_EX + "->  host:", str(host), Fore.LIGHTGREEN_EX + "login:", str(user),
              Fore.LIGHTGREEN_EX + "password:",
              str(secret))
        channel_1 = client.invoke_shell()
        channel_1.send('ls -l\n')
        time.sleep(2)
        output = channel_1.recv(5000)
        print(output.decode())
        s = True
    except (Exception, SSHException):
        print(Fore.RED + "->  host:", str(host), Fore.RED + "login:", str(user),
              Fore.RED + "password:",
              str(secret))
    finally:
        if s:
            client.close()
            print(colorama.Fore.YELLOW + "-> Session has closed!!!")
