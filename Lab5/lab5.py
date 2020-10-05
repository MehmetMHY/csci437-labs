import cv2
import numpy as np


# Mouse callback function
def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        window_name, image, point_list = param  # Unpack parameters
        cv2.rectangle(image, pt1=(x-15, y-15), pt2=(x+15, y+15), color=(0,0,255),thickness=3)
        cv2.imshow(window_name, image)
        point_list.append((x, y))

# Utility function to create an image window.
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

def main():
    # Reading the two images and storing it in variables img and meme
    baseball = cv2.imread('baseball.jpg')
    meme = cv2.imread('meme.jpg')

    # Create list.  The (x,y) points go in these lists.
    ptsA = []

    # Display images.
    displayA = baseball.copy()
    create_named_window("Image A", displayA)
    cv2.imshow("Image A", displayA)

    # Assign the mouse callback function, which collects (x,y) points.
    cv2.setMouseCallback("Image A", on_mouse=get_xy, param=("Image A", displayA, ptsA))

    # Loop until user hits the ESC key.
    print("Click on points.  Hit ESC to exit.")
    while True:
        if cv2.waitKey(100) == 27:  # ESC is ASCII code 27
            break
            print("PtsA:", ptsA)        # Print points to the console

    height, width = baseball.shape[:2]
    h1, w1 = meme.shape[:2]

    pts1 = np.float32([[0, 0], [w1, 0], [0, h1], [w1, h1]])
    pts2 = np.float32(ptsA)

    h, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)

    height, width, channels = baseball.shape

    bgr_output0 = cv2.warpPerspective(meme, h, (width, height))

    mask2 = np.zeros(baseball.shape, dtype=np.uint8)

    roi_corners2 = np.int32(ptsA)

    channel_count2 = baseball.shape[2]
    ignore_mask_color2 = (255,) * channel_count2

    cv2.fillConvexPoly(mask2, roi_corners2, ignore_mask_color2)

    mask2 = cv2.bitwise_not(mask2)
    masked_image2 = cv2.bitwise_and(baseball, mask2)

    # Using Bitwise or to merge the two images
    final = cv2.bitwise_or(bgr_output0, masked_image2)
    cv2.imwrite('final.png', final)

if __name__ == "__main__":
    main()

