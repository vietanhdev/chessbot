import numpy as np
import cv2
import os
import neural_chessboard.detector as board_detector
import gc
import neural_chessboard
import time
from threading import Thread, Lock


# Result windows
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('canny', cv2.WINDOW_NORMAL)
cv2.namedWindow('origin', cv2.WINDOW_NORMAL)


# Timing variables
beginTime = 0
endTime = 0


# Global variable to save read frame from camera
# and mutex for locking it
globalFrame = False
mutex = Lock()


# Function to continuously get frame from camera and save to globalFrame
# Run it as a thread
def getFrames():
    global mutex
    global globalFrame
    
    cap = cv2.VideoCapture(-1)

    cap.set(3,320)
    cap.set(4,240)
    cap.set(5,5)

    while True:

        ret, tmpFrame = cap.read()

        if not ret:
            continue
        
        # Save to shared variable
        mutex.acquire()
        globalFrame = tmpFrame
        mutex.release()



# Initialize the get_frames thread
t = Thread(target=getFrames)
t.start()



def measureTime(title):
    global beginTime
    global endTime
    # Measure time
    endTime = time.process_time()
    timeLast = endTime - beginTime
    print(title + ". Time: " + str(timeLast))
    beginTime = endTime


while(True):
    
    print("Start processing a new frame")
    mutex.acquire()
    frame = globalFrame
    mutex.release()
    
    
    # Display the origin frame
    cv2.imshow('origin', frame)
    cv2.waitKey(10)
    
    # Get key from keyboard
    key = cv2.waitKey(10)

    if key == 13:
        # try:
           
            transformMatrices = board_detector.detect(frame)
            result = board_detector.getCropImage(frame, transformMatrices)
            
            cv2.imshow('image', result)
            # cv2.waitKey(0)

            # Use tranformMatrices to crop 10000 next images
            for _ in range(10000):
				
                print("Start processing a new frame")
                mutex.acquire()
                frame = globalFrame
                mutex.release()
                
                measureTime("Aquire a new frame")

                crop = board_detector.getCropImage(frame, transformMatrices)
                
                measureTime("Crop")

                # Unpack shape of crop
                rows,cols,channels = crop.shape

                square_size = int (rows / 8)

                # Canny
                canny = cv2.Canny(crop, 50, 100)
                
                measureTime("Canny")


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


                measureTime("Detect")

                cv2.imshow('canny', canny)
                cv2.waitKey(10)

                cv2.imshow('image', crop)
                cv2.waitKey(10)
                
                measureTime("Show result")
            
        # except:
        #     print("Error in detecting board")

    elif key & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
os._exit()
