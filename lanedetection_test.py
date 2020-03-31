### importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os

### read in an image
imagelist = os.listdir("test_images/")
image = mpimg.imread("test_images/"+imagelist[5])
# plt.imshow(image)

### grayscale image
grayimage = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# plt.imshow(grayimage)

### Canny transform
low_threshold = 50
high_threshold = 150
cannyimage = cv2.Canny(grayimage, low_threshold, high_threshold)
# plt.imshow(cannyimage)

### mask onto cannyimage
mask = np.zeros_like(cannyimage)  
ignore_mask_color = 255   
imshape = image.shape
vertices = np.array([[(imshape[1]*0.1,imshape[0]*0.9),
                      (imshape[1]*0.49,imshape[0]*0.59),
                      (imshape[1]*0.51,imshape[0]*0.59),
                      (imshape[1]*0.9,imshape[0]*0.9)]],
                    dtype=np.int32)
cv2.fillPoly(mask, vertices, ignore_mask_color)
masked_cannyimage = cv2.bitwise_and(cannyimage, mask)
# plt.imshow(masked_cannyimage)

### Hough transform
rho = 1                # distance resolution in pixels of the Hough grid
theta = np.pi/180      # angular resolution in radians of the Hough grid
threshold = 1          # minimum number of votes (intersections in Hough grid cell)
min_line_len = 40      # minimum number of pixels making up a line
max_line_gap = 20      # maximum gap in pixels between connectable line segments
lines = cv2.HoughLinesP(masked_cannyimage, rho, theta, threshold, np.array([]),
                        minLineLength=min_line_len, maxLineGap=max_line_gap)
y1s = lines[:,0,0]
x1s = lines[:,0,1]
y2s = lines[:,0,2]
x2s = lines[:,0,3]

thetas = np.arctan2(y2s-y1s, x2s-x1s)
slopes = (y2s-y1s) / (x2s-x1s)
ycross = y1s - slopes*x1s
xcross = -ycross/slopes
ycross_bottom = slopes*imshape[0] + ycross

rightlineidx = slopes > 0
leftlineidx = slopes < 0

rightlineidx &= ycross_bottom > imshape[1]/2
rightlineidx &= ycross_bottom < imshape[1]
leftlineidx &= ycross_bottom > 0 
leftlineidx &= ycross_bottom < imshape[1]/2
    
right_theta_med = np.median(thetas[rightlineidx])
left_theta_med = np.median(thetas[leftlineidx])
rightlineidx &= thetas < right_theta_med + 5.0*np.pi/180.0
rightlineidx &= thetas > right_theta_med - 5.0*np.pi/180.0
leftlineidx &= thetas < left_theta_med + 5.0*np.pi/180.0
leftlineidx &= thetas > left_theta_med - 5.0*np.pi/180.0

outputlines = [[[0, 0, 0, 0]]]
if any(rightlineidx):
    rightline_slope = np.average(slopes[rightlineidx])
    rightline_ycross = np.average(ycross[rightlineidx])
    rightline_ycross_bottom = np.average(ycross_bottom[rightlineidx])
    outputlines = np.concatenate((outputlines,
                                  np.array([[[rightline_ycross_bottom,
                                              imshape[0],
                                              rightline_slope*0.6*imshape[0] + rightline_ycross,
                                              0.6*imshape[0]]]],
                                            dtype=int)),
                                  axis=0)
if any(leftlineidx):
    leftline_slope = np.average(slopes[leftlineidx])
    leftline_ycross = np.average(ycross[leftlineidx])
    leftline_ycross_bottom = np.average(ycross_bottom[leftlineidx])
    outputlines = np.concatenate((outputlines,
                                  np.array([[[leftline_ycross_bottom,
                                              imshape[0],
                                              leftline_slope*0.6*imshape[0] + leftline_ycross,
                                              0.6*imshape[0]]]],
                                            dtype=int)),
                                  axis=0)
    

line_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
for line in outputlines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
plt.imshow(line_image)

## line image onto original image
weighted_image = cv2.addWeighted(image, 0.8, line_image, 1, 0)
plt.imshow(weighted_image)