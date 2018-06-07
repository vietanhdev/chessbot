import numpy as np
import cv2
import os
import pathlib
import neural_chessboard.detector
import importlib
import gc
import neural_chessboard


pathlib.Path('./tmp').mkdir(parents=True, exist_ok=True) 
cap = cv2.VideoCapture(0)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)

while(True):


    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        continue

    # Display the resulting frame
    cv2.imshow('image',frame)
    key = cv2.waitKey(10)

    if key == 13:
        try:
           
            result = neural_chessboard.detector.detect(frame)
            
            cv2.imshow('image', result)
            cv2.waitKey(0)
            
        except:
            print("Error in detecting board")

    elif key & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()