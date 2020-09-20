import cv2
import numpy as np

low_thresholds = [50, 50, 50]
high_thresholds = [250, 250, 250]

def main():
    bgr_img = cv2.imread("stop0.jpg")
    image_height = bgr_img.shape[0]
    image_width = bgr_img.shape[1]

    cv2.imshow("Input image", bgr_img)

    # Convert BGR to HSV.
    hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV image", hsv_img)

    # Split into the different bands.
    planes = cv2.split(hsv_img)
    windowNames = ["Hue image", "Saturation image", "Gray image"]
    for i in range(3):
        cv2.namedWindow(windowNames[i])

    # Create trackbars.
    for i in range(3):
        cv2.createTrackbar("Low", windowNames[i], low_thresholds[i], 255, nothing)
        cv2.createTrackbar("High", windowNames[i], high_thresholds[i], 255, nothing)

    while True:
        # Create output thresholded image.
        thresh_img = np.full((image_height, image_width), 255, dtype=np.uint8)

        for i in range(3):
            low_val = cv2.getTrackbarPos("Low", windowNames[i])
            high_val = cv2.getTrackbarPos("High", windowNames[i])

            _, low_img = cv2.threshold(planes[i], low_val, 255, cv2.THRESH_BINARY)
            _, high_img = cv2.threshold(planes[i], high_val, 255, cv2.THRESH_BINARY_INV)

            thresh_band_img = cv2.bitwise_and(low_img, high_img)
            cv2.imshow(windowNames[i], thresh_band_img)

            # AND with output thresholded image.
            thresh_img = cv2.bitwise_and(thresh_img, thresh_band_img)

        cv2.imshow("Output thresholded image", thresh_img)
        if not cv2.waitKey(100) == -1:
            break

def nothing(x):
    pass

if __name__ == "__main__":
    main()