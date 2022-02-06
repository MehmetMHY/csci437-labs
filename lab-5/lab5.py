# Title: CSCI 437 Lab 5
# By: Bao (Jean) Duong & Mehmet Yilmaz

import numpy as np
import cv2

# mouse callback function
def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        window_name, image, point_list = param  # Unpack parameters
        cv2.rectangle(image, pt1=(x-15, y-15), pt2=(x+15, y+15), color=(0,0,255),thickness=3)
        cv2.imshow(window_name, image)
        point_list.append((x, y))

# utility function to create an image window.
def create_named_window(window_name, image):
    # WINDOW_NORMAL allows resize; use WINDOW_AUTOSIZE for no resize.
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    h = image.shape[0]  # image height
    w = image.shape[1]  # image width

    # Shrink the window if it is too big (exceeds some maximum size).
    WIN_MAX_SIZE = 1000
    if max(w, h) > WIN_MAX_SIZE:
        scale = WIN_MAX_SIZE / max(w, h)
    else:
        scale = 1
    cv2.resizeWindow(winname=window_name, width=int(w * scale), height=int(h * scale))

# swap index values x with y for a list
def swap(list, x, y):
    temp = list[x]
    list[x] = list[y]
    list[y] = temp
    return list

# main function
def main(image1, image2, out_name):
    # Reading the two images and storing it in variables main_image and temp_image
    main_image = cv2.imread(image1)
    temp_image = cv2.imread(image2)

    # Create list. The (x,y) points go in these lists.
    ptsA = []

    # Windows Name
    window_name = "Input Points (top_left, top right, buttom_left, & buttom_right)"

    # Display images.
    displayA = main_image.copy()
    create_named_window(window_name, displayA)
    cv2.imshow(window_name, displayA)

    # Assign the mouse callback function, which collects (x,y) points.
    cv2.setMouseCallback(window_name, on_mouse=get_xy, param=(window_name, displayA, ptsA))

    # Loop until user hits the ESC key.
    print("Click on points. Hit ESC to exit and continue.")
    while True:
        if cv2.waitKey(100) == 27:  # ESC is ASCII code 27
            break

    temp = ptsA.copy() # create copy of points from inputed clicks

    # draw black polygon, remove region, of where you want to replace in your input image
    temp = swap(temp, len(temp)-1, len(temp)-2)
    ptsA2 = np.array(temp)
    main_image = cv2.fillPoly(main_image, pts =[ptsA2], color=(0, 0, 0))

    # * map a new image onto a planar area of an exisiting image,
    #   using a homography projective transform. 

    height, width = main_image.shape[:2]
    h1, w1 = temp_image.shape[:2]

    pts1 = np.float32([[0, 0], [w1, 0], [0, h1], [w1, h1]])
    pts2 = np.float32(ptsA)
    h, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)

    height, width, channels = main_image.shape

    bgr_output0 = cv2.warpPerspective(temp_image, h, (width, height))

    mask2 = np.zeros(main_image.shape, dtype=np.uint8)

    roi_corners2 = np.int32(ptsA)

    channel_count2 = main_image.shape[2]
    ignore_mask_color2 = (255,) * channel_count2

    cv2.fillConvexPoly(mask2, roi_corners2, ignore_mask_color2)

    mask2 = cv2.bitwise_not(mask2)
    masked_image2 = cv2.bitwise_and(main_image, mask2)

    # Using Bitwise or to merge the two images
    final = cv2.bitwise_or(bgr_output0, masked_image2)

    # save final image
    cv2.imwrite(out_name, final)

if __name__ == "__main__":
    # input image names, make sure to spell it correctly
    print("CSCI 437 Lab 5")
    image1 = input("1st image (main):  ")
    image2 = input("2nd image (input): ")
    out_name = "output.png"

    main(image1, image2, out_name)
    
    print("\nCreated output file: " + out_name)

