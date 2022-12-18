# completed
import mysql.connector
from colorama import Fore, init

init(autoreset=True)

def con_msql(host, user, secret, datab_name):
    s = False
    try:
        session = mysql.connector.connect(
            host=host,
            user=user,
            password=secret,
            database=datab_name,
            port=3306
        )
        print(Fore.LIGHTGREEN_EX + "->  host:", str(host), Fore.LIGHTGREEN_EX + "database name:", str(datab_name), Fore.LIGHTGREEN_EX + "login:", str(user),
              Fore.LIGHTGREEN_EX + "password:",
              str(secret))
        s = True
        cur = session.cursor()
        cur.execute("SELECT VERSION()")

        version = cur.fetchone()

        print("Database version: {}".format(version[0]))
    except (Exception, mysql.connector.Error) as error:
        print(Fore.RED + "-> Something wrong: \n", str(error))
    finally:
        if s:
            session.close()
            print(Fore.YELLOW + "-> Session has closed")
