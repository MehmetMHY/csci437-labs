# Name: Bao (Jean) Duong & Mehmet Yilmaz
# Date: 9-20-20
# Class: Computer Vision
# Assignment: Lab 4 - Color Segmentation

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

    # Create output thresholded image.
    thresh_img = np.full((image_height, image_width), 255, dtype=np.uint8)

    for i in range(3):
        low_val = low_thresholds[i]
        high_val = high_thresholds[i]

        if (i == 0):
            # Manually threshold Hue (low: 95 | high: 190).
            _, low_img = cv2.threshold(planes[0], 115, 255, cv2.THRESH_BINARY)
            _, high_img = cv2.threshold(planes[0], 190, 255, cv2.THRESH_BINARY_INV)

            # Manually threshold Saturating (low: 90 | high: 255).
        elif (i == 1):
            _, low_img = cv2.threshold(planes[1], 90, 255, cv2.THRESH_BINARY)
            _, high_img = cv2.threshold(planes[1], 255, 255, cv2.THRESH_BINARY_INV)

            # Manually threshold Gray (low: 107 | high: 255).
        elif (i == 2):
            _, low_img = cv2.threshold(planes[2], 70, 255, cv2.THRESH_BINARY)
            _, high_img = cv2.threshold(planes[2], 255, 255, cv2.THRESH_BINARY_INV)

        thresh_band_img = cv2.bitwise_and(low_img, high_img)
        cv2.imshow(windowNames[i], thresh_band_img)

        # AND with output thresholded image.
        thresh_img = cv2.bitwise_and(thresh_img, thresh_band_img)

        # Save picture after it has been threshold
        output = cv2.imwrite("output0.png", thresh_img)

        # Morphological closing and opening on binary picture.
        morph()

def morph():
    # Read in oput images, but have to be manually edited.
    binary_img = cv2.imread("output0.png")

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)
    binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)
    filter = cv2.imwrite("filtered0.png", binary_img)

if __name__ == "__main__":
    main()