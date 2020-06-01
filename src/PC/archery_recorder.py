#!/usr/bin/env python3

"""
version : v1.0.1-alpha

MIT License

Copyright (c) 2020 Kyung-ha Lee <i_am@nulleekh.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import cv2
import threading
import time
from datetime import datetime
import queue


def main(cap, writer, q, prev_time, avgfps, flag_recording, delay):
    ret, img_color = cap.read()

    crnt_time = time.time()
    interval = crnt_time - prev_time
    fps = 1 / interval
    avgfps = (avgfps + fps) / 2

    if ret == True:
        if flag_recording:
            writer.write(img_color)
        if q.qsize() > avgfps * delay:
            q.put(img_color)
            while q.qsize() > avgfps * delay:
                img_color = q.get()

                cv2.namedWindow("Preview", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.putText(img_color, 'FPS: ' + str(int(avgfps)), (0, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0))
                cv2.putText(img_color, 'Delay: ' + str(delay), (0, 66), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0))
                cv2.putText(img_color, 'REC-O' if flag_recording else 'REC-X', (0, 99), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                            (0, 255, 0))
                cv2.imshow("Preview", img_color)
        else:
            q.put(img_color)

    key_input = cv2.waitKey(1) & 0xFF

    if key_input == 27:
        if writer != None:
            writer.release()
        cap.release()
        cv2.destroyAllWindows()
        exit()
    elif key_input == 32:
        if flag_recording == True:
            flag_recording = False

            writer.release()
        else:
            flag_recording = True

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter('archery_video-' + str(datetime.today().strftime("%Y%M%d%H%M%S")) + '.avi', fourcc,
                                     avgfps, (width, height))
    elif key_input == 125:
        delay -= 1
    elif key_input == 126:
        delay += 1

    try:
        threading.Timer(0.0001, main(cap, writer, q, crnt_time, avgfps, flag_recording, delay)).start()
    except RecursionError:
        pass
    except Exception as ex:
        print('exception: ' + ex)


cap = cv2.VideoCapture(0)

q = queue.Queue()

main(cap, None, q, 0, 0, False, 0)
