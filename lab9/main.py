# Lab 9

# Alot of credit goes to the lecture slides, thank you

import os
import cv2
import glob
import numpy as np

# mouse callback function
def get_xy(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        window_name, image, point_list = param  # Unpack parameters
        cv2.rectangle(image, pt1=(x-15, y-15), pt2=(x+15, y+15), color=(0,0,255),thickness=3)
        cv2.imshow(window_name, image)
        print((x, y))
        point_list.append((x, y))

# Detect features in the image and return the keypoints and descriptors.
def detect_features(bgr_img, show_features=False):
    detector = cv2.xfeatures2d.SURF_create(
        hessianThreshold=100,  # default = 100
        nOctaves=4,  # default = 4
        nOctaveLayers=3,  # default = 3
        extended=False,  # default = False
        upright=False  # default = False
    )

    # Extract keypoints and descriptors from image.
    gray_image = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = detector.detectAndCompute(gray_image, mask=None)

    # Optionally draw detected keypoints.
    if show_features:
        # Possible flags: DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, DRAW_MATCHES_FLAGS_DEFAULT
        bgr_display = bgr_img.copy()
        cv2.drawKeypoints(image=bgr_display, keypoints=keypoints,
                          outImage=bgr_display,
                          flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #cv2.imshow("Features", bgr_display)
        print("Number of keypoints: ", len(keypoints))
        #cv2.waitKey(0)

    return keypoints, descriptors

# Calculate an affine transformation from the training image to the query image.
def calc_affine_transformation(matches_in_cluster, kp_train, kp_query):
    if len(matches_in_cluster) < 3:
        return None, None
    
    # Estimate affine transformation from training to query image points.
    src_pts = np.float32([kp_train[m.trainIdx].pt for m in matches_in_cluster]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp_query[m.queryIdx].pt for m in matches_in_cluster]).reshape(-1, 1, 2)
    A_train_query, inliers = cv2.estimateAffine2D(
        src_pts, dst_pts,
        method=cv2.RANSAC,
        ransacReprojThreshold=3,    # Default = 3
        maxIters=2000,              # Default = 2000
        confidence=0.99,            # Default = 0.99
        refineIters=10              # Default = 10
    )

    return A_train_query, inliers

IMAGE_DIRECTORY = "images"
TRAINING_IMAGE_NAME = "book1.pgm"
QUERY_IMAGE_NAME = "Img01.pgm"

MINIMUM_MATCHES = 15 # inlier matches

def draw_square(image, x, y):
    cv2.rectangle(image, pt1=(x-15, y-15), pt2=(x+15, y+15), color=(0,0,255),thickness=3)

def function(training, query):
    #file_path = os.path.join(IMAGE_DIRECTORY, TRAINING_IMAGE_NAME)
    #assert(os.path.exists(file_path))
    bgr_train = cv2.imread(training)     # Get training image
    #file_path = os.path.join(IMAGE_DIRECTORY, QUERY_IMAGE_NAME)
    #assert(os.path.exists(file_path))
    bgr_query = cv2.imread(query)     # Get query image

    # Show input images.
    #cv2.imshow("Training image", bgr_train)

    # ### Use Mouse To Get Points. This is Temp:
    # window_name = "Training image" ; ptsA = [] ; displayA = bgr_train.copy()
    # cv2.setMouseCallback(window_name, on_mouse=get_xy, param=(window_name, displayA, ptsA))
    # print("Click on points. Hit ESC to exit and continue.")
    # while True:
    #     if cv2.waitKey(100) == 27:  # ESC is ASCII code 27
    #         break

    #cv2.imshow("Query image", bgr_query)

    # Extract keypoints and descriptors.
    kp_train, desc_train = detect_features(bgr_train, show_features=False)
    kp_query, desc_query = detect_features(bgr_query, show_features=False)

    matcher = cv2.BFMatcher.create(cv2.NORM_L2)

    # Match query image descriptors to the training image.
    # Use k nearest neighbor matching and apply ratio test.
    matches = matcher.knnMatch(desc_query, desc_train, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good.append(m)
    matches = good
    print("Number of raw matches between training and query: ", len(matches))

    bgr_matches = cv2.drawMatches(img1 = bgr_query, 
                                  keypoints1 = kp_query,
                                  img2 = bgr_train, 
                                  keypoints2 = kp_train,
                                  matches1to2 = matches, 
                                  matchesMask = None, 
                                  outImg = None)
    
    #cv2.imshow("All matches", bgr_matches)

    # Calculate an affine transformation from the training image to the query image.
    A_train_query, inliers = calc_affine_transformation(matches, kp_train, kp_query)

    print(A_train_query)

    matches = [matches[i] for i in range(len(matches)) if inliers[i] == 1]

    draw_square(bgr_train, 300, 240)
    draw_square(bgr_train, 300, 320)
    draw_square(bgr_train, 460, 235)

    bgr_matches = cv2.drawMatches(img1 = bgr_query, 
                                  keypoints1 = kp_query,
                                  img2 = bgr_train, 
                                  keypoints2 = kp_train,
                                  matches1to2 = matches,
                                  matchesMask = None, 
                                  outImg = None)

    temp = np.array([[300, 240], [300, 320], [460, 235]])
    temp = temp.T

    print(temp)

    temp1 = A_train_query * temp
    
    xT = temp1[0]
    yT = temp1[1]

    draw_square(bgr_matches, abs(int(xT[0])), abs(int(yT[0])))
    draw_square(bgr_matches, abs(int(xT[1])), abs(int(yT[1])))
    draw_square(bgr_matches, abs(int(xT[2])), abs(int(yT[2])))

    
    cv2.imshow("Inlier matches", bgr_matches)

    # Apply the affine warp to warp the training image to the query image.
    if A_train_query is not None and sum(inliers) >= MINIMUM_MATCHES:
        # Object detected! Warp the training image to the query image and blend the images.
        print("Object detected! Found %d inlier matches" % sum(inliers))
        warped_training = cv2.warpAffine(src=bgr_train, M=A_train_query,dsize=(bgr_query.shape[1], bgr_query.shape[0]))

        # Blend the images.
        blended_image = bgr_query / 2
        blended_image[:, : ,1] += warped_training[:, :, 1] / 2
        blended_image[:, :, 2] += warped_training[:, :, 2] / 2
        #cv2.imshow("Blended", blended_image.astype(np.uint8))
    else:
        print("Object not detected; can't fit an affine transform")
    
    #cv2.waitKey(0)




QUERY_IMAGE_DIRECTORY = "./query_images/"

def main():
    # Get a list of the query images.
    assert (os.path.exists(QUERY_IMAGE_DIRECTORY))
    image_file_names = glob.glob(os.path.join(QUERY_IMAGE_DIRECTORY, "*.png"))
    assert (len(image_file_names) > 0)

    # Process each query image.
    for image_file_name in image_file_names:

        function("printer_001.png", image_file_name)

        # Wait for xx msec (0 means wait till a keypress).
        key_pressed = cv2.waitKey(0) & 0xFF
        if key_pressed == 27:
            break # Quit on ESC
        #break

# def main():
#     function("printer_001.png", "./query_images/positive_000.png")

if __name__ == "__main__":
    main()


