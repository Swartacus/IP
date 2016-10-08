import sys
import image_in as reader

def main(filename):
	#open and extract headers from .ppm file.
	[size,mx,pixels] = reader.ppmreader(filename)

	header = "P2\n# CREATOR: weighted.py\n{0} {1}\n{2}\n".format(size[0],size[1],mx)

	#create output file to print to.
	ppm_out = open('weighted.pgm','w')

	ppm_out.write(header)

	#Apply transformation to pixels and print
	for i in pixels:
		g = i[0] * 0.299 + i[1] * 0.587 + i[2] * 0.114
		ppm_out.write("%d\n"%(g))

	ppm_out.close()

main('Prac1-origianl.ppm')
