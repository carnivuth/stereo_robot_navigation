# STEREO ROBOT NAVIGATION REPORT

## INTRODUCTION

The projects involves the implementation of a stereo matching algorithm capable of create a disparity map for the distance computation of objects in front of the robot.

## IMPLEMENTATION

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

