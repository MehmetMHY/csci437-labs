# Title: CSCI437 Homework 2 problem 4
# Date:  9-28-2020
# By:    Mehmet Yilmaz

# Sources:
#   1) "4-1 Binary Images" Lecture slides/notes

import sys
import time
import cv2
import numpy as np

# find the distance between two points
def distance(px, py, x, y):
    one = np.array((px, py))
    two = np.array((x, y))
    return np.linalg.norm(one-two)

# determine the distance between two centroids
def centroids_distance(centroid, centroid2):
    temp = centroid-centroid2
    return abs(abs(temp[0])-abs(temp[1]))

# main function
def main(video_file):
    #####[User_Parameters]#####
    C_val = 15          # constant to subtract from mean for the cv2.adaptiveThreshold()
    ksize = 2           # ksizexksize square box filter for opening and/or closing
    d_thresh = 10       # distance threshold for two points
    c_thresh = 0.6      # distance threshold for two centroids
    b_ideal_area = 250  # ideal area for a CCC black blob
    w_ideal_area = 36   # ideal area for a CCC white blobs
    #####[User_Parameters]#####

    # Read images from a video file in the current folder.
    video = cv2.VideoCapture(video_file)
    got_image, img = video.read()

    # make sure the video file exists
    if not got_image:
        print("Cannot read video source")
        sys.exit()

    frame = 0 # count number of frames
    while True:
        got_image, img = video.read()
        if not got_image:
            break

        image = img # determine what image to display though imshow()

        # wait for user to hit SPACE before the video starts playing
        if(frame == 0):
            print("[ Enter SPACE To Start ]")
            cv2.imshow("HW2_P4", img)
            cv2.waitKey(0)
            print()

        frame = frame + 1 # add to frame counter

        # grayscale color frame/image
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # apply adaptive thresholding to frame/image
        binary_img = cv2.adaptiveThreshold(
            src=gray_img,
            maxValue=255,  # output value where condition met
            adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
            thresholdType=cv2.THRESH_BINARY,  # threshold_type
            blockSize=51,  # neighborhood size (a large odd number)
            C=C_val)  # a constant to subtract from mean
        
        # clean up frame/image by applying opening and closing though a kernel (ksizexksize matrix box filter)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)
        binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

        # find connected components for all white blobs
        w_num_labels, w_labels_img, w_stats, w_centroids = cv2.connectedComponentsWithStats(binary_img)

        # find connected components for all black blobs
        b_num_labels, b_labels_img, b_stats, b_centroids = cv2.connectedComponentsWithStats(cv2.bitwise_not(binary_img))

        ### Debugging tools:        
        #bgr_image_display = cv2.cvtColor(binary_img, cv2.COLOR_GRAY2BGR)

        # loop though every white and black blobs
        i = 0
        for stat, centroid in zip(w_stats, w_centroids):
            j = 0
            for stat2, centroid2 in zip(b_stats, b_centroids):
                # get pixal coorindates for white and black plobs, for protential display boxing
                x_w = stat[cv2.CC_STAT_LEFT]
                y_w = stat[cv2.CC_STAT_TOP]
                w_w = stat[cv2.CC_STAT_WIDTH]
                h_w = stat[cv2.CC_STAT_HEIGHT]

                x_b = stat2[cv2.CC_STAT_LEFT]
                y_b = stat2[cv2.CC_STAT_TOP]
                w_b = stat2[cv2.CC_STAT_WIDTH]
                h_b = stat2[cv2.CC_STAT_HEIGHT]

                # get area(s) for the selected white and black blobs
                area_w = w_stats[i, cv2.CC_STAT_AREA]
                area_b = b_stats[j, cv2.CC_STAT_AREA]

                # get distance from the centroid of the selected white and balck blobs
                c_dist = centroids_distance(centroid, centroid2)

                # filter what gets displayed:
                #   - check if the distance between the two centroids is less then or equal to the set threshold
                #   - check if the pixal point distance between white and balck is below the set threshold
                #   - check if the white and black blob's areas are at or below a set threshold
                if(c_dist <= c_thresh and distance(x_w, y_w, x_b, y_b) < d_thresh and (area_b <= b_ideal_area and area_w <= w_ideal_area)):
                    # draw rectangle on frame/image, for slected white blob (smaller area)
                    marking = cv2.rectangle(img=image, pt1=(x_w, y_w), pt2=(x_w + w_w, y_w + h_w),color=(0, 0, 255), thickness=1)
                    # draw rectangle on frame/image, for slected black blob (larger area)
                    marking = cv2.rectangle(img=image, pt1=(x_b, y_b), pt2=(x_b + w_b, y_b + h_b),color=(0, 0, 255), thickness=1)
                
                j = j + 1
            i = i + 1
        
        # add frame counter to video well playing
        cv2.putText(image, text=str(frame), org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 255, 0), thickness=2)
        
        # display frame/image
        cv2.imshow("HW2_P4", image)
        cv2.waitKey(30)
        
if __name__ == "__main__":
    main("fiveCCC.avi")
    print("[ Enter SPACE To Exit ]")
    cv2.waitKey(0)