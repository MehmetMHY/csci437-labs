import math
import cv2
import numpy as np
import vanishing as v

def resize(bgr_img):
    scale_percent = 30  # percent of original size
    width = int(bgr_img.shape[1] * scale_percent / 100)
    height = int(bgr_img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image.
    bgr_img = cv2.resize(bgr_img, dim, interpolation=cv2.INTER_AREA)

    return bgr_img

def main(filename, message):
    print(message)

    bgr_img = cv2.imread(filename)

    bgr_img = resize(bgr_img)

    gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)

    # Get the image height and width.
    image_width = bgr_img.shape[1]
    image_height = bgr_img.shape[0]

    SIGMA_BLUR = 1.0

    # Smooth the image with a Gaussian filter.  If sigma is not provided, it
    # computes it automatically using   sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8.
    gray_img = cv2.GaussianBlur(
        src=gray_img,
        ksize=(0, 0),  # kernel size (should be odd numbers; if 0, compute it from sigma)
        sigmaX=SIGMA_BLUR,
        sigmaY=SIGMA_BLUR)

    # Pick a threshold such that we get a relatively small number of edge points.
    MIN_FRACT_EDGES = 0.05
    MAX_FRACT_EDGES = 0.08
    thresh_canny = 1

    edge_img = cv2.Canny(
        image=gray_img,
        apertureSize=3,  # size of Sobel operator
        threshold1=thresh_canny,  # lower threshold
        threshold2=3 * thresh_canny,  # upper threshold
        L2gradient=True)  # use more accurate L2 norm

    cv2.imwrite(str(filename[:-4])+"_Canny.png", edge_img)

    cv2.imshow("project", edge_img)
    cv2.waitKey(0)

    while np.sum(edge_img)/255 < MIN_FRACT_EDGES * (image_width * image_height):
        print("Decreasing threshold ...")
        thresh_canny *= 0.9

        edge_img = cv2.Canny(
            image=gray_img,
            apertureSize=3, # size of Sobel operator
            threshold1=thresh_canny,  # lower threshold
            threshold2=3 * thresh_canny,  # upper threshold
            L2gradient=True)  # use more accurate L2 norm

    while np.sum(edge_img) / 255 > MAX_FRACT_EDGES * (image_width * image_height):
        print("Increasing threshold ...")
        thresh_canny *= 1.1
        edge_img = cv2.Canny(
            image=gray_img, apertureSize=3, # size of Sobel operator
            threshold1=thresh_canny,  # lower threshold
            threshold2=3 * thresh_canny,  # upper threshold
            L2gradient=True)  # use more accurate L2 norm

    MIN_HOUGH_VOTES_FRACTION = 0.05  # Minimum points on a line (as fraction of image width)
    MIN_LINE_LENGTH_FRACTION = 0.06

    # Run Hough transform.  The output houghLines has size (N,1,4), where N is #lines.
    # The 3rd dimension has the line segment endpoints: x0,y0,x1,y1.
    houghLines = cv2.HoughLinesP(
        image=edge_img,
        rho=1,
        theta=math.pi / 180,
        threshold=int(image_width * MIN_HOUGH_VOTES_FRACTION),
        lines=None,
        minLineLength=int(image_width * MIN_LINE_LENGTH_FRACTION),
        maxLineGap=10
    )

    print("Number of lines: %d" % len(houghLines))

    # create text file with the complete set of line segments found from HoughLinesP
    output_name = str(filename[:-4]) + "_Line_Points_HoughLinesP.txt"
    output = open(output_name, "a")
    output.write("[Point 1] [Point 2] \n")
    for i in range(len(houghLines)):
        temp = houghLines[i]
        x1, y1, x2, y2 = temp[0]
        final = str([(x1, y1), (x2, y2)]) + "\n"
        final = "(" + str(x1) + ", " + str(y1) + ")->(" + str(x2) + ", " + str(y2) + ") \n"
        output.write(final)
    output.close()
    print(str(output_name) + " file with the complete set of line segments from HoughLinesP has been created!")

    houghLines, final_img = v.find_vanishing_point_directions(houghLines, bgr_img)

    print()

    cv2.imwrite(str(filename[:-4])+"_final.png", final_img)

if __name__ == "__main__":
    files = ["corridor1.jpg", "corridor2.jpg", "corridor3.png"]
    for filename in files:
        main(filename, str(filename + " is processing..."))
    print("DONE")
