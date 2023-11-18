# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import threading
import time
import board
import socket
import adafruit_bno055
from typing import Final

FREQUENCY:Final = 100 #Hz

# Set the IP address and port of the server
host = '192.168.2.27'
port = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# setup adafruit IMU sensor
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")

try:
    while True:
        # Send data to the server
        data_string=str(format(sensor.acceleration)) 
        #+ str(format(sensor.magnetic)) + str(format(sensor.gyro)) + str(format(sensor.quaternion)) + str(format(sensor.euler)) + str( format(sensor.gravity))
        #message = "Hello from Raspberry Pi!"
        client_socket.sendall(data_string.encode('utf-8'))
        time.sleep(1/FREQUENCY)  # Send data every changed frequency 

finally:
    # Close the connection
    client_socket.close()



## Attempt at making this program multithreaded
# def print_numbers():
#     for i in range(10):
#         time.sleep(1)
#         print(i)

# def print_letters():
#     for letter in 'abcdefghij':
#         time.sleep(1)
#         print(letter)
    
# t1=threading.Thread(target=print_numbers)
# t2=threading.Thread(target=print_letters)

# t1.start()
# t2.start()

# t1.join()
# t2.join()

#print("Execution Finished")