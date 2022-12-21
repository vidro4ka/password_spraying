import requests
import sys
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
from colorama import Fore, init

init(autoreset=True)


def con_http(host, user, secret):
    s = False
    try:
        response = requests.get(host, auth=HTTPBasicAuth(username=user, password=secret))

        if response.status_code != 200:
            print(Fore.RED + "->  host:", str(host), Fore.RED + "login:", str(user),
                  Fore.RED + "password:",
                  str(secret))
        elif response.status_code == 200:
            s = True
            print(Fore.LIGHTGREEN_EX + "->  host:", str(host), Fore.LIGHTGREEN_EX + "login:", str(user),
                  Fore.LIGHTGREEN_EX + "password:",
                  str(secret))
            print("Some info: \n", response.text)
    except(Exception, HTTPError):
        print(Fore.RED + "->  host:", str(host), Fore.RED + "login:", str(user),
              Fore.RED + "password:",
              str(secret))
