import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import pyautogui 

from hand_detector import *
from hand_extraction import *
from hand_utils import *
from hand_mouse_control import *
from imageproc import *
from utils import *

lo = np.array([12,129,75])
hi = np.array([255,150,150]) 

#main preprocessing image function
def preprocess_image(img, low, high):    
    #gaussian blur
    blured_img = gaussian_blur(img, 15)    
    
    #to ycrcb
    yc = ycbcr(blured_img)

    #threshold y cb cr        
    mask = in_range(yc,low,high)
  
    #make edges more clear
    for i in range(5):
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5)))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((9, 9)))
    
    max_contour = get_max_countour(mask)
    
    clean_mask = np.zeros((mask.shape), dtype=np.uint8)    
    if (max_contour is not None):        
        cv2.fillPoly(clean_mask,[max_contour], color=(255,255,255))       
 
    
    colored_mask = cv2.bitwise_and(img,img,mask=clean_mask) 
    return colored_mask

def release(camera):
    if camera is not None:
        camera.release()
        cv2.destroyAllWindows()

#parse camera index
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-c", required=True,
	help="camera index")

args = vars(ap.parse_args())

camera = cv2.VideoCapture(int(args['c']))
ret, frame = camera.read()

if ret == False:
    release(camera)
    
    
#parametrs for averaging frames
frame_sum = np.float32(frame)
count = 0
#make everithing smooth
frame_offset = 5 #change this to setup how many frames should be added

mouse_control = HandMouseControl(frame.shape[:2])
hand_extraction = HandExtraction()
detector = HandDetector()

need_to_extract = False
need_to_place_hand = True
on_mouse = False
show_offsets = False

try:
    while(True):
        # Capture frame-by-frame
        ret, frame = camera.read()
        if ret == False:
            continue
            
        frame = cv2.flip(frame,1)   #remove mirror efect mode
        
        if count < frame_offset:  #collecting frames
            cv2.accumulate(frame, frame_sum)
        else:
            count = 0
            frame_sum /= frame_offset
            average = cv2.convertScaleAbs(frame_sum)
            
            if need_to_extract:
                temp_lo, temp_hi = hand_extraction.train_hand(average)  
                lo[:], hi[:] = temp_lo[:], temp_hi[:]
                need_to_extract = False
            
            colored_hand_mask = preprocess_image(average, lo, hi)  
            
            if need_to_place_hand:
                cv2.imshow('Colored mask', colored_hand_mask)
                
            detector.detect(colored_hand_mask)          
            mouse_control.action(detector.far_finger, detector.fingers_count, on_mouse) # make action
            
        detector.plot(frame)    
        
        if show_offsets:
            mouse_control.draw_offsets(frame)
            
        if need_to_place_hand:        
            hand_extraction.draw_hand_rect(frame)
            
        cv2.imshow('Hand mouse control', frame)
        
        key = cv2.waitKey(1)
        
        if key & 0xFF == ord('w'):
            show_offsets = True if show_offsets == False else False        
        elif key & 0xFF == ord('a'):
            on_mouse = True if on_mouse == False else False        
        elif key & 0xFF == ord('h'):
            need_to_place_hand = True if need_to_place_hand == False else False        
        elif key & 0xFF == ord('s'):            
            need_to_extract = True               
        elif key & 0xFF == ord('q'):
            break
                
        count += 1
            
except KeyboardInterrupt:
    release(camera)
finally:
    release(camera)
release(camera)