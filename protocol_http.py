import requests
import sys
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth

user = "testing_http"
secret = "l57daf"

try:
    response = requests.get("http://localhost:8080/test_floder", auth=HTTPBasicAuth(username=user, password=secret))
    stdoutOrigin = sys.stdout
    sys.stdout = open("output.txt", "w")

    if response.status_code != 200:
        print("Status code:", response.status_code, "Not connected ;(\n", response.text)
    else:
        print("Status code:", response.status_code, "Connected:\n", response.text)

    sys.stdout.close()
    sys.stdout = stdoutOrigin

    if response.status_code != 200:
        print("Status code:", response.status_code, "Not connected ;(\n", response.text)
    else:
        print("Status code:", response.status_code, "Connected:\n", response.text)
except(Exception, HTTPError) as error:
    print("Not connected :(", error)
