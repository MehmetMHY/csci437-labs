import math
import numpy as np


def main():
    tc_w = np.array([[10, -25, 40]]).T
    ax = 1.22
    sx = math.sin(ax)
    cx = math.cos(ax)

    Rx = np.array(((1, 0, 0), (0, cx, -sx), (0, sx, cx)))
    R_c_w = Rx  # The only rotation is about x

    H_c_w = np.block([[R_c_w, tc_w], [0, 0, 0, 1]])  # Get as 4x4 matrix
    print("H_c_w:"), print(H_c_w)

    # Get transformation from world to camera.
    H_w_c = np.linalg.inv(H_c_w)
    print("H_w_c:"), print(H_w_c)

if __name__ == "__main__":
    main()