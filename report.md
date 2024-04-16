# STEREO ROBOT NAVIGATION REPORT

## PROJECT ANALYSIS

From the requirements the project consists in creating a system capable of sensing distance given a stereo image input from a video source (ideally a robot camera stream) exploiting the stereo matching principle, The system needs to implement the following functionalities:

- trigger an allarm when the distance sensed is lower than a thrashold ( 0.8 meters from requirements)
- compute the dimensions of the chessboard in the video and compare them with the real one

## IMPLEMENTATION

The project implements the stereo matching algorithm through OpenCV library's stereoBM class which implements the block matching algorithm
The project is organized as a python script with some command line parameters, (run python project.py --help for more informations), it implements
The algorithm implematation is done trough OpenCV's stereoBM class, the image is cutted to a central portion of the image of size $100x100$  

The projects output on the STDOUT a row with comma separated elements in the following format

```
dMain,z,z in meters, alarm, Hdiff,Wdiff 
```
Where:
- alarm is a boolean true only when the distance is lower that 0.8 meters
- dMain is the mean of the disparity of the central box of the image without considering the points 
Where Hdiff and Wdiff are optional parameter that can be enabled by passing the `-c` parameter.

## RESULTS

