import subprocess
import sys

def cmdline(command):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return err

def main():
    if len(sys.argv) < 4:
        print("usage: {} <in_key> <dictionary> <out_key>".format(sys.argv[0]))
        return

    count = 0
    for password in map(lambda l: l.strip(), open(sys.argv[2])):
        strcmd = "openssl rsa -in {} -out {} -passin pass:{}".format(sys.argv[1], sys.argv[3], password)
        res = cmdline(strcmd)
        if res.startswith("writing"):
            print("The key is: {}".format(password))
            return

        count += 1

if __name__ == '__main__':
    main()
