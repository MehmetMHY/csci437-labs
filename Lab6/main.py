# Title: Lab 6 Code
# Date:  10-9-2020

import sys
import time
import cv2
import numpy as np
import order_targets as ot


# find the distance between two points
def distance(px, py, x, y):
    one = np.array((px, py))
    two = np.array((x, y))
    return np.linalg.norm(one - two)



# determine the distance between two centroids
def centroids_distance(centroid, centroid2):
    temp = centroid - centroid2
    return abs(abs(temp[0]) - abs(temp[1]))


# main function
def main(video_file):
    #####[User_Parameters]#####
    C_val = 40  # constant to subtract from mean for the cv2.adaptiveThreshold()
    ksize = 2  # ksizexksize square box filter for opening and/or closing
    d_thresh = 10  # distance threshold for two points
    c_thresh = 0.6  # distance threshold for two centroids
    b_ideal_area = 250  # ideal area for a CCC black blob
    w_ideal_area = 36  # ideal area for a CCC white blobs
    #####[User_Parameters]#####

    img = cv2.imread(video_file)
    image = img  # determine what image to display though imshow()

    # grayscale color frame/image
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # apply adaptive thresholding to frame/image
    binary_img = cv2.adaptiveThreshold(
        src=gray_img,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=51,
        C=C_val)

    # clean up frame/image by applying opening and closing though a kernel (ksizexksize matrix box filter)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)
    binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

    # find connected components for all white blobs
    w_num_labels, w_labels_img, w_stats, w_centroids = cv2.connectedComponentsWithStats(binary_img)

    # find connected components for all black blobs
    b_num_labels, b_labels_img, b_stats, b_centroids = cv2.connectedComponentsWithStats(cv2.bitwise_not(binary_img))

    all_points = []

    # loop though every white and black blobs
    i = 0
    for stat, centroid in zip(w_stats, w_centroids):
        j = 0
        for stat2, centroid2 in zip(b_stats, b_centroids):
            # get pixal coorindates for white and black plobs, for protential display boxing
            x_w = stat[cv2.CC_STAT_LEFT]    ;   x_b = stat2[cv2.CC_STAT_LEFT]
            y_w = stat[cv2.CC_STAT_TOP]     ;   y_b = stat2[cv2.CC_STAT_TOP]
            w_w = stat[cv2.CC_STAT_WIDTH]   ;   w_b = stat2[cv2.CC_STAT_WIDTH]
            h_w = stat[cv2.CC_STAT_HEIGHT]  ;   h_b = stat2[cv2.CC_STAT_HEIGHT]

            # get area(s) for the selected white and black blobs
            area_w = w_stats[i, cv2.CC_STAT_AREA]
            area_b = b_stats[j, cv2.CC_STAT_AREA]

            # get distance from the centroid of the selected white and balck blobs
            c_dist = centroids_distance(centroid, centroid2)

            # filter what gets displayed:
            #   - check if the distance between the two centroids is less then or equal to the set threshold
            #   - check if the pixal point distance between white and balck is below the set threshold
            #   - check if the white and black blob's areas are at or below a set threshold
            if (c_dist <= c_thresh and distance(x_w, y_w, x_b, y_b) < d_thresh and (
                    area_b <= b_ideal_area and area_w <= w_ideal_area)):
                all_points.append(np.array((x_w, y_w)))

            j = j + 1
        i = i + 1

    all_points = list(ot.order_targets(all_points))

    c = 0
    for i in all_points:
        marking = cv2.putText(image, text=str(c), org=(i[0], i[1]), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, thickness=2, color=(0, 0, 255))
        c = c + 1

    f = 531
    cx = 320/2
    cy = 240/2

    K = np.array(((f, 0, cx), (0, f, cy), (0, 0, 1)), dtype="double")

    pts = []
    for i in range(len(all_points)):
        pts.append(np.array(all_points[i], dtype="double"))
    pts = np.row_stack((pts))
    pts = np.array(pts, dtype="double")

    xh = 7.4/2
    yh = 4.55/2

    P_M = np.array([[-xh, -yh, 1], 
                    [0, -yh,   1],
                    [xh, -yh,  1],
                    [-xh, yh,  1],
                    [xh, yh,   1]])
    P_M = np.array(P_M, dtype="double")

    PoseFound, rvec, tvec = cv2.solvePnP(objectPoints=P_M, imagePoints=pts, cameraMatrix=K, distCoeffs=None)
    
    W = np.amax(P_M,axis=0) - np.amin(P_M,axis=0)
    L = np.linalg.norm(W)
    d = L/5

    pAxes = np.float32([[0, 0, 0], [d, 0, 0], [0, d, 0], [0, 0, d]])

    pImg, J = cv2.projectPoints(objectPoints=pAxes, rvec=rvec, tvec=tvec, cameraMatrix=K, distCoeffs=None)

    pImg = pImg.reshape(-1, 2)

    cv2.line(image, tuple(np.int32(pImg[0])),tuple(np.int32(pImg[1])), (0, 0, 255), 3)
    cv2.line(image, tuple(np.int32(pImg[0])),tuple(np.int32(pImg[2])), (0, 255, 0), 3)
    cv2.line(image, tuple(np.int32(pImg[0])),tuple(np.int32(pImg[3])), (255, 0, 0), 3)

    pose = []
    rv = []
    tv = []
    for i in rvec:
        rv.append(float(str("%.2f" % float(i))))
    tv = []
    for i in tvec:
        tv.append(int(i))
    pose.append(rv) ; pose.append(tv)

    marking = cv2.putText(image, text=str("rvec: " + str(pose[0])), org=(50, 450), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.1, color=(255, 255, 255), thickness=2)
    marking = cv2.putText(image, text=str("tvec: " + str(pose[1])), org=(50, 400), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.1, color=(255, 255, 255), thickness=2)

    cv2.imshow("Lab 6", image)
    cv2.waitKey(30)


if __name__ == "__main__":
    main("CCCtarget.jpg")
    print("\n[ Enter SPACE To Exit ]\n")
    cv2.waitKey(0)


