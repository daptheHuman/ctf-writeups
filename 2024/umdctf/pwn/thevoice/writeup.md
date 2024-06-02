UMDCTF{pwn_g3ss3r1t_sk1ll5_d0nt_tak3_a5_many_y3ar5_t0_l3arn_pau1}
---

```c
gets(command);
g[atoi(command)] = 10191;
```

Using `g[atoi(command)]` for overwriting on canaries variable by passing the offset index  
And spray the buffer with the overwritted canary `10191` and ret2win