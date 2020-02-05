#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) # Set /dev/ttyACMO to location of Arduino
    ser.flush()

    ser.write("0\n".encode('utf-8')) # Have to send in bytes b/c Arduino can only read bytes
    line = ser.readline().decode('utf-8').rstrip()
    print(line)

    ser.write("0\n".encode('utf-8')) # Have to send in bytes b/c Arduino can only read bytes
    line = ser.readline().decode('utf-8').rstrip()
    print(line)

    angle = 90
    while True:
        message = str(angle) + "\n"
        print(message)
        ser.write(message.encode('utf-8')) # Have to send in bytes b/c Arduino can only read bytes
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
        angle+=10
