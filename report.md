# STEREO ROBOT NAVIGATION REPORT

## PROJECT ANALYSIS

From the requirements the project consists in creating a system capable of sensing distance given a stereo image in input from a video source (ideally a robot camera stream) exploiting the stereo matching principle.
The system needs to implement the following functionalities:

- trigger an allarm when the distance sensed is lower than a thrashold ( 0.8 meters from requirements)
- compute the dimensions of the chessboard in the video and compare them with the real one

## IMPLEMENTATION

The project implements the stereo matching algorithm through OpenCV library's stereoBM class which implements the block matching algorithm.
The project is organized in files python and a python script with some command line parameters, (run python project.py --help for more informations).

The algorithm implematation is done as we said through OpenCV's stereoBM class. 

We take the frames and check them (as corrupted frames can occur) and then we proceed to compute the disparity.

We cut the image to a central portion of the image of size $100x100$ to make it easier to calculate the distance.

So we take the mean values of the disparity and the distance from the chessboard in each frames, and set an alarm that will be triggered just when the value of the distance obtained is shorter then the threshold.

Lastly we compare the chessboard parameters obtained with the real ones, and print a graph of the difference between the values.

The projects output on the STDOUT is a row with comma separated elements in the following format

```
dMain,z,z in meters, alarm, Hdiff,Wdiff 
```
Where:
- alarm is a boolean true only when the distance is lower that 0.8 meters
- dMain is the mean of the disparity of the central box of the image without considering the points 
Where Hdiff and Wdiff are optional parameter that can be enabled by passing the `-c` parameter.

## RESULTS

The output we obtain is the following:

![Alt text](<Output bellino.png>)

so we notice a difference in the quality of the aspected width and the real one, that decrease the second time the drone gets near the chessboard.
