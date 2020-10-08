# importing the necessary libraries 
import cv2
import numpy as np


def main():
    cap = readVid('fiveCCC.avi')

    result = cv2.VideoWriter('filename1.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             30, (640, 480))

    frame = 0

    findCCC(cap, frame, result)

    # release the video capture object
    cap.release()
    # Closes all the windows currently opened.
    cv2.destroyAllWindows()


def readVid(file):
    # Creating a VideoCapture object to read the video
    file = cv2.VideoCapture('fiveCCC.avi')

    return file

def findCCC(cap, frame, result):
    # Loop untill the end of the video
    while (cap.isOpened()):

        # Capture frame-by-frame
        got_image, bgr_img = cap.read()

        frame += 1

        # conversion of BGR to grayscale is necessary to apply this operation
        gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

        _, binary_img = cv2.threshold(gray_img, thresh=170, maxval=255, type=cv2.THRESH_BINARY)

        binary_img = cv2.bitwise_not(binary_img)

        # # Clean up using opening + closing.
        ksize = 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
        binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)
        binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

        # Get connected components and region properties.
        num_labels, labels_img, stats, centroids = cv2.connectedComponentsWithStats(binary_img)

        # Draw the frames at the top left of the screen.
        cv2.putText(bgr_img, text=str(frame), org=(20, 50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5,
                    color=(0, 255, 0))

        # Draw rectangles.
        for stat, centroid in zip(stats, centroids):
            x0 = stat[cv2.CC_STAT_LEFT]
            y0 = stat[cv2.CC_STAT_TOP]
            w = stat[cv2.CC_STAT_WIDTH]
            h = stat[cv2.CC_STAT_HEIGHT]
            bgr_img = cv2.rectangle(img=bgr_img, pt1=(x0, y0), pt2=(x0 + w, y0 + h), color=(0, 0, 255), thickness=1)
            cv2.imshow("boxes", bgr_img)

        # Call function to save vid.
        saveVid(result, bgr_img)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

# Function to save result vid.
def saveVid(result, bgr_img):
    result.write(bgr_img)

if __name__ == "__main__":
    main()
