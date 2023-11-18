import socket
import time

# Set the IP address and port of the server
host = '192.168.2.27' # The ip address of the PC you want to send data to
port = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")

try:
    while True:
        # Send data to the server
        message = "Hello from Raspberry Pi!"
        client_socket.sendall(message.encode('utf-8'))
        time.sleep(1)  # Send data every 1 second

finally:
    # Close the connection
    client_socket.close()
