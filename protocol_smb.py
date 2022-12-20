import colorama
import smbclient
from colorama import Fore, init

init(autoreset=True)


def con_smb(name_server, user, secret):
    name_host = r'\\' + name_server + r'\Users\tester\Documents\smb_folder'
    s = False
    try:
        smbclient.register_session(server=name_server, username=user, password=secret,
                                   port=445, connection_timeout=30)
        s = True
        print(Fore.LIGHTGREEN_EX + "->  host:", str(name_server), Fore.LIGHTGREEN_EX + "login:", str(user),
              Fore.LIGHTGREEN_EX + "password:",
              str(secret))
        try:
            with smbclient.open_file(name_host + r'\hello.txt', mode='w') as f:
                f.write('hello world')
            print('successfully writing in file!\nAnd this is command "dir": ')
            print(smbclient.listdir(name_host))
        except:
            print(Fore.RED + "->  host:", str(name_server), Fore.RED + "login:", str(user),
                  Fore.RED + "password:",
                  str(secret))
        smbclient.delete_session(server=name_server, port=445)
    except:
        print(Fore.RED + "->  host:", str(name_server), Fore.RED + "login:", str(user),
              Fore.RED + "password:",
              str(secret))
