'''
marker.py
Author: Adam Swart
Marks MCQ sheets
'''
import cv2
import os
import numpy as np
import cvutils
import csv
import cv2.cv as cv
from operator import itemgetter
import pdf2img
import pre_processing
import sys

# answer blocks are (621,660)
#1232,72
'''
Marks the MCQ sheet
'''
def getAnswers(img):
    blocks = [[1232,2178],[72,72+660,72+(660*2),72+(660*3),72+(660*4),72+(660*5)]]
    w = 621
    h = 660
    answers = np.zeros((60,5))
    for i, x in enumerate(blocks[0]):
        for j, y in enumerate(blocks[1]):
            # Isolate the 5x5 answer grid and find all the circles
            crop_img = img[y-10:y+h+10, x-10:x+w+10]
            aimg = cv2.medianBlur(crop_img,5)
            cimg = cv2.cvtColor(aimg, cv2.COLOR_GRAY2BGR)
            circles = cv2.HoughCircles(aimg, cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=25,minRadius=30,maxRadius=50)
            circles = np.uint16(np.around(circles))
            circles= circles[0]
            # cv2.imshow('',crop_img)
            # cv2.waitKey(0)
            # sort the circles into rows and columns
            circles = sorted(circles, key=itemgetter(1))
            rows = [[],[],[],[],[]]
            for l in range(len(circles)):
                rows[l/5].append(circles[l])
            for l in range(len(rows)):
                rows[l] = sorted(rows[l], key=itemgetter(0))

            # determine whether a circle is filled in
            q = 0
            ans = []
            for r in rows:
                count = 0
                line_filled = []
                for b in r:
                    crop = crop_img[b[1]-b[2]:b[1]+b[2], b[0]-b[2]:b[0]+b[2]]
                    p = cv2.countNonZero(crop)
                    t = b[2]*b[2]*(np.pi/4)
            #        print p/float(t)
                    if (p/float(t) > 1.3):
                        #print '{0}: {1}'.format((i*6 + j)*5+q+1, str(unichr(65+count)))
                        answers[(i*6 + j)*5+q, count] = 1
                    count += 1
                q += 1

    return answers


'''
Finds the student number
'''
def studentNum(img):
    # (160,595) to (285,1770)
    # (285,595) to (,)
    # w = 125
    # h = 1175
    # for letter h = 2990
    #thresh, img = cv2.threshold(img, 200,255,cv2.THRESH_BINARY)
    # find the year
    snum = ''
    year_img = img[595:595+1175, 160:160+125*2]
    aimg = cv2.medianBlur(year_img,5)
    cimg = cv2.cvtColor(aimg, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(aimg, cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=25,minRadius=30,maxRadius=50)
    circles = np.uint16(np.around(circles))
    circles= circles[0]
    circles = sorted(circles, key=itemgetter(0))
    # cv2.imshow('',year_img)
    # cv2.waitKey(0)
    cols = [[],[]]
    for l in range(len(circles)):
        cols[l/10].append(circles[l])
    for l in range(len(cols)):
        cols[l] = sorted(cols[l], key=itemgetter(1))
    for c in cols:
        count = 0
        for b in c:
            crop = year_img[b[1]-b[2]:b[1]+b[2], b[0]-b[2]:b[0]+b[2]]
            p = cv2.countNonZero(crop)
            p = cv2.countNonZero(crop)
            t = b[2]*b[2]*(np.pi/4)
            #print p/float(t)
            if (p/float(t) > 1.3):
                snum += str(count)
            count += 1

    # find the letter
    l_img = img[595:595+2990, 160+125*2:160+125*3]
    aimg = cv2.medianBlur(l_img,5)
    circles = cv2.HoughCircles(aimg, cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=25,maxRadius=50)
    circles = np.uint16(np.around(circles))
    circles= circles[0]
    circles = sorted(circles, key=itemgetter(1))
    count = 0
    for b in circles:
        crop = l_img[b[1]-b[2]:b[1]+b[2], b[0]-b[2]:b[0]+b[2]]
        p = cv2.countNonZero(crop)
        t = b[2]*b[2]*(np.pi/4)
        if (p/float(t) > 1.3):
            snum += str(unichr(65+count))
        count += 1

    # find the last 4 numbers
    d_img = img[595:595+1175, 160+125*3 - 5:160+125*7]
    aimg = cv2.medianBlur(d_img,5)
    cimg = cv2.cvtColor(aimg, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(aimg, cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=25,minRadius=25,maxRadius=50)
    circles = np.uint16(np.around(circles))
    # cv2.imshow('',d_img)
    # cv2.waitKey(0)
    circles= circles[0]
    circles = sorted(circles, key=itemgetter(0))
    cols = [[],[],[],[]]
    for l in range(len(circles)):
        cols[l/10].append(circles[l])
    for l in range(len(cols)):
        cols[l] = sorted(cols[l], key=itemgetter(1))
    for c in cols:
        count = 0
        for b in c:
            crop = d_img[b[1]-b[2]:b[1]+b[2], b[0]-b[2]:b[0]+b[2]]
            p = cv2.countNonZero(crop)
            t = b[2]*b[2]*(np.pi/4)
            if (p/float(t) > 1.3):
                snum += str(count)
            count += 1
    if (len(snum) == 7):
        return snum
    else:
        return ''

'''
Finds the task number
'''
def taskNum(img):
    # (695, 1850) to (925,3165)
    task = ''
    task_img = img[2000:3180, 680:950]
    aimg = cv2.medianBlur(task_img,5)
    circles = cv2.HoughCircles(aimg, cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=25,maxRadius=50)
    circles = np.uint16(np.around(circles))
    circles= circles[0]
    circles = sorted(circles, key=itemgetter(0))
    cols = [[],[]]
    for l in range(len(circles)):
        cols[l/10].append(circles[l])
    for l in range(len(cols)):
        cols[l] = sorted(cols[l], key=itemgetter(1))
    for c in cols:
        count = 0
        for b in c:
            crop = task_img[b[1]-b[2]:b[1]+b[2], b[0]-b[2]:b[0]+b[2]]
            p = cv2.countNonZero(crop)
            t = b[2]*b[2]*(np.pi/4)
            if (p/float(t) > 1.3):
                task += str(count)
            count += 1
    if (len(task) == 2):
        return task
    else:
        return ''

def writeResults(answers, task,  snum):
    with open('Results.csv','w') as csvfile:
        fields = ['student_number','task','question','answer']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        for i, j in enumerate(answers):
            ans = ''
            for r in range(len(j)):
                if (j[r] == 1):
                    ans += str(unichr(65+r))
            if len(ans) == 1:
                writer.writerow({'student_number':snum,'task':task,'question':str(i+1) , 'answer':ans})

# do the thing
img = pre_processing.process('images/ppm/mcq{0}.ppm'.format(str(sys.argv[1])))
answers = getAnswers(img)
snum = studentNum(img)
task = taskNum(img)
writeResults(answers,task,snum)
