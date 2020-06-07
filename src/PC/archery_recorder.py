#!/usr/bin/env python3

"""
version : v1.0.5-alpha

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
import time
import queue
import os.path


def main(cap, writer, q, prev_time, avgfps, flag_recording, delay, file_number, change_resolution, resolution, change_camera, camera):
    if change_camera == True:
        if cap != None:
            cap.release()

        cap = cv2.VideoCapture(camera)
        perv_camera = camera

        change_resolution = True
        change_camera = False

    if change_resolution == True:
        while q.qsize():
            q.get()

        if resolution == 0:
            cap.set(3, 720)
            cap.set(4, 480)
        elif resolution == 1:
            cap.set(3, 1280)
            cap.set(4, 720)
        elif resolution == 2:
            cap.set(3, 1920)
            cap.set(4, 1080)
        elif resolution == 3:
            cap.set(3, 2048)
            cap.set(4, 1080)
        elif resolution == 4:
            cap.set(3, 2560)
            cap.set(4, 1440)
        elif resolution == 5:
            cap.set(3, 3840)
            cap.set(4, 2160)
        elif resolution == 6:
            cap.set(3, 4096)
            cap.set(4, 2160)
        elif resolution == 7:
            cap.set(3, 8192)
            cap.set(4, 4320)

        change_resolution = False

    ret, img_color = cap.read()
    # rotate: img_color = cv2.flip(img_color, -1)  

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

                img_color = cv2.flip(img_color, 1)

                cv2.namedWindow("Preview", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.putText(img_color, 'REC-O' if flag_recording else 'REC-X', (0, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                            (0, 0, 255) if flag_recording else (0, 255, 0))
                cv2.putText(img_color, 'Cam: ' + str(camera), (0, 66), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0))
                cv2.putText(img_color, 'SD' if resolution == 0 else 'HD' if resolution == 1 else 'FHD' if resolution == 2 else '2K' if resolution == 3 else 'QHD' if resolution == 4 else 'UHD' if resolution == 5 else '4K' if resolution == 6 else '8K', (99, 66), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0))
                cv2.putText(img_color, 'FPS: ' + str(int(avgfps)), (0, 99), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0))
                cv2.putText(img_color, 'Delay: ' + str(delay), (99, 99), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0))

                # rotate: img_color = cv2.flip(img_color, -1)

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

            file_number += 1
            file_name = 'archery_video-' + str(file_number) + '.avi'
            while os.path.isfile(file_name):
                file_number += 1
                file_name = 'archery_video-' + str(file_number) + '.avi'

            writer = cv2.VideoWriter(file_name, fourcc,
                                     avgfps, (width, height))
    elif 48 <= key_input and key_input <= 57:
        change_camera = True
        camera = key_input-48
    elif key_input == 123 or key_input == 108:
        change_resolution = True
        resolution -= 1
    elif key_input == 124 or key_input == 104:
        change_resolution = True
        resolution += 1
    elif key_input == 125 or key_input == 100:
        delay -= 1
    elif key_input == 126 or key_input == 117:
        delay += 1

    if resolution < 0:
        change_resolution = False
        resolution = 0
    elif resolution > 7:
        change_resolution = False
        resolution = 7

    try:
        main(cap, writer, q, crnt_time, avgfps, flag_recording, delay, file_number, change_resolution, resolution, change_camera, camera)
    except RecursionError:
        pass
    except Exception as ex:
        print('exception: ' + str(ex))


q = queue.Queue()

main(None, None, q, 0, 0, False, 0, 0, True, 0, True, 0)
