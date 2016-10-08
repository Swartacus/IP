import cv2 as cv
import numpy as np
import random as rdm

def encode(px):
	img=px
	sz_img=np.shape(img)

	enc_px1 = np.zeros((2*sz_img[0],2*sz_img[1]))
	enc_px2 = np.zeros((2*sz_img[0],2*sz_img[1]))

	for i in range(0,sz_img[0]):
		for j in range(0,sz_img[1]):
			coin = rdm.randrange(0,2)
			if img[i][j]==0:
			# encode black pixels into layers
				if coin == 1:
					enc_px1[2*i][2*j]=0
					enc_px1[2*i+1][2*j]=255
					enc_px1[2*i][2*j+1]=255
					enc_px1[2*i+1][2*j+1]=0

					enc_px2[2*i][2*j]=255
					enc_px2[2*i+1][2*j]=0
					enc_px2[2*i][2*j+1]=0
					enc_px2[2*i+1][2*j+1]=255
				else:
					enc_px1[2*i][2*j]=255
					enc_px1[2*i+1][2*j]=0
					enc_px1[2*i][2*j+1]=0
					enc_px1[2*i+1][2*j+1]=255

					enc_px2[2*i][2*j]=0
					enc_px2[2*i+1][2*j]=255
					enc_px2[2*i][2*j+1]=255
					enc_px2[2*i+1][2*j+1]=0
			else:
			# encode white pixels into layers
				if coin == 1:
					enc_px1[2*i][2*j]=255
					enc_px1[2*i+1][2*j]=0
					enc_px1[2*i][2*j+1]=0
					enc_px1[2*i+1][2*j+1]=255

					enc_px2[2*i][2*j]=255
					enc_px2[2*i+1][2*j]=0
					enc_px2[2*i][2*j+1]=0
					enc_px2[2*i+1][2*j+1]=255
				else:
					enc_px1[2*i][2*j]=0
					enc_px1[2*i+1][2*j]=255
					enc_px1[2*i][2*j+1]=255
					enc_px1[2*i+1][2*j+1]=0

					enc_px2[2*i][2*j]=0
					enc_px2[2*i+1][2*j]=255
					enc_px2[2*i][2*j+1]=255
					enc_px2[2*i+1][2*j+1]=0

	return enc_px1, enc_px2

def overlay(src,mask):
	sz_src = np.shape(src)
	sz_mask = np.shape(mask)
	out = np.zeros((sz_src[0],sz_src[1]))

	for i in range(0,sz_src[0]):
		for j in range(0,sz_src[1]):
			if int(src[i][j])==255 & int(mask[i][j])==255:
				out[i][j]=255
			elif int(src[i][j])==0 & int(mask[i][j])==0:
				out[i][j]=0
			elif int(src[i][j])==0 & int(mask[i][j])==255:
				out[i][j]=255
			elif int(src[i][j])==255 & int(mask[i][j])==0:
				out[i][j]=255

	return out



def hideImage(filename):
	# read in image, convert to black and white
	img = cv.imread(filename,0)
	rval ,img = cv.threshold(img,135,255,cv.THRESH_BINARY)
	#print img
	# encode image into two seperate images
	enc_img1, enc_img2 = encode(img)
	# overlay image
	ov_img = overlay(enc_img1,enc_img2)

	# write images
	cv.imwrite('overlay.ppm',ov_img)
	cv.imwrite('enc_img1.ppm',enc_img1)
	cv.imwrite('enc_img2.ppm',enc_img2)


hideImage('original.ppm')
