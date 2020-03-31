import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os
from moviepy.editor import VideoFileClip
from IPython.display import HTML

from processimage import LaneDetection

ld = LaneDetection()
videolist = os.listdir("test_videos/")

for videoname in videolist:
    outputdir = "test_videos_output/" + videoname
    clip = VideoFileClip("test_videos/" + videoname)
    clip_processed = clip.fl_image(ld.process_image)
    %time clip_processed.write_videofile(outputdir, audio=False)