import matplotlib.pyplot as plt
import argparse
import cv2 as cv
import pandas as pd
import constants
from computeDisparityMap import computeDisparityMap
from computeChessboard import computeChessboard

# GET ARGUMENTS
def getParams():
    parser = argparse.ArgumentParser(prog='CVproject',description='computer vision project',epilog='credits carnivuth')
    parser.add_argument('-i','--imageDim',default='100',help='image box dimension to cut from original frames for disparity computation',type=int)
    parser.add_argument('-d','--numDisparities',default='128',help='numDisparities parameter for disparity map algorithm',type=int)
    parser.add_argument('-b','--blockSize',default=constants.BEST_BLOCKSIZE_VALUE,help='blocksize parameter for disparity map algorithm', type=int)
    parser.add_argument('-c','--chessboard',help='Compute chessboard recognition',action='store_true')
    parser.add_argument('-p','--cutted_frame',help='print cutted window frame',action='store_true')
    return parser.parse_args()

def main(LCameraView,RCameraView,numDisparities,blockSize,chessboard,interval,cutted_frame):

    if chessboard:
        df = pd.DataFrame(columns = ['dMain','z in mm','Z in m','alarm','Hdiff','Wdiff'])
    else:
        df = pd.DataFrame(columns = ['dMain','z in mm','Z in m','alarm'])
    
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

            # disparity map computation
            z,dMain=computeDisparityMap(imgL,imgR,frameL.shape,numDisparities,blockSize,interval,cutted_frame)

            if (z/1000 < constants.MINIMUM_DISTANCE):
               alarm=1 
            else:
               alarm=0 
               
            # print output data, adding data to dataframe
            if chessboard: 
                Hdiff,Wdiff = computeChessboard(imgL,z)
                print("{},{},{},{},{},{}".format(dMain,z,z/1000,alarm,Hdiff,Wdiff))
                output = {
                        'dMain': dMain,
                        'z in mm': z,
                        'Z in m': z/1000,
                        'alarm': alarm,
                        'Hdiff': Hdiff,
                        'Wdiff': Wdiff
                        }
                df.loc[len(df)] = output
            else:
                print("{},{},{},{}".format(dMain,z,z/1000,alarm))
                output = {
                        'dMain': dMain,
                        'z in mm': z,
                        'Z in m': z/1000,
                        'alarm': alarm
                        }
                df.loc[len(df)] = output

        if chessboard:
            df= df[df['Hdiff'] != -100]
            df= df[df['Wdiff'] != -100]

        # plotting dataframe
        df.plot(subplots=True,)
        plt.tight_layout()
        plt.show()

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
main(LCameraView,RCameraView,args.numDisparities,args.blockSize,args.chessboard,args.imageDim,args.cutted_frame)


