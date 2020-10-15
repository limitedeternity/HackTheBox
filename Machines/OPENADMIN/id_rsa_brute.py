#!/usr/bin/env python
import subprocess
import sys
import pipes


def cmdline(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return err


def main():
    if len(sys.argv) < 4:
        print("usage: {} <in_key> <dictionary> <out_key>".format(sys.argv[0]))
        return

    for password in map(lambda l: l.strip(), open(sys.argv[2])):
        if not password:
            continue

        strcmd = "openssl rsa -in {} -out {} -passin {}".format(sys.argv[1], sys.argv[3], pipes.quote("pass:" + password))
        res = cmdline(strcmd)
        if res.startswith("writing"):
            print("The key is: {}".format(password))
            return


if __name__ == '__main__':
    main()
