import cv2 as cv
import constants
from utils import imshow

# FIND CHESBOARD IN THE IMAGE
def computeChessboard(imgL,z):
    ret,corners = cv.findChessboardCorners(imgL ,(constants.CB_INNER_H_CORNERS,constants.CB_INNER_W_CORNERS))

    if ret == True:

        # draw chessboard corners in the left image
        cv.drawChessboardCorners(imgL, (constants.CB_INNER_H_CORNERS,constants.CB_INNER_W_CORNERS), corners, ret)

        imshow("chessboard",'chessboard',imgL)

        # get w value WRONG VALUES
        h =abs(corners[constants.CB_INNER_H_CORNERS-1][0][1]- corners[0][0][1])
        w =abs(corners[constants.CB_INNER_H_CORNERS-1][0][0]- corners[corners.shape[0]-1][0][0])

        # compute W value 
        HComputed =z * h/constants.FOCAL_LENGHT 
        WComputed =z * w/constants.FOCAL_LENGHT 
    
        # compare W value with real w of the chessboard
        Hdiff = abs(HComputed- constants.H)
        Wdiff = abs(WComputed- constants.W)

        # print differences
        return Hdiff, Wdiff

    else:
        return -100,-100
