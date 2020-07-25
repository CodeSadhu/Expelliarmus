import numpy as np
import cv2
import time

capture = cv2.VideoCapture(0)   # VideoCapture(0) imples the number of cameras, 0 indexed
# capture = cv2.VideoCapture("Desktop/ABC.mp4") can be done to use prerecorded videos as well!

time.sleep(3)   # Time window for the camera to focus properly

bg = 0  # Background image that gets displayed when clock is placed

for i in range(40):
    #For camera to capture the background properly
    ret, bg = capture.read()
    #capture.read() will return 2 params: 1. bool value to check whether bg was captured or not & 2. bg itself

while(capture.isOpened()):
    # Pretty self explanatory
    ret, img = capture.read()
    if not ret:
        # If not capturing, break
        break

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    low_red = np.array([0, 120, 70])
    up_red = np.array([10, 255, 255])

    mask1 = cv2.inRange(hsv, low_red, up_red) # Differentiating between the cloaking object and background

    low_red = np.array([170, 120, 70])
    up_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, low_red, up_red)

    mask1 += mask2

    mask1 = cv2.morphologyEx(
        mask1,
        cv2.MORPH_OPEN,         # Remove noise from image
        np.ones(
            (3, 3),
            np.uint8
        ),
        iterations=3
    )

    mask1 = cv2.morphologyEx(
        mask1,
        cv2.MORPH_DILATE,       # Smoothen the image
        np.ones(
            (3, 3),
            np.uint8
        ),
        iterations=2
    )

    mask2 = cv2.bitwise_not(mask1)  # Store everything in mask2 except cloaking object (mask1)

    res1 = cv2.bitwise_and(
        bg,
        bg,                         # Differentiate cloak color from bg color
        mask=mask1
    )

    res2 = cv2.bitwise_and(
        img,
        img,
        mask=mask2
    )

    result = cv2.addWeighted(res1, 1, res2, 1, 0)       # Add two images using Alpha (1), Beta (1), Gamma (0) values. Pure mathematical shit.

    cv2.imshow("Peek-a-boo!", result)
    escape = cv2.waitKey(10)    # Wait for user to press ESC key
    if escape == 27:
        # 27: ASCII value of ESC key
        break

capture.release()
