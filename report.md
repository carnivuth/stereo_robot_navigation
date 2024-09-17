# STEREO ROBOT NAVIGATION REPORT

## PROJECT ANALYSIS

The project consists in creating a system capable of sensing distance given a stereo image input from a video source (ideally a robot camera stream) exploiting the stereo matching principle.

The system needs to implement the following functionalities:

- trigger an alarm when the distance sensed is lower than a threshold ( 0.8 meters from requirements)
- compute the dimensions of the chessboard in the video and compare them with the real one

## IMPLEMENTATION

The system computes the disparity map for each frame and cuts it to a central portion of $100 \times 100$ pixels, to improve computation of distance the mean value of the disparity is taken as common reference for all the point in the window.

Than the computation of distance is performed, and the system signals if distance is lower than the threshold value.

In the last phase chessboard corners and dimensions differences are computed and stored in a dataframe for post execution evaluation.

The projects behaves like a line filter on the `STDOUT` , for each frame computed it prints a row with comma separated elements in the following format:

```
dMain,z,z in meters, alarm, Hdiff,Wdiff
```

Where:
- `alarm` is a boolean true only when the distance is lower than 0.8 meters
- `dMain` is the mean of the disparity of the central box of the image
- `z` is the computed distance
- `Hdiff` and `Wdiff` are the computed differences between the real dimensions of the chessboard and the real value

### SEARCH FOR THE BEST PARAMETERS

In order to look for the best set of parameters the team decided to adopt a brute force approach by testing the script running with different parameters and evaluating the results afterwards.

## RESULTS

After parameter tuning the system shows the following results:

![](final_statistics.png)

The system shows a decrease of performance in the second phase (*near the frame 300*) where the drone is nearest to the camera, one possible explanation can be found in the fact that in this phase, the drone camera is not perfectly parallel to the plane of the chessboard, this could cause some errors in the measurements due to the fact that the formulas used to compute it:

$$
W = \frac{z\ast w}{f}
$$

$$
H = \frac{z\ast h}{f}
$$
Relies on the assumption of the plane being perfectly parallel
