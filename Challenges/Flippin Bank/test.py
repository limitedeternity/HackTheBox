#!/usr/bin/env python

from Crypto.Cipher import AES

from bit_flipper import *
from paddings import *
from binascii import unhexlify

def test():
    cleartext = "logged_username=xxxxx&password=g0ld3n_b0y"
    target = "xxxxx"
    replacement = "admin"

    print "Cleartext       :", cleartext, "(len=%d)" % len(cleartext)
    print "Target          :", cleartext.replace(target, replacement), "(len=%d)" % len(cleartext.replace(target, replacement))

    cleartext = pad(cleartext, AES.block_size, Padding.PKCS7)
    ciphertext = unhexlify(raw_input("Ciphertext      : "))

    dolphin = BitFlipper(ciphertext, cleartext, block_size=AES.block_size)
    dolphin.flip(target, replacement)
    flipped_ciphertext = dolphin.get_ciphertext()

    print "New ciphertext  :", flipped_ciphertext.encode("hex")

if __name__ == '__main__':
    test()
