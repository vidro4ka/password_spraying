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
            print(Fore.RED + "-> Status code:", str(response.status_code), "Not connected ;(\n",
                  str(response.text))
        elif response.status_code == 200:
            s = True
            print(Fore.LIGHTGREEN_EX + "->  host:", str(host), Fore.LIGHTGREEN_EX + "login:", str(user),
                  Fore.LIGHTGREEN_EX + "password:",
                  str(secret))
            print(Fore.LIGHTGREEN_EX + "-> Status code:", str(response.status_code), str(response.text))
    except(Exception, HTTPError) as error:
        print(Fore.RED + "-> Not connected :(", str(error))
