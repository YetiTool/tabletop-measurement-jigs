import os
import paramiko
from datetime import datetime
import numpy as np

# file name and path params
dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
gcode_filename = f"probing {dt_string}.gcode"
xy_coords_filename = f"xy coordinates {dt_string}.csv"
path = os.path.dirname(os.path.abspath(__file__))

# sftp params
host = "192.168.200.51"
username = "pi"
password = "pi"
port = 22

# gcode params
# x_coords = [0, 404, 900]
x_min, x_max, x_gridpoints = 0, 1140, 5  # change these values for x reach and gridpoints
y_min, y_max, y_gridpoints = 0, 2020, 10  # change these values for y reach and gridpoints
xy_feedrate = 6000
z_feedrate = 300
dwell_period = 3

# coordinate logging
xy_coords_list = []

# gcode generator
x_coords = np.linspace(x_min, x_max, num=x_gridpoints)
y_coords = np.linspace(y_max, y_min, num=y_gridpoints)
local_path_gcode = os.path.join(path, "Output", gcode_filename)
with open(local_path_gcode, 'w') as f:
    f.write("G0\n")
    f.write("G90\n")
    f.write(f"Z30 F{z_feedrate}\n")

    for y in y_coords:
        for x in x_coords:
            f.write(f"X{x:.3f} Y{y:.3f} F{xy_feedrate}\n")
            f.write(f"Z-3 F{z_feedrate}\n")
            f.write(f"G4 P{dwell_period}\n")
            f.write(f"Z10 F{z_feedrate}\n")
            xy_coords_list.append(f"{x:.3f}, {y:.3f},@")

    f.write(f"Z30 F{z_feedrate}\n")
    print(f"File: '{gcode_filename}' saved to '{local_path_gcode}'")

f.close()

# coordinate log generator
local_path_xy_coords = os.path.join(path, "Output", xy_coords_filename)
with open (local_path_xy_coords, 'w') as c:
    coords = 0
    for item in xy_coords_list:
        c.write(f"{str(item)}")
        coords += 1
        if coords % x_gridpoints == 0:
            c.write("\n")
c.close()
print(f"File: '{xy_coords_filename}' saved to '{local_path_xy_coords}'")

# sftp sending gcode file to console
ssh_client = paramiko.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host, port=port, username=username, password=password)

print("connection established successfully")

ftp = ssh_client.open_sftp()

# nice
files = ftp.put(local_path_gcode, f"/home/pi/easycut-smartbench/src/jobCache/ {gcode_filename}")
print("File transferred successfully")

ftp.close()
ssh_client.close()