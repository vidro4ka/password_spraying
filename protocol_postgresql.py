import colorama
import psycopg2
from psycopg2 import Error
from colorama import Fore, init

init(autoreset=True)


def con_psgrsql(host, user, secret, datab_name):
    global session, cursor
    s = False
    try:
        session = psycopg2.connect(user=user,
                                   password=secret,
                                   host=host,
                                   dbname=datab_name)
        s = True
        print(Fore.LIGHTGREEN_EX + "->  host:", str(host), Fore.LIGHTGREEN_EX + "database name:", str(datab_name),
              Fore.LIGHTGREEN_EX + "login:", str(user),
              Fore.LIGHTGREEN_EX + "password:",
              str(secret))
        cursor = session.cursor()
        print("-> Some info about PostgreSQL: \n", session.get_dsn_parameters(), "\n")
    except (Exception, Error):
        print(Fore.RED + "->  host:", str(host), Fore.RED + "database name:", str(datab_name),
              Fore.RED + "login:", str(user),
              Fore.RED + "password:",
              str(secret))
    finally:
        if s:
            cursor.close()
            session.close()
            print(colorama.Fore.YELLOW + "-> Connection with PostgreSQL has closed")
