import numpy as np
import cv2

def grayscale(img):   
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def gaussian_blur(img, kernel_size):    
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def ycbcr(img): 
    return cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

def in_range(yc, lo, hi):
    return cv2.inRange(yc,lo,hi)

def erode(img, kern = None, iters=2):
    return cv2.erode(img, kernel=kern, iterations=iters)

def dilate(img, kern = None, iters = 1):
    return cv2.dilate(img, kernel=kern, iterations=iters)

def find_countours(thresholded):
    image, countours, hierarchies = cv2.findContours(thresholded, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return countours

def get_polygon(cont, ratio = 18):
    return cv2.approxPolyDP(cont, ratio, True)

def get_bound_box(cont):
    return cv2.minAreaRect(cont) #center (x,y), (width, height), angle of rotation

def hull(contour, retPts=True):
    hull = cv2.convexHull(contour, returnPoints = retPts)
    return hull

def defects(contour, hull):
    if hull is not None and len(hull > 3) and len(contour) > 3:
        defects = cv2.convexityDefects(contour, hull)
        return defects
    return None