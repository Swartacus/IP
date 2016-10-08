import sys
import image_in

def main(filename):
	[size,mx,pixels] = image_in.ppmreader(filename)

	out = open('average.pgm','w')

	header = "P2\n# CREATOR: average.py\n{0} {1}\n{2}\n".format(size[0],size[1],mx)

	out.write(header)

	#Apply grayscale
	for i in pixels:
		g = (i[0]+i[1]+i[2])/3
		out.write("%d\n"%g)

	out.close()

main('Prac1-origianl.ppm')
