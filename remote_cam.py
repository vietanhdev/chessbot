import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError
import sys
import os
import readchar
import subprocess as subp
import urllib, cStringIO


class Cam():

    def __init__(self, url):
        self.stream = requests.get(url, stream=True)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
        print "camera initialised"

        
    def start(self):
        self.thread.start()
        print("camera stream started")
        
    def run(self):
        bytes = ''       
        while not self.thread_cancelled:
            try:
                bytes += self.stream.raw.read(1024)
                a = bytes.find('\xff\xd8')
                b = bytes.find('\xff\xd9')
                if a!=-1 and b!=-1:
                    jpg = bytes[a:b+2]
                    bytes= bytes[b+2:]
                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                    cv2.imshow('cam',img)
                    cv2.imwrite('tmp/img.png', img)
                    if cv2.waitKey(1) == 27:
                        cline = "python3 neural-chessboard/main.py detect --input tmp/img.png --output tmp/result.png"
                        if not os.system(str(cline)):
                            result = cv2.imread("tmp/result.img")
                            cv2.imshow('result', result)

                    # key = readchar.readkey()
                    # if key == 'p':
                    #     cline = "python3 neural-chessboard/main.py detect --input tmp/img.png --output tmp/result.png"
                    #     if not os.system(str(cline)):
                    #         result = cv2.imread("tmp/result.img")
                    #         cv2.imshow('result', result)
                    # elif key == 'q':
                    #     exit(0)
            except ThreadError:
                self.thread_cancelled = True

            
    def is_running(self):
        return self.thread.isAlive()
        
        
    def shut_down(self):
        self.thread_cancelled = True
        #block while waiting for thread to terminate
        while self.thread.isAlive():
            time.sleep(1)
        
        return True

  
    
if __name__ == "__main__":
  url = 'http://192.168.1.47:8080/videofeed'
  cam = Cam(url)
  cam.start()

