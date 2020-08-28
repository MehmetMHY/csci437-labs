import cv2
import sys
import numpy as np

def main():
    # Read images from a video file in the current folder.
    video_capture = cv2.VideoCapture("earth.wmv")     # Open video capture object
    got_image, bgr_image = video_capture.read()       # Make sure we can read video
    if not got_image:
        print("Cannot read video source")
        sys.exit()

    # Read and show images until end of video is reached.
    while True:
        got_image, bgr_image = video_capture.read()
        if not got_image:
            break       # End of video; exit the while loop
        # Draw a marker (a cross) in the middle of the image.
        cv2.drawMarker(bgr_image, position=(200,200), color=(0, 0, 255), markerType=cv2.MARKER_CROSS)

        # Draw some text at the bottom of the image.
        cv2.putText(bgr_image, text="Hello", org=(150, 350), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.5, color=(0, 255, 0))

        cv2.imshow("my image", bgr_image)

        # Wait for xx msec (0 means wait till a keypress).
        cv2.waitKey(30)

if __name__ == "__main__":
    main()
