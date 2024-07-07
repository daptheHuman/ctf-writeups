#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.39.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("chal-lz56g6.wanictf.org", 9005)

    return r


def main():
    r = conn()

    r.interactive()


if __name__ == "__main__":
    main()
