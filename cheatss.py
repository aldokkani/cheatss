import time
import numpy as np
import cv2
from mss import mss

monitor = {'top': 213, 'left': 15, 'width': 448 + 10, 'height': 448 + 5}

counter = 0

with mss() as sct:
    while True:
        # frame_start = time.time()

        board = np.array(sct.grab(monitor))
        board = cv2.cvtColor(board, cv2.COLOR_RGB2GRAY)
        # cv2.imshow('Board', board)

        time.sleep(0.1)

        board2 = np.array(sct.grab(monitor))
        board2 = cv2.cvtColor(board2, cv2.COLOR_RGB2GRAY)

        diff = cv2.absdiff(board, board2)
        # cv2.imshow('Diff', diff)

        if diff.any():
            counter += 1
            print(counter)


        # print(f' Loop took {time.time() - frame_start} seconds.')
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
