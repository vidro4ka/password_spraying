from smb.SMBConnection import SMBConnection, SMBError

host = ''
user = ''
secret = ''
port = 445
session = False

try:
    session = SMBConnection(username=user,
                            password=secret,
                            use_ntlm_v2=True)
    result = session.connect(host=host,
                             port=port)
    print("successfully")
    print(result)
except (Exception, SMBError) as error:
    print("Something wrong!!!")
finally:
    if session:
        session.close()
        print("Session has closed")
