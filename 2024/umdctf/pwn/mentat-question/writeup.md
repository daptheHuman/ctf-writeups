UMDCTF{3_6u1ld_n4v16470r5_4_7074l_0f_1.46_m1ll10n_62_50l4r15_r0und_7r1p}
---
Since the PIE enabled we need to leak the address first by using the arbitary read

```c
if (num2 < 1) {
        puts("Oh, I was not aware we were using negative numbers!");
        puts("Would you like to try again?");
        gets(buf);
        if (strncmp(buf, "Yes", 3) == 0) {
            fputs("Was that a ", stdout);
            printf(buf);
```

But for some reason i couldnt get into the condition when the `num2` is negative it must be zero,
So i notice on the next prompt the input is set to be `0` then i just send empty line 

After getting into the condition, i need to leak the PIE address, after that ret2win