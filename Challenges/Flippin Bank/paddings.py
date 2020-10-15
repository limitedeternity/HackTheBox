from enum import Enum
import random


class Padding(Enum):
    No = 0
    Zero = 1
    ANSI_X923 = 2
    ISO_10126 = 3
    PKCS7 = 4
    PKCS5 = 5
    ISOIEC_78164 = 6


def __random_bytes(n):
    return "".join([chr(random.randint(0, 255)) for _ in range(n)])


def pad(msg, block_size, padding=Padding.Zero):
    if padding == Padding.PKCS5:
        block_size = 8

    pad_size = block_size - (len(msg) % block_size)
    if pad_size == 16:
        pad_size = block_size

    if padding == Padding.Zero:
        return msg + "\0" * pad_size
    elif padding == Padding.ANSI_X923:
        return msg + "\0" * (pad_size - 1) + chr(pad_size)
    elif padding == Padding.ISO_10126:
        return msg + __random_bytes(pad_size - 1) + chr(pad_size)
    elif padding == Padding.ISOIEC_78164:
        return msg + chr(0x80) + "\x00" * (pad_size - 1)
    elif padding == Padding.PKCS7:
        return msg + chr(pad_size) * pad_size
    elif padding == Padding.PKCS5:
        return msg + chr(pad_size) * pad_size

    return msg


def unpad(msg, block_size, padding=Padding.Zero):
    if padding == Padding.PKCS5:
        block_size = 8

    msg_size = len(msg)

    if padding == Padding.Zero:
        msg_size = msg.rfind("\0")
    elif padding == Padding.ANSI_X923:
        msg_size -= ord(msg[-1])
    elif padding == Padding.ISO_10126:
        msg_size -= ord(msg[-1])
    elif padding == Padding.ISOIEC_78164:
        msg_size = msg.rfind("\x80")
    elif padding == Padding.PKCS7:
        msg_size -= ord(msg[-1])
    elif padding == Padding.PKCS5:
        msg_size -= ord(msg[-1])

    if msg_size == -1:
        return msg
    else:
        return msg[:msg_size]
