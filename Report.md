# **Report: Finding Lane Lines on the Road** 

Also uploaded on:

https://github.com/yeongseok94/CarND-LaneLines-P1.git

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report

---

## Code Description

* helperfunction.py: Copied version on helper functions described in P1.ipynb. Not used in running of the code.
* lanedetection_test.py: Test code used for detailed test.
* lanedetection_video.py: Main code for lane detection on the test videos.
* processimage.py: Necessary classes and functions for lane detection. Especially, 'process_image' shows the overall pipeline.

## Reflection on work

### 1. Pipeline description

My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I .... 

In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### 2. Potential shortcomings

One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggestion on improvements

A possible improvement would be to ...

Another potential improvement could be to ...
