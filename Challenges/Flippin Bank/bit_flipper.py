from paddings import *


def xor(a, b):
    return "".join([chr(ord(a[i]) ^ ord(b[i % len(b)])) for i in range(len(a))])


class BitFlipper:
    def __init__(self, ciphertext, plaintext, block_size=16):
        self._ciphertext = ciphertext
        self._block_size = block_size

        if len(ciphertext) % block_size != 0:
            raise Exception("Invalid ciphertext length or block size")

        self._plaintext = plaintext
        if len(self._plaintext) != len(ciphertext):
            raise Exception("Invalid plaintext length")

    def get_plaintext(self):
        return self._plaintext

    def get_ciphertext(self):
        return self._ciphertext

    def flip(self, a, b):
        if a not in self._plaintext:
            raise Exception("Unable to find occurence of %s in plaintext" % a)
        if len(a) != len(b):
            raise Exception("Data length mismatch")

        plaintextblock = [self._plaintext[i:i + self._block_size] for i in
                          range(0, len(self._plaintext), self._block_size)]

        offset = 0
        in_block = -1
        for i in range(len(plaintextblock)):
            if a in plaintextblock[i]:
                in_block = i
                offset = plaintextblock[i].find(a)
                break

        if in_block < 1 or len(a) > self._block_size:
            raise Exception("Bit Flipping attack cannot change consecutive blocks")

        modif = xor(a, b)
        pos = (in_block-1)*self._block_size + offset

        self._ciphertext = self._ciphertext[:pos] + xor(modif, self._ciphertext[pos:pos + len(a)]) + self._ciphertext[
                                                                                                     pos + len(a):]

        return self._ciphertext

    def __str__(self):
        return "<%s plaintext=%s>" % (self.__class__.__name__, self.get_plaintext())

    def __repr__(self):
        return "<%s plaintext=%s>" % (self.__class__.__name__, self.get_plaintext())
