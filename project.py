import cv2 as cv
#import numpy as np
#import matplotlib.pyplot as plt


## LOAD VIDEOS
LCameraView= cv.VideoCapture('robotL.avi' )
RCameraView= cv.VideoCapture('robotR.avi')
 
# SHOW VIDEO FRAMES
def playVideos(LCameraView, RCameraView):
    while LCameraView.isOpened() and RCameraView.isOpened():
        Lret, Lframe = LCameraView.read()
        Rret, Rframe = LCameraView.read()
     
        # if frame is read correctly ret is True
        if not Lret or not Rret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        Lgray = cv.cvtColor(Lframe, cv.COLOR_BGR2GRAY)
        Rgray = cv.cvtColor(Rframe, cv.COLOR_BGR2GRAY)
        cv.imshow("Lframe", Lgray) 
        cv.imshow("Rframe", Rgray) 
        #cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break
     
    LCameraView.release()
    RCameraView.release()
    cv.destroyAllWindows()

playVideos(LCameraView,RCameraView)
