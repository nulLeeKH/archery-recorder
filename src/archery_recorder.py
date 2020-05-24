#!/usr/bin/env python3

import cv2
import threading
import time
from datetime import datetime
import queue

monitoring_delay = 5

def main(cap, writer, q, prev_time, avgfps, flag_recording):
    ret,img_color = cap.read()

    crnt_time = time.time()
    interval = crnt_time - prev_time
    fps = 1/interval
    avgfps = (avgfps+fps)/2

    if ret == True:
        if flag_recording:
            writer.write(img_color)
        if q.qsize() >= avgfps * monitoring_delay:
            q.put(img_color)    
            while q.qsize() >= avgfps * monitoring_delay:
                img_color = q.get()

                cv2.namedWindow("Preview", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("Preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.putText(img_color, str(int(avgfps)), (0, 33), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                cv2.putText(img_color, 'REC-O' if flag_recording else 'REC-X', (0, 66), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
                cv2.imshow("Preview", img_color)
        else:
            q.put(img_color)

    key_input = cv2.waitKey(1)&0xFF

    if key_input == 27:
        if writer != None:
            writer.release()
        cap.release()
        cv2.destroyAllWindows()
        exit()
    elif key_input ==32:
        if flag_recording == True:
            flag_recording = False

            writer.release()
        else:
            flag_recording = True

            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter('archery_video-' + str(datetime.today().strftime("%Y%M%d%H%M%S")) + '.avi', fourcc, avgfps, (width, height))

    try:
        threading.Timer(0.0001, main(cap, writer, q, crnt_time, avgfps, flag_recording)).start()
    except RecursionError:
        pass
            
    

cap = cv2.VideoCapture(0)

q = queue.Queue()

main(cap, None, q, 0, 0, False)
