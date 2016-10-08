'''
pre-processing.py
Author: Adam Swart
Pre-processing to normalise MCQ sheets
'''

import cv2
import os
import numpy as np
import cvutils
import math
from operator import itemgetter

'''
Finds the corners in an image
'''
def findCorners(img):
    img2 = img.copy()
    template = cv2.imread('images/templates/cnr_template.ppm', 0)
    w, h = template.shape[::-1]

    corners = []
    threshold = 0.7

    for i in range(4):
        # Apply template matching
        res = cv2.matchTemplate(img2,template,cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        #if max_val > threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1]+h)
        #cv2.rectangle(img2,top_left, bottom_right, (0,0,255), 2)
        centre = (top_left[0]+int(w/2),top_left[1]+int(h/2))
        cv2.circle(img2,centre,50,(0,255,0),-1)
        corners.append(centre)


    cv2.imwrite('res.ppm',img2)
    corners = sorted(corners, key=lambda x: x[1])

    return corners


'''
Flips a page if it is upside down
'''
def flip(img, corners):
    result = img
    w, h = img.shape[::-1]

    if corners[0][1] < 500:
        result = cv2.flip(img,-1)
        corners = findCorners(result)
#        cv2.imwrite('flip.ppm',result)
    return result, corners


'''
Corrects misalignments
'''
def align(img, corners):
    result = img.copy()
    h, w = np.shape(result)
    if corners[0][1] != corners[1][1]:
        xd = corners[0][0] - corners[1][0]
        yd = corners[0][1] - corners[1][1]
        grad = yd/xd
        theta = np.arctan(grad)
        A = cv2.getRotationMatrix2D((w/2,h/2),theta,1)
        result = cv2.warpAffine(result,A,(w,h))
#        cv2.imwrite('align.ppm',result)
        corners = findCorners(result)
#        print corners
    return result


'''
Finds the first answer block

def get_block(img):
    img2 = img.copy()'''

def normalise(img, corners):
    #h = corners[2][1] - corners[0][1]
    #w =  corners[1][0] - corners[0][0]
    h = 4235
    w = 3190
    corners = sorted(corners, key=itemgetter(0))

    crop_img = img[corners[0][1]:corners[0][1]+h, corners[0][0]:corners[0][0]+w]
#    thresh, crop_img = cv2.threshold(crop_img, 200,255,cv2.THRESH_BINARY)
    crop_img = cv2.adaptiveThreshold(~crop_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
cv2.THRESH_BINARY,11,-2)
    cv2.imwrite("cropped.ppm", crop_img)
    return crop_img



def process(path):
    img = cv2.imread(path,0)
    corners = findCorners(img)
    img, corners = flip(img, corners)
    corners = sorted(corners, key=itemgetter(0))
    if (corners[0][0] < 50 or corners[0][0] > 200) and (corners[0][1] < 500 or corners[0][1] > 700):
        corners[0] = (150, 600)
        corners[1] = (3350, 600)
    img = align(img, corners)
    img = normalise(img,corners)
    return img
