import argparse
import cv2 as cv
from utils import imshow

# chessboard dimensions (in millimeters)
H = 178
W = 125

# best blocksize value 
BEST_BLOCKSIZE_VALUE=33
# chessboard parameters
CB_INNER_W_CORNERS = 6
CB_INNER_H_CORNERS = 8

# allarm trigger limit (in meters)
MINIMUM_DISTANCE =  0.8

# camera parameters
FOCAL_LENGHT =  567.2 
BASELINE = 92.226 


# GET ARGUMENTS
def getParams():
    parser = argparse.ArgumentParser(prog='CVproject',description='computer vision project',epilog='credits carnivuth')
    parser.add_argument('-i','--imageDim',default='100',help='image box dimension to cut from original frames for disparity computation',type=int)
    parser.add_argument('-d','--numDisparities',default='128',help='numDisparities parameter for disparity map algorithm',type=int)
    parser.add_argument('-b','--blockSize',default=BEST_BLOCKSIZE_VALUE,help='blocksize parameter for disparity map algorithm', type=int)
    parser.add_argument('-c','--chessboard',help='Compute chessboard recognition',action='store_true')
    parser.add_argument('-s','--cornerWinSize',help='corner win size parameter',type=int)
    return parser.parse_args()

# FIND CHESBOARD IN THE IMAGE
def computeChessboard(imgL,z,cornerWinSize):
    ret,corners = cv.findChessboardCorners(imgL ,(CB_INNER_H_CORNERS,CB_INNER_W_CORNERS))

    if ret == True:

        criteria = (cv.TERM_CRITERIA_EPS + cv.TermCriteria_COUNT, 40, 0.001)
        corners = cv.cornerSubPix( imgL, corners,(cornerWinSize,cornerWinSize) ,(-1,-1),criteria)
        # draw chessboard corners in the left image
        cv.drawChessboardCorners(imgL, (CB_INNER_H_CORNERS,CB_INNER_W_CORNERS), corners, ret)
        imshow("chessboard",'chessboard',imgL)

        # get w value WRONG VALUES
        h =abs(corners[CB_INNER_H_CORNERS-1][0][1]- corners[0][0][1])
        w =abs(corners[CB_INNER_H_CORNERS-1][0][0]- corners[corners.shape[0]-1][0][0])

        # compute W value 
        HComputed =z * h/FOCAL_LENGHT 
        WComputed =z * w/FOCAL_LENGHT 
    
        # compare W value with real w of the chessboard
        Hdiff = abs(HComputed- H)
        Wdiff = abs(WComputed- W)

        # print differences
        return Hdiff, Wdiff
        #print("The difference from the computed H and the real H is {}".format(Hdiff))
        #print("The difference from the computed W and the real W is {}".format(Wdiff))
    else:
        return -100,-100

def computeDisparityMap(imgL,imgR,frameShape,numDisparities,blockSize,interval):
            
    # Set Disparity map algotithm's parameters
    stereoMatcher = cv.StereoSGBM_create()
    stereoMatcher.setNumDisparities(numDisparities)
    stereoMatcher.setBlockSize(blockSize)
    
    # Disparity map computing
    disparity = stereoMatcher.compute(imgL, imgR)

    # Calculate center frame
    center = frameShape
    centerY = int(center[0]/2)
    centerX = int(center[1]/2)
    halfsize = int(interval/2)
    
    # cut disparity to the center frame
    disparity = disparity[centerY-halfsize:centerY+halfsize, centerX-halfsize:centerX+halfsize]
            
    # main disparity computing excluding negative values where disparity could not be computed
    dMain = (disparity[disparity >= 0]/16).mean()

    # depth computing
    z = (FOCAL_LENGHT * BASELINE)/dMain

    # printing disparity map
    imshow("disparity",'numDisparity {}, blockSize {}'.format(numDisparities,blockSize),disparity)

    return z,dMain

def main(LCameraView,RCameraView,numDisparities,blockSize,chessboard,interval,cornerWinSize):

    
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

            z,dMain=computeDisparityMap(imgL,imgR,frameL.shape,numDisparities,blockSize,interval)

            if (z/1000 < MINIMUM_DISTANCE):
               alarm=1 
            else:
               alarm=0 
               
            if chessboard: 
                Hdiff,Wdiff = computeChessboard(imgL,z,cornerWinSize)
                print("{},{},{},{},{},{}".format(dMain,z,z/1000,alarm,Hdiff,Wdiff))
            else:
                print("{},{},{},{}".format(dMain,z,z/1000,alarm))

    except KeyboardInterrupt:
        LCameraView.release()
        RCameraView.release()
        print("Released Video Resource")

# READ PARAMS
args =getParams()

# LOAD VIDEOS
LCameraView= cv.VideoCapture('robotL.avi')
RCameraView= cv.VideoCapture('robotR.avi')

# MAIN COMPUTATION
main(LCameraView,RCameraView,args.numDisparities,args.blockSize,args.chessboard,args.imageDim,args.cornerWinSize)

