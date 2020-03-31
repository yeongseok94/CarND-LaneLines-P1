### importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os

class LaneDetection:
    def __init__(self):
        ### Gaussian smoothing
        self.kernel_size = 5
        
        ### Canny transform
        self.low_threshold = 50
        self.high_threshold = 150
        
        ### mask onto cannyimage
        self.vertice_coeff = [[0.1,0.9],[0.49,0.59],[0.51,0.59],[0.9,0.9]]
        
        self.rho = 1            # distance resolution in pixels of the Hough grid
        self.theta = np.pi/180  # angular resolution in radians of the Hough grid
        self.threshold = 1      # minimum number of votes (intersections in Hough grid cell)
        self.min_line_len = 40  # minimum number of pixels making up a line
        self.max_line_gap = 20  # maximum gap in pixels between connectable line segments
    
    def process_image(self, image):
        ### grayscale image
        grayimage = self.grayscale(image)
        
        ### Gaussian smoothing
        blurimage = self.gaussian_blur(grayimage)
        
        ### Canny transform
        cannyimage = self.canny(blurimage)
        
        ### mask onto cannyimage
        self.imshape = image.shape
        vertices = np.array([[(self.imshape[1]*0.1,self.imshape[0]*0.9),
                              (self.imshape[1]*0.49,self.imshape[0]*0.59),
                              (self.imshape[1]*0.51,self.imshape[0]*0.59),
                              (self.imshape[1]*0.9,self.imshape[0]*0.9)]],
                            dtype=np.int32)
        masked_cannyimage = self.region_of_interest(cannyimage, vertices)
        
        ### Hough transform
        self.line_candidate = self.Hough_transform(masked_cannyimage)
        
        ### Select lane lines
        self.lanelines = self.select_lane()
        
        ### Visualize lane lines
        line_image = self.draw_lines(image, self.lanelines)
        
        ### line image onto original image
        weighted_image = self.weighted_img(line_image, image)
        
        return weighted_image
    
    def grayscale(self, img):
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    def gaussian_blur(self, img):
        return cv2.GaussianBlur(img, (self.kernel_size, self.kernel_size), 0)
    
    def canny(self, img):
        return cv2.Canny(img, self.low_threshold, self.high_threshold)
    
    def region_of_interest(self, img, vertices):
        mask = np.zeros_like(img)   
        if len(img.shape) > 2:
            channel_count = img.shape[2]
            ignore_mask_color = (255,) * channel_count
        else:
            ignore_mask_color = 255
        cv2.fillPoly(mask, vertices, ignore_mask_color)
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image
    
    def weighted_img(self, img, initial_img, α=0.8, β=1, γ=0):
        return cv2.addWeighted(initial_img, α, img, β, γ)
    
    def Hough_transform(self, img):
        lines = cv2.HoughLinesP(img, self.rho, self.theta, self.threshold, np.array([]),
                                minLineLength=self.min_line_len, maxLineGap=self.max_line_gap)
        return lines
    
    def select_lane(self):
        y1s = self.line_candidate[:,0,0]
        x1s = self.line_candidate[:,0,1]
        y2s = self.line_candidate[:,0,2]
        x2s = self.line_candidate[:,0,3]
        thetas = np.arctan2(y2s-y1s, x2s-x1s)
        slopes = (y2s-y1s) / (x2s-x1s)
        ycross = y1s - slopes*x1s
        xcross = -ycross/slopes
        ycross_bottom = slopes*self.imshape[0] + ycross
        
        rightlineidx = slopes > 0
        leftlineidx = slopes < 0
        
        rightlineidx &= ycross_bottom > self.imshape[1]/2
        rightlineidx &= ycross_bottom < self.imshape[1]
        leftlineidx &= ycross_bottom > 0 
        leftlineidx &= ycross_bottom < self.imshape[1]/2
            
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
                                                      self.imshape[0],
                                                      rightline_slope*0.6*self.imshape[0] + rightline_ycross,
                                                      0.6*self.imshape[0]]]],
                                                   dtype=int)),
                                          axis=0)
        if any(leftlineidx):
            leftline_slope = np.average(slopes[leftlineidx])
            leftline_ycross = np.average(ycross[leftlineidx])
            leftline_ycross_bottom = np.average(ycross_bottom[leftlineidx])
            outputlines = np.concatenate((outputlines,
                                          np.array([[[leftline_ycross_bottom,
                                                      self.imshape[0],
                                                      leftline_slope*0.6*self.imshape[0] + leftline_ycross,
                                                      0.6*self.imshape[0]]]],
                                                   dtype=int)),
                                          axis=0)
        
        return outputlines
        
    def draw_lines(self, image, lines, color=(255, 0, 0), thickness=5):
        line_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(image, (x1, y1), (x2, y2), color, thickness)
                
        return line_image