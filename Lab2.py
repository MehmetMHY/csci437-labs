import math
import numpy as np


def main():
    tc_w = np.array([[10, -25, 40]]).T
    ax = 1.22
    sx = math.sin(ax)
    cx = math.cos(ax)

    Rx = np.array(((1, 0, 0), (0, cx, -sx), (0, sx, cx)))
