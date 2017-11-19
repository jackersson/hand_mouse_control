import cv2
import numpy as np
import time
import pyautogui

class HandMouseControl:
    
    def __init__(self, frame_size):
        self.fingers = None
        
        #blind zones initialization (could be changed)
        self.offset_x, self.offset_y = 120, 180
        self.offset_w, self.offset_h = 150, 10

        self.is_mouse_down = False

        #delay between clicks
        self.clicks_delay = 1 #1 second

        #initialize start time
        self.left_click_time  = time.clock()
        self.right_click_time = time.clock()
        
        #set the correspondence between image -> screen coordinates
        self.set_ratio(frame_size)
    
    def set_ratio(self, frame_size):
        self.screen_w,  self.screen_h = pyautogui.size() 
        self.frame_h, self.frame_w   = frame_size

        self.zone_width = (self.frame_w - self.offset_x - self.offset_w ) 
        self.zone_height= (self.frame_h - self.offset_y - self.offset_h) 

        self.ratio_x = float(float(self.screen_w) / self.zone_width )
        self.ratio_y = float(float(self.screen_h) / self.zone_height )      

    def get_screen_coordinates(self, far_finger):
        delta_x = far_finger[0] - self.offset_x
        if delta_x < 0:
            delta_x = 1
        elif delta_x > (self.frame_w - self.offset_w - self.offset_x):
            delta_x = (self.frame_w - self.offset_w - self.offset_x)
                   
        delta_y = far_finger[1] - self.offset_h
        if delta_y < 0:
            delta_y = 1
        if delta_y > (self.frame_h - self.offset_y - self.offset_h ):
            delta_y = self.frame_h - self.offset_y - self.offset_h  
          
        new_x = max(delta_x * self.ratio_x, 1)
        new_y = max(delta_y * self.ratio_y, 1) 
        
        return new_x, new_y
    
    def mouse_down(self, x, y, change_pos = True):
        if self.is_mouse_down:
            return
        if not change_pos:
            x, y = pyautogui.position()
        pyautogui.mouseDown(x, y, button='left')
        self.is_mouse_down = True
        
    def mouse_up(self, x, y, change_pos = True):
        if not self.is_mouse_down:
            return
        
        if not change_pos:
            x, y = pyautogui.position()
        pyautogui.mouseUp(x, y, button='left')
        
        self.is_mouse_down = False
        
    def mouse_move(self, x, y):
        pyautogui.moveTo(x, y, duration=0.01)
        
        
    def action(self, far_finger, fingers_count, do_action=True):  
        if do_action == False:
            self.mouse_up(0, 0, False)
            return

        if fingers_count is None:
            self.mouse_up(0, 0, False)
            return 
        
        if fingers_count >= 2: #big and pointer fingers we can move mouse 
            self.mouse_up(0, 0, False)                                  
            if far_finger is not None:                
                new_x, new_y = self.get_screen_coordinates(far_finger)   
                self.mouse_move(new_x, new_y)
        #only pointer finger present    
        elif fingers_count == 1 and time.clock() - self.left_click_time > self.clicks_delay:
           if far_finger is not None :                
                new_x, new_y = self.get_screen_coordinates(far_finger) 
                if not self.is_mouse_down:
                    self.mouse_down(0, 0, False )
                else:
                    self.mouse_move(new_x, new_y )           
        #closed wrist
        elif fingers_count < 1 and time.clock() - self.right_click_time > self.clicks_delay:
            self.mouse_up(0, 0, False)
            pyautogui.click(button='right')
            self.right_click_time = time.clock()
            

    #draw blind zones with green color
    def draw_offsets(self, frame):
        green_multiplier = 15
        offset = 100
        h,w = frame.shape[:2]
        frame[0:h-self.offset_y, 0:self.offset_x, 1] += green_multiplier
        frame[0:h-self.offset_y, w - self.offset_w:w, 1] += green_multiplier

        frame[h-self.offset_y:h, :, 1] += green_multiplier
        frame[0:self.offset_h, self.offset_x:w - self.offset_w, 1] += green_multiplier