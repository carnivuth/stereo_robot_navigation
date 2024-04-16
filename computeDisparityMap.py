import cv2 as cv
from utils import imshow
import constants

def computeDisparityMap(imgL,imgR,frameShape,numDisparities,blockSize,interval,cutted_frame):
   
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
    z = (constants.FOCAL_LENGHT * constants.BASELINE)/dMain

    # printing disparity map
    if cutted_frame:
        imshow("disparity",'numDisparity {}, blockSize {}'.format(numDisparities,blockSize),disparity)

    return z,dMain
