import serial
import time

filename = "Z Vals.csv"
path = "C:\\Users\\ramiz\\Desktop\\"
readings = 0

PORT = 'COM14'
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


with open (f"{path}{filename}", 'w') as f:
    while True:
        input("")
        value = get_reading()
        # value = "test"
        readings += 1
        print(value)
        print(readings)
        f.write(f"{value},")
        if readings % 3 == 0:
             f.write("\n")
            