
import requests
from requests.auth import HTTPBasicAuth

user = ''
secret = ''
url = ''

session = requests.get(url=url, auth=HTTPBasicAuth(username=user, password=secret))

if session:
    print(session.status_code, 'Connected!!!')
    print("Some info: \n", session.text)
else:
    print("Not connected :(")
print(session.status_code)
