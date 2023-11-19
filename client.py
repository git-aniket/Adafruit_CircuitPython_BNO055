"""
This script creates a TCP/IP server that listens for incoming connections
and prints the data received from the client.
"""
import socket
import time
import threading
import sys

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

def receive_data_thread():
    try:
            while True:
                # Receive data from the client
                data = client_socket.recv(4096)
                if not data:
                    break  # No more data, break the loop

                # Print the received data
                print(f"Received data: {data.decode('utf-8')}")

    finally:
            # Close the connection
            client_socket.close()
            server_socket.close()


# Create a thread with the function read_data_thread
my_thread = threading.Thread(target=receive_data_thread)
my_thread.start()

my_thread.join()
sys.exit(0)
