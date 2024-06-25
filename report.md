# STEREO ROBOT NAVIGATION REPORT

## PROJECT ANALYSIS

From the requirements the project consists in creating a system capable of sensing distance given a stereo image in input from a video source (ideally a robot camera stream) exploiting the stereo matching principle.
The system needs to implement the following functionalities:

- trigger an allarm when the distance sensed is lower than a thrashold ( 0.8 meters from requirements)
- compute the dimensions of the chessboard in the video and compare them with the real one

## IMPLEMENTATION

The project implements the stereo matching algorithm through OpenCV library's stereoBM class which implements the block matching algorithm.
The project is organized in files python and a python script with some command line parameters, (run python project.py --help for more informations).

The algorithm implematation is done, as we said, through OpenCV's stereoBM class. 

We take the frames using the function VideoCapture() from OpenCV and check them (as corrupted frames can occur) and then we proceed to compute the disparity, using the function computeDisparityMap that take two stereo images and compute the disparity map between them using stereoMatcher.compute(imgL, imgR) with stereoMatcher = cv.StereoBM_create().

We cut the image to a central portion of the image of size $100x100$ to make it easier to calculate the distance.

Then we take the mean values of the disparity saved in dMain and the distance from the chessboard in each frames saved in z, and set an alarm that will be triggered just when the value of the distance obtained is shorter then the threshold.

Lastly we compute the chessboard, finding the corners with the function cv.findChessboardCorners() and calculating the parameters so that we can compare the chessboard parameters obtained with the real ones, and print a graph of the difference between the values.

The projects output on the STDOUT is a row with comma separated elements in the following format

```
dMain,z,z in meters, alarm, Hdiff,Wdiff 
```
Where:
- alarm is a boolean true only when the distance is lower than 0.8 meters
- dMain is the mean of the disparity of the central box of the image without considering the points 
Where Hdiff and Wdiff are optional parameter that can be enabled by passing the `-c` parameter.

## RESULTS

The output we obtain is the following:

![](final_statistics.png)

so we notice a difference in the quality of the aspected width and the real one, that decrease the second time the drone gets near the chessboard.
One hypothesis could be that, given the second time the drone approaches the chessboard it is not exactly centered but approaches with a trajectory more shifted to the side, we believe thsat this change in viewing angle could influence the detection of the corners, and knowing that lens distortions are usually more pronounced at the edges of the field of view, with part of the chessboard being closer to the edge, there could be a distortion effect that reduce the precision of the calculations.
