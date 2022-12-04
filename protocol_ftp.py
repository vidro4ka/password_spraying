import ftplib
from ftplib import Error

#home
#host = ""

#for presentation
host = ""
user = ''
secret = ''
session = False

try:
    session = ftplib.FTP(host=host,
                         user=user,
                         passwd=secret)
    directory = session.nlst()
    print(directory)
except Error as error:
    print("Something is wrong")
finally:
    if session:
        session.close()
        print("Session has closed")
