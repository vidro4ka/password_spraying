import colorama
import winrm
from requests.exceptions import HTTPError
from colorama import Fore, init

init(autoreset=True)


def con_winrm(host, user, secret):
    try:
        s = winrm.Session(host, auth=(user, secret))
        print(Fore.LIGHTGREEN_EX + "->  host:", str(host), Fore.LIGHTGREEN_EX + "login:", str(user),
              Fore.LIGHTGREEN_EX + "password:",
              str(secret))
        r = s.run_ps('whoami')
        print(r.std_out)
        r = s.run_ps('ipconfig')
        print(r.std_out)
    except(Exception, HTTPError) as error:
        print(Fore.RED + "-> Something is wrong", str(error))
