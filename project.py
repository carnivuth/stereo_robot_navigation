import argparse
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
 
# chessboard dimensions
H = 178
W = 125

# allarm trigger limit
MINIMUM_DISTANCE =  0.8

# chessboard parameters
CB_INNER_W_CORNERS = 6
CB_INNER_H_CORNERS = 8

# camera parameters
FOCAL_LENGHT =  567.2 
BASELINE = 92.226 

# display image
def imshow(wname,title, img):
    plt.figure(wname); 
    plt.clf()
    plt.imshow(img)
    plt.title(title)
    plt.pause(0.000001)

# GET ARGUMENTS
def getParams():
    parser = argparse.ArgumentParser(prog='CVproject',description='computer vision project',epilog='credits carnivuth')
    parser.add_argument('-d','--numDisparities',default='128',help='numDisparities parameter for disparity map algorithm',type=int)
    parser.add_argument('-b','--blockSize',default='13',help='blocksize parameter for disparity map algorithm', type=int)
    parser.add_argument('-c','--chessboard',help='Compute chessboard recognition',action='store_true')
    return parser.parse_args()

# FIND CHESBOARD IN THE IMAGE
def computeChessboard(imgL,z):
    ret,corners = cv.findChessboardCorners(imgL ,(CB_INNER_H_CORNERS,CB_INNER_W_CORNERS))

    if ret == True:

        # draw chessboard corners in the left image
        cv.drawChessboardCorners(imgL, (CB_INNER_H_CORNERS,CB_INNER_W_CORNERS), corners, ret)
        imshow("chessboard",'chessboard',imgL)

        # get w value WRONG VALUES
        h =abs(corners[CB_INNER_H_CORNERS][0][1]- corners[0][0][1])
        w =abs(corners[CB_INNER_H_CORNERS][0][0]- corners[corners.shape[0]-1][0][1])

        # compute W value 
        HComputed =z * h/FOCAL_LENGHT 
        WComputed =z * w/FOCAL_LENGHT 
    
        # compare W value with real w of the chessboard
        Hdiff = abs(HComputed- H)
        Wdiff = abs(WComputed- W)

        # print differences
        print("The difference from the computed H and the real H is {}".format(Hdiff))
        print("The difference from the computed W and the real W is {}".format(Wdiff))

# SHOW VIDEO FRAMES IN GRAYSCALE
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
        if cv.waitKey(1) == ord('q'):
            break
     
    LCameraView.release()
    RCameraView.release()

def computeDisparityMap(imgL,imgR,frameShape,numDisparities,blockSize):

    # Calculate center frame
    center = frameShape
    centerY = int(center[0]/2)
    centerX = int(center[1]/2)
    interval = 100
    
    imgLCutted = imgL[centerY-interval:centerY+interval, centerX-interval:centerX+interval]
    imgRCutted = imgR[centerY-interval:centerY+interval, centerX-interval:centerX+interval]
            
    # Set Disparity map algotithm's parameters
    stereoMatcher = cv.StereoBM_create()
    stereoMatcher.setNumDisparities(numDisparities)
    stereoMatcher.setBlockSize(blockSize)
    
    # Disparity map computing
    disparity = stereoMatcher.compute(imgLCutted, imgRCutted)
            
    # main disparity computing
    dMain = np.absolute(disparity).mean()

    # depth computing
    z = (FOCAL_LENGHT * BASELINE)/dMain

    # printing disparity map
    imshow("disparity",'disparity with numDisparity {} and blockSize {}'.format(numDisparities,blockSize),disparity)

    # printing results
    print("main disparity value is {}".format(dMain))
    print("distance from the object is {} meters".format(z/1000))

    if (z/1000 < MINIMUM_DISTANCE):
        print("distance from the object under the minimum distance, detected distance: {} meters".format(z/1000))

    return z

def main(LCameraView,RCameraView,numDisparities,blockSize,chessboard):

    try:
        while LCameraView.isOpened() and RCameraView.isOpened():

            # Extract frames
            Lret, frameL = LCameraView.read()
            Rret, frameR = RCameraView.read()

            # Check for corrupted frames
            if not Lret or frameL is None or  not Rret or frameR is None:
                LCameraView.release()
                RCameraView.release()
                break
                
            # Get image frames
            imgL = cv.cvtColor(frameL, cv.COLOR_BGR2GRAY)
            imgR = cv.cvtColor(frameR, cv.COLOR_BGR2GRAY)

            z=computeDisparityMap(imgL,imgR,frameL.shape,numDisparities,blockSize)

            if chessboard: 
                computeChessboard(imgL,z)



    except KeyboardInterrupt:
        LCameraView.release()
        RCameraView.release()
        print("Released Video Resource")


# LOAD VIDEOS
LCameraView= cv.VideoCapture('robotL.avi')
RCameraView= cv.VideoCapture('robotR.avi')

# READ PARAMS
args =getParams()

# MAIN COMPUTATION
main(LCameraView,RCameraView,args.numDisparities,args.blockSize,args.chessboard)

