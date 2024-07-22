import serial
import time
from datetime import datetime
import os
import threading

# User defined variables
x_gridpoints = 251  # For data formatting change to number of x_gridpoints in probing_gcode_generator
PORT = 'COM4'

dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
z_coords_filename = f"Z Vals {dt_string}.csv"
path = os.path.dirname(os.path.abspath(__file__))
readings = 0
reading = 0

# Serial connection to DTI setup
ser = serial.Serial(PORT, 9600, timeout=5)
time.sleep(1)
ser.flushInput()

def get_reading():
    try:
        raw_reading = ser.read_until(b'\r',20)
        # print(raw_reading)
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
        if readings % x_gridpoints == 0:
             f.write("\n")
