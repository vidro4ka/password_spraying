from winrm import Session

host = ''
user = ''
secret = ''

session = Session(host=host,
                  auth=(user, secret))
if session:
    print("Successfully connected!!!")
    r = session.run_cmd('ipconfig', ['/all'])
else:
    print("Something wrong!!!")
