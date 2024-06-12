We can see on the wireshark and `Follow TCP Stream` that the flag is retrieved by sending the string (java) to the server. We can use the same string to test it

But if we use the same string, we will get the fake flag, then i realize that i need to change the `fakechall` into `flagserver`, But it need to modify the `\x09` into `\x0a` because the server will check the length of the string

bcactf{thankS_5OCK3ts_and_tHreADInG_clA5s_2f6fb44c998fd8}