import argparse
import cv2 as cv
import matplotlib.pyplot as plt
 
# GET ARGUMENTS
def getParams():
    parser = argparse.ArgumentParser(prog='CVproject',description='computer vision project',epilog='credits carnivuth')
    parser.add_argument('-d','--numDisparities',default='16',help='numDisparities parameter for disparity map algorithm')
    parser.add_argument('-b','--blockSize',default='17',help='blocksize parameter for disparity map algorithm')
    return parser.parse_args()

# COMPUTE DISPARITY MAP
def computeDisparityMap(LCameraView,RCameraView,numDisparities,blockSize):

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
                
            # Calculate center frame
            center = frameL.shape
            centerY = int(center[0]/2)
            centerX = int(center[1]/2)
            interval = 50
            
            # Get image center box
            imgL = cv.cvtColor(frameL, cv.COLOR_BGR2GRAY)[centerY-interval:centerY+interval, centerX-interval:centerX+interval]
            imgR = cv.cvtColor(frameR, cv.COLOR_BGR2GRAY)[centerY-interval:centerY+interval, centerX-interval:centerX+interval]
            
            # Set Disparity map algotithm's parameters
            stereoMatcher = cv.StereoBM_create()
            stereoMatcher.setNumDisparities(numDisparities)
            stereoMatcher.setBlockSize(blockSize)
            
            # Disparity map computing
            disparity = stereoMatcher.compute(imgL, imgR)
            disparityImg = cv.normalize(disparity, disparity, alpha=255,beta=0, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)
            disparityImg = cv.applyColorMap(disparityImg, cv.COLORMAP_JET)
            
            plt.figure(1); plt.clf()
            plt.imshow(disparityImg)
            plt.title('disparity with numDisparity {} and blockSize {}'.format(numDisparities,blockSize))
            plt.pause(0.000001)

    except KeyboardInterrupt:
        LCameraView.release()
        RCameraView.release()
        print("Released Video Resource")

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
        #cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break
     
    LCameraView.release()
    RCameraView.release()
#    cv.destroyAllWindows()

# LOAD VIDEOS
LCameraView= cv.VideoCapture('robotL.avi')
RCameraView= cv.VideoCapture('robotR.avi')

# READ PARAMS
args =getParams()

# COMPUTE DISPARITY MAP
computeDisparityMap(LCameraView,RCameraView,int(args.numDisparities),int(args.blockSize))

