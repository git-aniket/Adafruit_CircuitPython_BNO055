"""
Script to create a socket and send data from IMU to PC over 
socket connection
"""
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import threading
import time
import board
import socket
import adafruit_bno055
from typing import Final
import sys

FREQUENCY:Final = 1000 #Hz

# Set the IP address and port of the client
host = '192.168.2.3'
port = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# setup adafruit IMU sensor
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")

def send_data():
    try:
        while True:
            # Send data to the server
            data_string=str(format(sensor.acceleration)) + str(format(sensor.magnetic)) + str(format(sensor.gyro)) + str(format(sensor.quaternion)) + str(format(sensor.euler)) + str( format(sensor.gravity))
            client_socket.sendall(data_string.encode('utf-8'))
            time.sleep(1/FREQUENCY)  # Send data according to Frequency

    finally:
        # Close the connection
        client_socket.close()

send_data_thread=threading.Thread(target=send_data)
send_data_thread.start()
send_data_thread.join()

print("Exiting")
sys.exit(0)