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

**Step 4. Mask onto Canny Transformed Image**

Next, I masked the possible lane region onto Canny transformed image. Here, I used openCV "fillPoly" function.
The region of interest is trapezoidal area that covers about lower quarter of the image slightly above from the bottom of the image.
Note that the bottom of the region is not equal to the bottom of the image in order to reject fron area of the car.
Vertices of the trapezoidal area are defined as relative value proportional to image size.

**Step 5. Line Candidates by Hough Transform**

Next, I obtained line candidates by Hough transform. Here, I used openCV "HoughLinesP" function.
I selected distance resolution as 1px, angular resolution as 1deg, minimum number of votes as 1, minimum line length as 40px, and maximum line gap as 20px.

**Step 6. Selection of Left and Right Lines of the Lane**

Final procedure includes deciding the lane lines with obtained line candidates.

First, I categorized the line candidates into left line candidates and right line candidates with slopes of the lines.
Right line candidates should have positive slope values,
and left line candidates should have negative slope values.

Next, I narrowed down each line candidates by checking where on the bottom of the image the extrapolated line segments go through.
Proper right line candidates should go through right half of the bottom of the image,
and left line candidates should go through left half of the bottom of the image.

Next, I again narrowed down each line candidates by checking whether the slope of the line is inside ±5deg with respect to the median value among them.
Here I simply selected median value as a priori estimate of the slope, but it can be some other value.
This procedure is to reject unexpected line expectation.

Finally, I selected one single right lane line and left lane line by averaging the line parameters of the line candidates and visualized it on the image.


### 2. Potential Shortcomings

One potential shortcoming would be what would happen when ... 

Another shortcoming could be ...


### 3. Suggestion on Improvements

A possible improvement would be to ...

Another potential improvement could be to ...
