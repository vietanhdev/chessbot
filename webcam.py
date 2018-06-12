import numpy as np
import cv2
import os
import pathlib
import neural_chessboard.detector as board_detector
import importlib
import gc
import neural_chessboard


pathlib.Path('./tmp').mkdir(parents=True, exist_ok=True) 
cap = cv2.VideoCapture(1)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('canny', cv2.WINDOW_NORMAL)

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
                # Capture frame-by-frame
                ret, frame = cap.read()
                if not ret:
                    continue

                crop = board_detector.getCropImage(frame, transformMatrices)

                # Unpack shape of crop
                rows,cols,channels = crop.shape

                # crop[:row/8,:cols/8] = (0,0,255)

                square_size = int (rows / 8)

                np.count_nonzero

                # Canny
                canny = cv2.Canny(crop, 50, 100)


                # Detect if there is a piece
                # Padding to the center of the square
                borderPadding = 25

                font = cv2.FONT_HERSHEY_SIMPLEX
                for i in range(8):
                    for j in range(8):

                        sq = canny[i*square_size + 2 * borderPadding:(i+1)*square_size - borderPadding * 2:, j*square_size + 2 * borderPadding:(j+1)*square_size - borderPadding * 2:]

                        crop[i*square_size + borderPadding:i*square_size + borderPadding + 10:, j*square_size + borderPadding:j*square_size + borderPadding + 10:, ::] = (0,255,0)
                        
                        # Count non zero point
                        numOfNonZero = cv2.countNonZero(sq)

                        if (numOfNonZero > 40):
                            crop[i*square_size + borderPadding:(i+1)*square_size - borderPadding * 2:, j*square_size + borderPadding:(j+1)*square_size - borderPadding * 2:, ::] = (0,0,255)


                cv2.imshow('canny', canny)
                cv2.waitKey(1)

                cv2.imshow('image', crop)
                cv2.waitKey(1)
            
        # except:
        #     print("Error in detecting board")

    elif key & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()