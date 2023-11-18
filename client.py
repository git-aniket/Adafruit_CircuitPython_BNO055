# Import socket module
import socket 
# Create a socket object 
s = socket.socket()
# Define the port on which you want to connect 
port = 12345

#connect to the server on nescessary ip on same network
s.connect(('192.168.2.31',port))

#receive data from the server and decoding to get the string
print(s.recv(1024).decode())
#close connection
s.close()
