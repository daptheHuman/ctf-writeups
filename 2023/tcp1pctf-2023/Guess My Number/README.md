# Guess My Number

## Information
**Category:** |
--- | 
Misc|

**Description:** 
~~~
My friend said if i can guess the right number, he will give me something. Can you help me?

nc ctf.tcp1p.com 7331
~~~
## Solution
We can compile the binary file with IDA, go to vuln function

```c
int vuln()
{
  int v1; // [rsp+Ch] [rbp-4h]

  key = 0;
  srand(1337u);
  v1 = rand();

  printf("Your Guess : ");
  fflush(_bss_start);
  __isoc99_scanf("%d", &key);

  if ( ((v1 + 1337331) ^ key) == -889275714 )
  {
    puts("Correct! This is your flag :");
    system("cat flag.txt");
    exit(0);
  }

  return puts("Wrong, Try again harder!");
}
```

Inspecting in this function we can see the vuln is in the `srand()`, because we can see the value that passed to the srand and it's not changing

We can try to print the output of `rand()` if we using `srand(1337)`

```c
int main() {
    int i = 0;
    for (i = 0; i < 10; i++) {
        srand(1337);
        printf("%d\n", rand());
    }
    return 0;
}
```
So, rand will output the same value

`(v1 + 1337331) ^ key) == -889275714 )`

By having the `v1` we can get the what should we input as a `key` in order to get `-889275714`


`( 292616681 + 1337331 ) ^  -889275714 = -612639902`



>TCP1P{r4nd0m_1s_n0t_th4t_r4nd0m_r19ht?_946f38f6ee18476e7a0bff1c1ed4b23b}
