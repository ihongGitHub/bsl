#!/usr/bin/env python3

import serial
import time

print('Now Start 2018.02.10')
ser = serial.Serial('/dev/ttyUSB0', 9600)

ser.isOpen()

hks = 0
while hks<120:
    hks += 1
    print('count:', hks)
    ser.write(bytearray([48,49,50,51,52]))
    time.sleep(1)

ser.close()
