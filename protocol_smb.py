import smbclient

name_host = r''
user = ''
secret = ''
host = ""
name_server = ""

try:
    smbclient.register_session(server=name_server, username=user, password=secret,
                               port=445, connection_timeout=30)
    print("connected!")
    try:
        with smbclient.open_file(r"\\TEST-SERVER-MAC\Users\tester\Documents\smb_folder\hello.txt", mode='w') as f:
            f.write('hello world')
        print('successfully writing in file!\nAnd this is command "dir": ')
        print(smbclient.listdir(r"\\TEST-SERVER-MAC\Users\tester\Documents\smb_folder"))
    except:
        print("error with writing")
    smbclient.delete_session(server=name_server, port=445)
except:
    print('Something is wrong\n')
