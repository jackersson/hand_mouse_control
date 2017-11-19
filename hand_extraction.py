import cv2
import numpy as np
import math

from utils import *

class HandExtraction:
    def __init__(self):
        self.trained_hand = False
        self.hand_row_nw = None
        self.hand_row_se = None
        self.hand_col_nw = None
        self.hand_col_se = None
        self.hand_hist = None
        
    def draw_hand_rect(self, frame):  
        rows,cols = frame.shape[:2]
        dels = 20
        #change distance between rects
        self.hand_row_nw = np.array([6*rows/dels,6*rows/dels,6*rows/dels,
                                     9*rows/dels,9*rows/dels,9*rows/dels,
                                     12*rows/dels,12*rows/dels,12*rows/dels], dtype=np.int16)

        self.hand_col_nw = np.array([9*cols/dels,10*cols/dels,11*cols/dels,
                                     9*cols/dels,10*cols/dels,11*cols/dels,
                                     9*cols/dels,10*cols/dels,11*cols/dels], dtype=np.int16)

        self.hand_row_se = self.hand_row_nw + 50 #change height of rects
        self.hand_col_se = self.hand_col_nw + 30 #change width of rects
    
        size = self.hand_row_nw.size
        for i in range(size):
            cv2.rectangle(frame,(self.hand_col_nw[i],self.hand_row_nw[i]),(self.hand_col_se[i],self.hand_row_se[i]),(0,255,0),1)
        
        black = np.zeros(frame.shape, dtype=frame.dtype)
        frame_final = np.vstack([black, frame])
        return frame_final
    
    def train_hand(self, frame):
        self.trained_hand = True
        return self.set_hand_hist(frame)
        
    #calculate color range for hand extraction based on colors from rects
    def set_hand_hist(self, frame):  
        hsv = ycbcr(frame)
        roi = np.zeros([90,10,3], dtype=hsv.dtype)

        size = self.hand_row_nw.size
        for i in range(size):
            roi[i*10:i*10+10,0:10] = hsv[self.hand_row_nw[i]:self.hand_row_nw[i]+10, self.hand_col_nw[i]:self.hand_col_nw[i]+10]

	
        temp_lo = []
        temp_hi = []
        for i in range(0, 3):
            croped = roi[:, :, i].copy()
            blured = gaussian_blur(croped, 9).flatten()            
            temp_lo.append(min(blured))
            temp_hi.append(max(blured))   
        
        
        '''
        temp_lo = []
        temp_hi = []
        for i in range(0, 2):
            croped = roi[:, :, i].copy()
            blured = gaussian_blur(croped, 9).flatten()
            
            mul_min, mul_max = 1.0, 1.0
            #if (i == 1):
                #mul_min, mul_max = 0.95, 1.03
            
            temp_lo.append(int (min(blured) * mul_min))
            temp_hi.append(int (max(blured) * mul_max))
        #temp_lo.append(0)
        #temp_hi.append(255)
        '''  
        return np.array(temp_lo), np.array(temp_hi)
        
