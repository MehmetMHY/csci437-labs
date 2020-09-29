import sys
import time
import cv2
import numpy as np

# Mouse callback function. Appends the x,y location of mouse click to a list.
clicks = []
def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        clicks.append([x, y])

def recedeSqaure(video_file):
    # Read images from a video file in the current folder.
    video_capture = cv2.VideoCapture(video_file)  # Open video capture object
    got_image, bgr_image = video_capture.read()  # Make sure we can read video
    if not got_image:
        print("Cannot read video source")
        sys.exit()
    
    template = cv2.imread('1.png',0)
    w, h = template.shape[::-1]

    # Read and show images until end of video is reached.
    while True:
        got_image, bgr_image = video_capture.read()
        if not got_image:
            break  # End of video; exit the while loop

        if(len(clicks) > 3):
            for i in range(len(clicks)):
                x = clicks[i][0]
                y = clicks[i][1]
                pos = cv2.drawMarker(bgr_image, position=(int(x), int(y)), color=(0, 0, 255), markerType=cv2.MARKER_SQUARE)

        # cv2.namedWindow("Lab 1: OpenCV-Python Basics", cv2.WINDOW_NORMAL)
        cv2.imshow("Lab 3", bgr_image)

        cv2.setMouseCallback('Lab 3', get_xy)

        if(len(clicks) != 0):
            cv2.waitKey(30)
        else:
            print("Click on the image, then hit a key and it will play!")
            cv2.waitKey(0)


if __name__ == "__main__":
    recedeSqaure("building.avi")
    print("Enter CTRL-C To Exit")
    time.sleep(100)