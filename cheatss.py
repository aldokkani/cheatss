import time
import numpy as np
import cv2
from mss import mss
import pyautogui
import imutils

monitor = {'top': 0, 'left': 0, 'width': 500, 'height': 800}

prev_frame = None

for i in range(1, 0, -1):
    print(i)
    time.sleep(1)

with mss() as sct:
    while True:
        # frame_start = time.time()

        frame = np.array(sct.grab(monitor))
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if prev_frame is None:
            prev_frame = gray
            continue

        # compute the absolute difference between the current frame and first frame
        frame_delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[1] if imutils.is_cv2() else cnts[0]

        # loop over the contours
        for c in cnts:
            # compute the bounding box for the contour
            (x, y, w, h) = cv2.boundingRect(c)
            print(x + w/2, y + h/2)
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if cnts:
            print('==========')

        # update the previous frame
        prev_frame = gray

        cv2.imshow("Board", frame)
        # print(f' Loop took {time.time() - frame_start} seconds.')
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

# for i in range(3, 0, -1):
#     print(i)
#     time.sleep(1)
#
# pyautogui.click(159, 524)
# pyautogui.click(103, 637)
