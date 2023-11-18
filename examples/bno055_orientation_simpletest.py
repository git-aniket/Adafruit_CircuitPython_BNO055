# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import threading
import time
import board
import socket
import adafruit_bno055
from typing import Final
FREQUENCY:Final=100 #Hz

TCP_IP = '192.168.2.27'
TCP_PORT = 5005
BUFFER_SIZE = 1024

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',5023))
s.connect((TCP_IP, TCP_PORT))

while True:
    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    print()
    s.send(format(sensor.acceleration))
    time.sleep(2)








#while True:
    ##print("Temperature: {} degrees C".format(sensor.temperature))
    #"""
    #print(
        #"Temperature: {} degrees C".format(temperature())
    #)  # Uncomment if using a Raspberry Pi
    #"""
    #print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    #print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    #print("Gyroscope (rad/sec): {}".format(sensor.gyro))
    ##print("Quaternion: {}".format(sensor.quaternion))
    ##print("Euler angle: {}".format(sensor.euler))
    ##print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    ##print("Gravity (m/s^2): {}".format(sensor.gravity))
    #print()
    #time.sleep(1/FREQUENCY)

    #s.send(format(sensor.acceleration))




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


