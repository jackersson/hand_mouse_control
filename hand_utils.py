import cv2
import numpy as np
from utils import *

#detect possible fingers from defects
def eliminate_defects( bounding_box, defects, contour ):  
    x,y = bounding_box[0]
    w,h = bounding_box[1]
    
    tolerance = h / 4
    angle_to = 110
    new_defects = []
    
    if defects is None or contour is None:
        return new_defects
    
    for i in range(len(defects)):
        s,e,f,d = defects[i,0]
        start = tuple(contour[s][0])
        end   = tuple(contour[e][0])
        far   = tuple(contour[f][0]) 
        
        if distanceP2P(start, far) > tolerance and distanceP2P(end, far) > tolerance:
            current_angle = get_angle(start, far, end)
            if current_angle < angle_to and current_angle > 30:
                condition = y + h / 4
                if (end[1] >  condition):
                    continue
                elif (start[1] >  condition):
                    continue
                else:
                    new_defects.append([s, e, f])
                    
    remove_redundant(new_defects, contour, bounding_box )    
    return new_defects

def get_far_finger(fingers, contour):    
    far = None
    is_start = False
    max_y = 10**5
    if fingers is not None and len(fingers) > 0:
        for i in range(len(fingers)):
            s,e,f = fingers[i]            
            fr = tuple(contour[f][0]) 
            if (fr[1] < max_y): 
                max_y = fr[1]
                far = fingers[i]                   
            
            if (e != -1 ):
                end = tuple(contour[e][0])       
                if (end[1] <= max_y):  
                    max_y = end[1]
                    far = fingers[i]
                    is_start = True
    return far, is_start

#remove redundant fingers for gesture recognition
def get_target_fingers(fingers, contour, bound_rect):  

    fingers_count = 0
     
    if fingers is None or (len(fingers) <= 0):
        return None, None, fingers_count
    
    new_fingers = []
    far_finger_pt = None
    far, is_start = get_far_finger(fingers,contour )

    
    if far == None or len(far) < 3:
        return new_fingers, far_finger_pt, fingers_count
    
    w,h = bound_rect[1]
    tolerance=h/5
    
    s,e,f = far
    if s == -1:
        new_fingers.append(far)
        far_finger_pt = tuple(contour[f][0])
        fingers_count = 1
    else:
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])     
        if end[1] < start[1] and abs(start[1] - end[1]) > tolerance:
            new_fingers.append(far)
            far_finger_pt = end
            fingers_count = 2    
    return new_fingers, far_finger_pt, fingers_count  

def remove_redundant(new_defects, contour, bound_rect):
    w,h = bound_rect[1]
    tolerance=w/4
    for i in range(len(new_defects)):
        
        s1,e1,f = new_defects[i]
        start1 = tuple(contour[s1][0])
        end1   = tuple(contour[e1][0])
        
        for j in range(len(new_defects)):   
            
            s2,e2,f = new_defects[j]
            start2 = tuple(contour[s2][0])
            end2   = tuple(contour[e2][0])
            
            if distanceP2P(start1, end2) < tolerance:
                contour[s1][0] = end2
                break
            if distanceP2P(end1, start2) < tolerance:
                contour[s2][0] = end1
            
def check_one_finger(fingers, contour, bounding_rect, hulls, center):
    x,y = bounding_rect[0]
    w,h = bounding_rect[1]
    
    max_finger_height = h / 1.65
    possible_finger_point = [0, y + w / 2 ]
    index =  0
    for hl in hulls:
        cur_point = contour[hl[0]][0]
        if cur_point[1] < possible_finger_point[1]:
            possible_finger_point = cur_point
            index = hl[0]
            
    tolerance = h / 6
    n = 0
    for hl in hulls:
        cur_point = contour[hl[0]][0]
        if cur_point[1] < (possible_finger_point[1] + tolerance) and cur_point[1] != possible_finger_point[1] :
            if cur_point[1] < y and cur_point[0] != possible_finger_point[0]:
                if distanceP2P(possible_finger_point, cur_point) > tolerance:
                    n += 1
                    
    if n < 2 and len(fingers) == 0:
        fingers.append([-1, -1, index])               