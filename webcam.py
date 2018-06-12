import numpy as np
import cv2
import os
import pathlib
import neural_chessboard.detector as board_detector
import importlib
import gc
import neural_chessboard
import time


pathlib.Path('./tmp').mkdir(parents=True, exist_ok=True) 
cap = cv2.VideoCapture(0)

cap.set(3,320)
cap.set(4,240)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('canny', cv2.WINDOW_NORMAL)

beginTime = 0
endTime = 0

while(True):


    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        continue

    # Display the resulting frame
    cv2.imshow('image',frame)
    key = cv2.waitKey(10)

    if key == 13:
        # try:
           
            transformMatrices = board_detector.detect(frame)
            result = board_detector.getCropImage(frame, transformMatrices)
            
            cv2.imshow('image', result)
            # cv2.waitKey(0)

            # Use tranformMatrices to crop 100 next images
            for _ in range(10000):
				
                # Measure time
                endTime = time.process_time()
                timeLast = endTime - beginTime
                print("Time: " + str(timeLast))
                beginTime = endTime
				
				
                # Capture frame-by-frame
                ret, frame = cap.read()
                if not ret:
                    continue

                # Measure time
                endTime = time.process_time()
                timeLast = endTime - beginTime
                print("Capture Time: " + str(timeLast))
                beginTime = endTime
        

                crop = board_detector.getCropImage(frame, transformMatrices)
                
                # Measure time
                endTime = time.process_time()
                timeLast = endTime - beginTime
                print("Crop Time: " + str(timeLast))
                beginTime = endTime

                # Unpack shape of crop
                rows,cols,channels = crop.shape

                square_size = int (rows / 8)

                # Canny
                canny = cv2.Canny(crop, 50, 100)
                
                # Measure time
                endTime = time.process_time()
                timeLast = endTime - beginTime
                print("Canny Time: " + str(timeLast))
                beginTime = endTime


                # Detect if there is a piece
                # Padding to the center of the square
                borderPadding = 15

                font = cv2.FONT_HERSHEY_SIMPLEX
                for i in range(8):
                    for j in range(8):

                        sq = canny[i*square_size + 2 * borderPadding:(i+1)*square_size - borderPadding * 2:, j*square_size + 2 * borderPadding:(j+1)*square_size - borderPadding * 2:]

                        crop[i*square_size + borderPadding:i*square_size + borderPadding + 10:, j*square_size + borderPadding:j*square_size + borderPadding + 10:, ::] = (0,255,0)
                        
                        # Count non zero point
                        numOfNonZero = cv2.countNonZero(sq)

                        if (numOfNonZero > 40):
                            crop[i*square_size + borderPadding:(i+1)*square_size - borderPadding * 2:, j*square_size + borderPadding:(j+1)*square_size - borderPadding * 2:, ::] = (0,0,255)


                 # Measure time
                endTime = time.process_time()
                timeLast = endTime - beginTime
                print("Detect Time: " + str(timeLast))
                beginTime = endTime

                #~ cv2.imshow('canny', canny)
                #~ cv2.waitKey(1)

                #~ cv2.imshow('image', crop)
                #~ cv2.waitKey(1)
            
        # except:
        #     print("Error in detecting board")

    elif key & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
