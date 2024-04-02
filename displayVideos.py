import argparse
import cv2 as cv
from utils import imshow

# GET ARGUMENTS
def getParams():
    parser = argparse.ArgumentParser(prog='CVproject',description='computer vision project',epilog='credits carnivuth')
    parser.add_argument('-i','--imageDim',default='100',help='image box dimension to cut from original frames for computation',type=int)
    return parser.parse_args()

# SHOW VIDEO FRAMES IN GRAYSCALE
def playVideos(LCameraView, RCameraView,boxSize):
    while LCameraView.isOpened() and RCameraView.isOpened():
        Lret, Lframe = LCameraView.read()
        Rret, Rframe = LCameraView.read()
     
        # if frame is read correctly ret is True
        if not Lret or not Rret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        imgL= cv.cvtColor(Lframe, cv.COLOR_BGR2GRAY)
        imgR= cv.cvtColor(Rframe, cv.COLOR_BGR2GRAY)
        # Calculate center frame
        center = Lframe.shape
        centerY = int(center[0]/2)
        centerX = int(center[1]/2)
        halfsize = int(boxSize/2)

        
        imgLCutted = imgL[centerY-halfsize:centerY+halfsize, centerX-halfsize:centerX+halfsize]
        imgRCutted = imgR[centerY-halfsize:centerY+halfsize, centerX-halfsize:centerX+halfsize]
        imshow("videoL","videoL",imgLCutted)
        imshow("videoR","videoR",imgRCutted)

        if cv.waitKey(1) == ord('q'):
            break
     
    LCameraView.release()
    RCameraView.release()


# LOAD VIDEOS
LCameraView= cv.VideoCapture('robotL.avi')
RCameraView= cv.VideoCapture('robotR.avi')

# READ PARAMS
args =getParams()

playVideos(LCameraView,RCameraView,args.imageDim)
