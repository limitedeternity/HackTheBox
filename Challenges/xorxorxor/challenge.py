#!/usr/bin/python3

output = bytes.fromhex(open('output.txt', 'r').read().strip())

class XOR:
    def __init__(self, key: bytes):
        assert len(key) == 4
        self.key = key

    def encrypt(self, data: bytes) -> bytes:
        xored = b''
        for i in range(len(data)):
            xored += bytes([data[i] ^ self.key[i % len(self.key)]])
        return xored

    def decrypt(self, data: bytes) -> bytes:
        return self.encrypt(data)

def main():
    zero_shift = XOR(b'\x00' * 4).decrypt(output)[:4]
    key = XOR(zero_shift).encrypt(b'HTB{')
    print('Flag: ', XOR(key).decrypt(output))

if __name__ == '__main__':
    main()
