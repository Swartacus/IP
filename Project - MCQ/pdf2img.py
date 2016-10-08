'''
pdf2img.py
Author: Adam Swart
Script that converts all pages from a pdf document to jpeg images, and converts
the jpeg images to the ppm format
'''

from wand.image import Image
import cv2
import cvutils


#extract images from pdf and save as jpeg
def getppm(filename):
    with Image(filename=filename,resolution=(600,600)) as img:
		img_width = img.width
		img.format = 'jpeg'
		img.save(filename="images/jpeg/pg.jpeg")

    jpgs = cvutils.imlist('images/jpeg')

    #convert jpeg images to ppm
    i = 0
    for k in jpgs:
        img = cv2.imread(k)
        cv2.imwrite('images/ppm/mcq{0}.ppm'.format(i), img)
        i += 1

#getppm('MCQ_600dpi_2016.pdf')
