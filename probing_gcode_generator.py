import os
import paramiko

xy_feedrate = 4000
z_feedrate = 300
dwell_period = 5
filename = "test.gcode"
path = os.path.dirname(os.path.abspath(__file__))
host = "192.168.200.51"
username = "pi"
password = "pi"
port = 22

local_path = os.path.join(path, filename)
x_coords = [0, 404, 900]
# xy_coords_list = []

with open(local_path, 'w') as f:
    f.write("G0\n")
    f.write("G90\n")
    f.write(f"Z30 F{z_feedrate}\n")

    for y in range(2400, 0, -300):
        for x in x_coords:
            f.write(f"X{x} Y{y} F{xy_feedrate}\n")
            f.write(f"Z-3 F{z_feedrate}\n")
            f.write(f"G4 P{dwell_period}\n")
            f.write(f"Z10 F{z_feedrate}\n")
            # xy_coords_list.append(f"{x}, {y}")

    f.write(f"Z30 F{z_feedrate}\n")
    print(f"File: '{filename}' saved to '{path}'")
    # for item in xy_coords_list:
    #     f.write(f"{str(item)},\n")

f.close()

print("Does the file exist?", os.path.exists(local_path))

ssh_client = paramiko.SSHClient()

ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=host, port=port, username=username, password=password)

print("connection established successfully")

ftp = ssh_client.open_sftp()

files = ftp.put(local_path, "/home/pi/easycut-smartbench/src/jobCache/" + filename)
print("File transferred successfully")

ftp.close()
ssh_client.close()