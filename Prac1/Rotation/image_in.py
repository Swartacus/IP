import sys

def ppmreader(ppmfile):

	file = open(ppmfile)

	data = file.readlines()

	# Extract data

	ppm_size = data[2]
	ppm_size = ppm_size.split(' ')
	ppm_mx = data[3]
	ppm_pixels = data[4:len(data)]

	size = map(int,ppm_size)
	mx = int(ppm_mx)
	img = map(int,ppm_pixels)

	pixels = [img[3*i:3*(i+1)] for i in range(len(img)/3)]

	file.close()

	return [size,mx,pixels]
