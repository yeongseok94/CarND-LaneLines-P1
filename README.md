# **Report: Finding Lane Lines on the Road** 

Also uploaded on GitHub Repository: https://github.com/yeongseok94/CarND-LaneLines-P1.git

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report

---

## Code Description

* "helperfunction.py": Copied version on helper functions described in P1.ipynb. Not used in running of the code.
* "lanedetection_test.py": Test code used for detailed test.
* "lanedetection_video.py": Main code for lane detection on the test videos.
* "processimage.py": Necessary classes and functions for lane detection. Especially, "LaneDetection.process_image()" shows the overall pipeline.

## Reflection on Work

### 1. Pipeline Description

Overall pipline can be easily found in "LaneDetection.process_image()".

**Step 1. Grayscale Image**

First, I grayscaled the image for further processing. Here, I used openCV "cvtColor" function.

**Step 2. Obtain Gaussian Blurred Image**

Next, I removed noises with Gaussian filter of kernel size 5. Here, I used openCV "GaussianBlur" function.

**Step 3. Obtain Edges with Canny Transform**

Next, I obtained edges with Canny transform. Here, I used openCV "Canny" function.
The low and high thresholds are set as 50 and 150.

### 2. Potential Shortcomings

One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggestion on Improvements

A possible improvement would be to ...

Another potential improvement could be to ...
