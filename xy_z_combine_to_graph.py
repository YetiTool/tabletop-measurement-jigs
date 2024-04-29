import os
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Inputs
path = os.path.dirname(os.path.abspath(__file__))
xy_filename = "xy coordinates 25-04-2024 17-51-37.csv"
z_filename = "Z Vals 29-04-2024 19-01-56.csv"
xy_path = os.path.join(path, "Output", xy_filename)
z_path = os.path.join(path, "Output", z_filename)

# Outputs
xyz_filename = "xyz_coords.csv"#
png_filename = "tabletop.png"
xyz_path = os.path.join(path, "Output", xyz_filename)
png_path = os.path.join(path, "Output", png_filename)
xy_list = []
z_list = []
x_list = []
y_list = []
xyz_list = []

with open (xy_path, 'r') as xy:
    xy_string = (xy.read().replace("\n", "").replace("@", ""))
xy.close()
xy_list = xy_string.split(",")

with open (z_path, 'r') as z:
    z_string = (z.read().replace("\n", ""))
z.close()
z_list = z_string.split(",")

for index in range(len(xy_list)):
    if (index % 2 == 0): 
        x_list.append(xy_list[index])
    else:
         y_list.append(xy_list[index])

del x_list[-1]
del z_list[-1]

x_list = [float(x_val) for x_val in x_list]
y_list = [float(y_val) for y_val in y_list]
z_list = [float(z_val) for z_val in z_list]
z_average = sum(z_list)/len(z_list)
z_list = [z_val - z_average for z_val in z_list]  # Normalise Z values

for i in range(len(x_list)):
    x_cur = (x_list[i])
    y_cur = (y_list[i])
    z_cur = (z_list[i])
    sub_list = [x_cur, y_cur, z_cur,]
    xyz_list.append(sub_list)
print(xyz_list)

DATA = np.array(xyz_list)

Xs = DATA[:,0]
Ys = DATA[:,1]
Zs = DATA[:,2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_trisurf(Xs, Ys, Zs, cmap=cm.cividis_r , linewidth=0)
fig.colorbar(surf)


ax.set_zlim(-1, 1)  # Set Z axis limits

ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))

fig.tight_layout()

plt.show() # or:
fig.savefig(png_path)