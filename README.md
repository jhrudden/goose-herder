# goose-herder

## References

-   Relied heavily on [DJITellopy's pygame example]("https://www.youtube.com/watch?v=muTznEnt9oMhttps://github.com/damiafuentes/DJITelloPy/blob/master/examples/manual-control-pygame.py") for creating environment for controlling tello drone via PC and viewing live stream from drone.
-   Used OpenCV's [camera calibration guide]("https://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html") to accurately calculate distance from camera to targets.

### Notice

If recieving `imu` errors, then cameras aren't getting enough light

### Distance Calculation

Focal length of camera ~= 3 mm

Use pinhole camera model for determining distance: https://en.wikipedia.org/wiki/Pinhole_camera_model
