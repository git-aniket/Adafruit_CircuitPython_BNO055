import socket

# Set the IP address and port to listen on
host = '0.0.0.0'  # Listen on all available interfaces
port = 12345

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections (max 1 connection in this example)
server_socket.listen(1)
print(f"Listening for connections on {host}:{port}")

# Accept a connection and get the client socket and address
client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

try:
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break  # No more data, break the loop

        # Print the received data
        print(f"Received data: {data.decode('utf-8')}")

finally:
    # Close the connection
    client_socket.close()
    server_socket.close()
