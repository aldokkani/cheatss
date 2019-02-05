import time
import numpy as np
import cv2
from mss import mss
import pyautogui
import imutils
from operator import itemgetter

monitor = {'top': 215, 'left': 0, 'width': 1030, 'height': 430}

prev_frame = None

piece_color = True  # True == light and False == dark
moves = []

for i in range(1, 0, -1):
    print(i)
    time.sleep(1)

def copy_move(mvs, d):
    global monitor
    for m in mvs:
        pyautogui.click(m[0] + d, m[1] + monitor['top'])

    pyautogui.click(mvs[-1][0] + d, mvs[-1][1] + monitor['top'])  # click away
    for m in mvs[::-1]:
        pyautogui.click(m[0] + d, m[1] + monitor['top'])


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
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 500:
                continue

            # compute the bounding box for the contour
            (x, y, w, h) = cv2.boundingRect(c)
            print(x + w / 2, y + h / 2)
            moves.append((int(x + w / 2), int(y + h / 2)))

            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if moves:
            # if moves[0][0] < monitor['width'] / 2:
            #     diff = 570
            # else:
            #     diff = -570
            # if len(moves) == 2:
            #     for m in moves:
            #         pyautogui.click(m[0] + diff, m[1] + monitor['top'])
            #
            #     pyautogui.click(moves[-1][0] + diff, moves[-1][1] + monitor['top'])  # click away
            #     for m in moves[::-1]:
            #         pyautogui.click(m[0] + diff, m[1] + monitor['top'])
            #     # copy_move(moves, diff)
            #
            # elif len(moves) == 4:
            #     sm = sorted(moves, key=itemgetter(1))
            #     if sm[3][1]-sm[0][1] < 10:
            #         smoves = sorted(moves)
            #         mwidth = monitor['width']
            #         if smoves[0][0] < mwidth * 0.25 or mwidth * 0.5 < smoves[0][0] < mwidth * 0.75:
            #             pyautogui.click(smoves[3][0] + diff, smoves[3][1] + monitor['top'])
            #             pyautogui.click(smoves[1][0] + diff, smoves[1][1] + monitor['top'])
            #         else:
            #             pyautogui.click(smoves[0][0] + diff, smoves[0][1] + monitor['top'])
            #             pyautogui.click(smoves[2][0] + diff, smoves[2][1] + monitor['top'])
            #     else:
            #         for m in moves:
            #             pyautogui.click(m[0] + diff, m[1] + monitor['top'])
            #
            #         pyautogui.click(moves[-1][0] + diff,
            #                         moves[-1][1] + monitor['top'])  # click away
            #         for m in moves[::-1]:
            #             pyautogui.click(m[0] + diff, m[1] + monitor['top'])

            # update the previous frame
            prev_frame = gray
            moves = []
            print('==========')

        # cv2.imshow("Board", frame)
        # print(f' Loop took {time.time() - frame_start} seconds.')
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
