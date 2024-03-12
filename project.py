import cv2 as cv
#import numpy as np
#import matplotlib.pyplot as plt

import os
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "wayland"

LCameraView= cv.VideoCapture('robotL.avi' )
RCameraView= cv.VideoCapture('robotR.avi')
 
while LCameraView.isOpened() :
    ret, frame = LCameraView.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        print(ret)
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("frame", gray) 
    #cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
 
LCameraView.release()
RCameraView.release()
cv.destroyAllWindows()
