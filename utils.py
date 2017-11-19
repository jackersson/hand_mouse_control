import cv2
import numpy as np
import math
from imageproc import *

def vector(a, b): #creates vector from two points
    return [a[0] - b[0], a[1] - b[1]]

def distance(vec): #measures magnitude of vector
    return (vec[0]**2 + vec[1]**2)**0.5

def distanceP2P(a, b): #measures distance between two points
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def dot(a, b): #element wise multiplication with sum of two vectors
    return a[0] * b[0] + a[1] * b[1]

def get_angle(start, far, end): #getting angle between three points
    
    a = vector(far, start)
    b = vector(far, end  )
    ab = dot(a, b)
    dist_ab = distance(a) * distance(b) 
    
    calc = min(max((ab / dist_ab), -1.0), 1.0)   
    
    angle = math.acos(calc) * 180 / math.pi
    return angle

def get_max_countour(thresholded):    
    countours = find_countours(thresholded)
    
    count = len(countours)
    if count <= 0:
        return None
    
    max_area = 100    
    max_index = -1
    for i in range(count):
        countour = countours[i]
        area = cv2.contourArea(countour)
        if ( max_area < area):
            max_area = area
            max_index = i
            
    if max_index == -1:
        return None
                
    return countours[max_index]

def centroid(contour):
    moments = cv2.moments(contour)
    if moments['m00'] != 0:
        cx = int(moments['m10']/moments['m00'])
        cy = int(moments['m01']/moments['m00'])
        return (cx,cy)
    else:
        return None