import winrm
from requests.exceptions import HTTPError

host = ''
user = ''
secret = ''
try:
    s = winrm.Session(host, auth=(user, secret))
    r = s.run_ps('whoami')
    print(r.std_out)
    r = s.run_ps('ipconfig')
    print(r.std_out)
except(Exception, HTTPError) as error:
    print(error)

