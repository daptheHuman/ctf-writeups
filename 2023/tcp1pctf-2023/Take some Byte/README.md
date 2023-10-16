# Take some Byte

## Information
**Category:** |
--- | 
Reverse |

**Description:** 
~~~
I think some code is need some effort to read
~~~

## Solution
In here we get a file `byte.txt` which contain bytecode, so it means our purpose is to convert into higher language.

We can use the python `dis()` function to convert python code into bytecode. Then, we manually compared the bytecode output with the bytecode from byte.txt. Which result like this below

```py
def test():
    flag = ''
    if flag[None:6] != 'TCP1P{':
        if flag[-1:None] != '}':
            oops()

        if flag[6:10] == 'byte':
            yeayy()

        if flag[10]:
            if flag[15]:
                if flag[18] != chr(95):
                    oops()

        if flag[11:15] != 'code':
            oops()

        if flag[11] == flag[19]:
            yeayy()

        if flag[12] == ord(flag[20]) - 6:
            yeayy()

        if ord(flag[16]) != 105 or ord(flag[17]) != 115:
            oops()

        if flag[19] != 'H':
            oops()

        if ord(flag[20]) == 117:
            yeayy()

        if ord(flag[21]) != ord(flag[2]) - 10:
            oops()

        if flag[22] != flag[0].lower():
            oops()

        if flag[22] == flag[23]:
            yeayy()
    return None

dis.dis(test)   # disassemble test() function
```

We can assume `yeayy()` means its ok and `oops()` means not ok. So we can reverse script like this according yeayy() and oops() above

```py
flag = list("_"*25)

flag[None:6] = 'TCP1P{'
flag[-1] = '}'
flag[6:10] = 'byte'
flag[10] = "_"
flag[15] = "_"
flag[18] = chr(95)
flag[11:15] = 'code'
flag[19] = flag[11]
flag[20] = chr(117)
flag[12] = chr(ord(flag[20]) - 6)
flag[16] = chr(105)
flag[17] = chr(115)
flag[19] = 'H'
flag[21] = chr(ord(flag[2]) - 10)
flag[22] = flag[0].lower()
flag[23] = flag[22]

# Make into string
print(''.join(flag))
```

>TCP1P{byte_code_is_HuFtt}