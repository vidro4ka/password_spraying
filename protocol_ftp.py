import ftplib
import socket
from ftplib import Error
from colorama import Fore, init

init(autoreset=True)

def con_ftp(host, user, secret):
    s = False
    try:
        session = ftplib.FTP(host=host,
                             user=user,
                             passwd=secret)

        s = True
        print(Fore.LIGHTGREEN_EX + "->  host:", str(host), Fore.LIGHTGREEN_EX + "login:", str(user),
              Fore.LIGHTGREEN_EX + "password:",
              str(secret))
        directory = session.nlst()
        print(directory)
    except Error:
        print(Fore.RED + "->  host:", str(host), Fore.RED + "login:", str(user),
              Fore.RED + "password:",
              str(secret))
    except TimeoutError:
        print(Fore.RED + "->  host:", str(host), Fore.RED + "login:", str(user),
              Fore.RED + "password:",
              str(secret))
    except socket.gaierror:
        print(Fore.RED + "->  host:", str(host), Fore.RED + "login:", str(user),
              Fore.RED + "password:",
              str(secret))
    finally:
        if s:
            session.close()
            print(Fore.YELLOW + "-> Session has been closed")

