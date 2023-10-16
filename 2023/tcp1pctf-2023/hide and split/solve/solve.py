import xattr

attrs = []
def get_extended_attributes(file_path, attr):
    try:
        value = xattr.getxattr(file_path, f"user.flag{attr}")
        print(f"flag{attr}: {value}")
        attrs.append(value.decode("utf-8"))

    except Exception as e:
        # Handle any other exceptions that may occur
        print(e)

for i in range(100):
    id = "{:02d}".format(i)
    filename = f"flag{id}.txt"
    get_extended_attributes(filename, i)
    # You can perform operations with the 'filename' variable here.

print("".join(attrs))