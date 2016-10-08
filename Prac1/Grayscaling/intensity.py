import sys
import image_in as reader

def main(filename):
	[size,mx,pixels] = reader.ppmreader(filename)

	header = "P2\n# CREATOR: intensity.py\n{0} {1}\n{2}\n".format(size[0],size[1],mx)

	ppm_out = open('intensity.pgm','w')

	ppm_out.write(header)

	#Apply grayscale
	for i in pixels:
		g = (max(i[0], i[1], i[2]) + min(i[0], i[1], i[2]))/2
		ppm_out.write("%d\n"%(g))

	ppm_out.close()

main('Prac1-origianl.ppm')
