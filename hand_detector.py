import cv2
import numpy as np

from utils import *
from hand_utils import *
from imageproc import *
from draw_utils import *

class HandDetector:    
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.polygon = None #approx. polygon that fits entire contour
        self.hand_contour = None #full contour points
        self.hulls = None #peak points of contour
        self.defect = None
        self.fingers = None
        self.far_finger = None #the far finger point
        self.fingers_count = None
        self.center = None
          
        
    def detect(self, colored_mask):
        self.reset()
        
        gray = grayscale(colored_mask)
        ret, thresholded = cv2.threshold(gray, 0, 255, 0)
        
        
        max_contour = get_max_countour(thresholded)
        
        self.hand_contour = max_contour
        if self.hand_contour is None:
            return None
        
        bounding_rect = get_bound_box(max_contour)
        self.hulls   = hull(max_contour) # returns index in contour and point itself
        hulls_no_pts = hull(max_contour, False) #returns only index in contour    
        
        self.polygon  = get_polygon(self.hulls, 10)
        self.center = centroid(max_contour) 
        self.defect = defects(max_contour, hulls_no_pts) 

        #try to find possible finger points
        fingers = eliminate_defects(bounding_rect, self.defect, max_contour)
        
        #check if finger only one
        check_one_finger(fingers, max_contour, bounding_rect, hulls_no_pts, self.center  )
        
        #remove redundant fingers
        if fingers is not None and len(fingers) > 0:
            self.fingers, self.far_finger, self.fingers_count = get_target_fingers(fingers,max_contour, bounding_rect )
        
    def plot(self, frame):
        if self.hand_contour is not None: 
            #draw_contours(frame, self.hand_contour)
            #plot_hulls(frame, self.hulls)
            #plot_center(frame, self.center)            
            plot_fingers(frame, self.fingers, self.hand_contour, (0,0,255))
            #plot_defects(frame, self.defect, self.hand_contour, (0, 255, 0))