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

ax = 1.22 # radians
sx = math.sin(ax)
cx = math.cos(ax)

Rx = np.array(((1, 0, 0), (0, cx, -sx), (0, sx, cx)))
R_c_w = Rx  # The only rotation is about x

H_c_w = np.block([[R_c_w, tc_w], [0, 0, 0, 1]])  # Get as 4x4 matrix
print("H_c_w:"), print(H_c_w)

print("\n[ Q2-b: ]")

# Get transformation from world to camera.
H_w_c = np.linalg.inv(H_c_w)
print("H_w_c:"), print(H_w_c)





