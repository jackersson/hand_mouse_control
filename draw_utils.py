import cv2
import numpy as np

#draws contours in image
def draw_contours(image, box):
    cv2.drawContours(image,[box],0,(100,0,255),2)

#plot hull points in contour 
def plot_hulls(image, hulls, color=(255, 0,0)):
    for hpt in hulls:
        pt = hpt[0]
        cv2.circle(frame, (pt[0], pt[1]), 5, color, -1)

#plot centroid point of contour
def plot_center(frame, center, color=(0, 255, 0)):
    cv2.circle(frame, center, 5, color, -1)
        
#plot start, middle, end point of defect and connect it with lines    
def plot_defects(frame, defects, contour, color=(0, 255, 0)):
    if defects is not None and len(defects) > 0:
        for i in range(len(defects)):
            s,e,f,d = defects[i,0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])    
            cv2.line(frame, start, far,(255,255,255),1)
            cv2.line(frame, far, end,(255,255,255),1)
            
            cv2.circle(frame, start, 2, color, -1)
            cv2.circle(frame, end, 2, color, -1)
            cv2.circle(frame, far, 2, (255, 0, 255), -1)
            
#plot fingers like plot defects           
def plot_fingers(frame, fingers, contour, color=(0, 255, 0)):
    if fingers is not None and len(fingers) > 0:
        for i in range(len(fingers)):
            s,e,f = fingers[i]
            
            far = tuple(contour[f][0])              
            if (s != -1 ):
                start = tuple(contour[s][0])
                cv2.line(frame, start, far,(255,255,0),1)
                cv2.circle(frame, start, 2, (0, 0, 255), -1)                
            
            if (e != -1 ):
                end = tuple(contour[e][0])
                cv2.line(frame, far, end,(255,255,0),1)
                cv2.circle(frame, end, 2, (255,0,0), -1)                
            
            cv2.circle(frame, far, 2, (0, 255, 0), -1)