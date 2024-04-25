import serial
import time
from datetime import datetime
import os
import threading

dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
z_coords_filename = f"Z Vals {dt_string}.csv"
path = os.path.dirname(os.path.abspath(__file__))
readings = 0
reading = 0

PORT = 'COM14'
ser = serial.Serial(PORT, 9600, timeout=5)
time.sleep(1)
ser.flushInput()

def get_reading():
    try:
        raw_reading = ser.read_until(b'\r',20)
        reading = float(raw_reading[3:])
        reading /= 1000.0
        return reading
    except Exception as e:
            print(e)

def const_read():
    global reading
    while True:
        reading = get_reading()

reading_thread = threading.Thread(target=const_read)
reading_thread.daemon = True  # Daemonize the thread to exit when the main program exits
reading_thread.start()

local_path_z_coords = os.path.join(path, "Output", z_coords_filename)
with open (local_path_z_coords, 'w') as f:
    while True:
        input("")
        value = reading
        readings += 1
        print(value)
        print(readings)
        f.write(f"{value},")
        if readings % 3 == 0:
             f.write("\n")
