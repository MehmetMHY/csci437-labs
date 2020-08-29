import sys
import time
import cv2


def recedeSqaure(video_file):
    # Read images from a video file in the current folder.
    video_capture = cv2.VideoCapture(video_file)  # Open video capture object
    got_image, bgr_image = video_capture.read()  # Make sure we can read video
    if not got_image:
        print("Cannot read video source")
        sys.exit()

    img_height = bgr_image.shape[0]
    img_width = bgr_image.shape[1]
    cx = int(round(img_width / 2))
    cy = int(round(img_height / 2))
    fx = 500
    fy = 500

    # x, y, z
    z = 1.0
    p1 = [-1.0, -1.0, z]
    p2 = [1.0, -1.0, z]
    p3 = [1.0, 1.0, z]
    p4 = [-1.0, 1.0, z]

    frame = 0

    # Read and show images until end of video is reached.
    while True:
        got_image, bgr_image = video_capture.read()
        if not got_image:
            break  # End of video; exit the while loop

        frame = frame + 1

        x = int(fx * p1[0]) / (p1[2] + z) + cx
        y = int(fy * p1[1]) / (p1[2] + z) + cy
        pos1 = cv2.drawMarker(bgr_image, position=(int(x), int(y)), color=(0, 0, 255), markerType=cv2.MARKER_SQUARE)

        x = int(fx * p2[0]) / (p2[2] + z) + cx
        y = int(fy * p2[1]) / (p2[2] + z) + cy
        pos2 = cv2.drawMarker(bgr_image, position=(int(x), int(y)), color=(0, 0, 255), markerType=cv2.MARKER_SQUARE)

        x = int(fx * p3[0]) / (p3[2] + z) + cx
        y = int(fy * p3[1]) / (p3[2] + z) + cy
        pos3 = cv2.drawMarker(bgr_image, position=(int(x), int(y)), color=(0, 0, 255), markerType=cv2.MARKER_SQUARE)

        x = int(fx * p4[0]) / (p4[2] + z) + cx
        y = int(fy * p4[1]) / (p4[2] + z) + cy
        pos4 = cv2.drawMarker(bgr_image, position=(int(x), int(y)), color=(0, 0, 255), markerType=cv2.MARKER_SQUARE)

        cv2.putText(bgr_image, text=str(frame), org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5,
                    color=(0, 255, 0))

        # cv2.namedWindow("Lab 1: OpenCV-Python Basics", cv2.WINDOW_NORMAL)
        cv2.imshow("Lab 1: OpenCV-Python Basics", bgr_image)

        # Wait for xx msec (0 means wait till a keypress).
        cv2.waitKey(30)
        z = z + 0.1


if __name__ == "__main__":
    recedeSqaure("earth.wmv")
    print("Enter CTRL-C To Exit")
    time.sleep(100)
