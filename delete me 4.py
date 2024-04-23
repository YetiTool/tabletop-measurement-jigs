import serial
import time
import numpy as np

PORT = 'COM15'
ser = serial.Serial(PORT, 9600, timeout=5)
time.sleep(1)
ser.flushInput()


def get_reading():
    try:
        #TODO: add kivy delay
        raw_reading = ser.read_until(b'\r',20)
        reading = float(raw_reading[3:])
        reading /= 1000.0
        print(reading)
        return reading
    except Exception as e:
            print(e)

while True:
     get_reading()