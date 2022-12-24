import colorama
import winrm
from requests.exceptions import HTTPError
from colorama import Fore, init

init(autoreset=True)


def con_winrm(host, user, secret):
    try:
        s = winrm.Session(host, auth=(user, secret))
        try:
            r = s.run_ps('whoami')
            print(Fore.LIGHTGREEN_EX + '-> host:', str(host),
                  Fore.LIGHTGREEN_EX + 'login:', str(user),
                  Fore.LIGHTGREEN_EX + 'password:', str(secret))
            print(r.std_out)
            r = s.run_ps('ipconfig')
            print(r.std_out)
        except(Exception, HTTPError):
            print(Fore.LIGHTRED_EX + '-> host:', str(host),
                  Fore.LIGHTRED_EX + 'login:', str(user),
                  Fore.LIGHTRED_EX + 'password:', str(secret))

    except(Exception, HTTPError):
        print(Fore.LIGHTRED_EX + '-> host:', str(host),
              Fore.LIGHTRED_EX + 'login:', str(user),
              Fore.LIGHTRED_EX + 'password:', str(secret))
