import numpy as np
import math

ax, ay, az = 1.1, -0.5, 0.1 # radians

sx, sy, sz = np.sin(ax), np.sin(ay), np.sin(az)
cx, cy, cz = np.cos(ax), np.cos(ay), np.cos(az)

Rx = np.array(((1, 0, 0), (0, cx, -sx), (0, sx, cx)))
Ry = np.array(((cy, 0, sy), (0, 1, 0), (-sy, 0, cy)))
Rz = np.array(((cz, -sz, 0), (sz, cz, 0), (0, 0, 1)))

print("-----------------------------------------------------------------------------------")
print("\n[ Q1-a: ]")
# Apply X rotation first, then Y, then Z
R = Rz @ Ry @ Rx    # Use @ for matrix mult
print("XYZ:")
print(R)

print()

print("ZYX:")

print("\n[ Q1-b ]")
print(np.matrix.transpose(R))
print("           ⬆ Equal ⬇")
print(np.linalg.inv(R))

print("\n[ Q1-c ]")
# Apply Z rotation first, then Y, then X
R2 = Rx @ Ry @ Rz
print(R2)
print("-----------------------------------------------------------------------------------")
print("\n[ Q2-a: ]")
tc_w = np.array([[10, -25, 40]]).T

R_c_w = R  # The only rotation is about x

H_c_w = np.block([[R_c_w, tc_w], [0, 0, 0, 1]])  # Get as 4x4 matrix
print("H_c_w:"), print(H_c_w)

print("\n[ Q2-b: ]")

# Get transformation from world to camera.
H_w_c = np.linalg.inv(H_c_w)
print("H_w_c:"), print(H_w_c)

print("\n[ Q2-c: ]")
f = 400
cx = 256
cy = 170
K = np.array(((f, 0, cx), (0, f, cy), (0, 0, 1)))
print("K = \n", str(K))

Mext = H_w_c[0:3, :]

print("Mext = \n", str(Mext))

P_w = np.array(((6.8158, 7.8493, 9.9579, 8.8219, 9.5890, 10.9092, 13.2690),
                (-35.1954, -36.1723, -25.2799, -38.3767, -28.84, -48.8146, -58.0988),
                (43.0640, 43.7815, 40.1151, 46.6153, 42.2858, 56.1475, 59.1422)))

final_points = []
for i in range(len(P_w[0])):
    P_temp = P_w[ : , i]
    P_temp = np.append(P_temp, 1)
    temp = K @ Mext @ P_temp
    temp = temp / temp[2]
    final_points.append(temp)

# EXAMPLE: 
# print(P_w[ : , 0])
# P_temp = (((6.8, -35.1, 42.0, 1)))
# p = K @ Mext @ P_temp
# p = p / p[2]
# print("p:"), print(p)

def print_list(theList, indent):
    if(indent): print()
    for i in range(len(theList)):
        print(theList[i])
    if(indent): print()

print_list(final_points, True)

image = np.zeros((cx,cy))
for i in range(len(final_points)):
    x = int(round(final_points[i][0]))
    y = int(round(final_points[i][1]))
    image[x][y] = 1