import os
import paramiko
from datetime import datetime

dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
xy_feedrate = 4000
z_feedrate = 300
dwell_period = 5
gcode_filename = f"probing {dt_string}.gcode"
xy_coords_filename = f"xy coordinates {dt_string}.csv"
path = os.path.dirname(os.path.abspath(__file__))
host = "192.168.200.51"
username = "pi"
password = "pi"
port = 22
x_coords = [0, 404, 900]
xy_coords_list = []

local_path_gcode = os.path.join(path, "Output", gcode_filename)
with open(local_path_gcode, 'w') as f:
    f.write("G0\n")
    f.write("G90\n")
    f.write(f"Z30 F{z_feedrate}\n")

    for y in range(2400, 0, -300):
        for x in x_coords:
            f.write(f"X{x} Y{y} F{xy_feedrate}\n")
            f.write(f"Z-3 F{z_feedrate}\n")
            f.write(f"G4 P{dwell_period}\n")
            f.write(f"Z10 F{z_feedrate}\n")
            xy_coords_list.append(f"{x}, {y}")

    f.write(f"Z30 F{z_feedrate}\n")
    print(f"File: '{gcode_filename}' saved to '{local_path_gcode}'")

f.close()

local_path_xy_coords = os.path.join(path, "Output", xy_coords_filename)
with open (local_path_xy_coords, 'w') as c:
    for item in xy_coords_list:
        c.write(f"{str(item)}\n")
    print(f"File: '{xy_coords_filename}' saved to '{local_path_xy_coords}'")
c.close()

ssh_client = paramiko.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host, port=port, username=username, password=password)

print("connection established successfully")

ftp = ssh_client.open_sftp()

files = ftp.put(local_path_gcode, "/home/pi/easycut-smartbench/src/jobCache/" + gcode_filename)
print("File transferred successfully")

ftp.close()
ssh_client.close()