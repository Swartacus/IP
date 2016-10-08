import sys
import image_in

def main(filename):
	[size,mx,pixels] = image_in.ppmreader(filename)

	header = "P2\n# CREATOR: channels.py\n{0} {1}\n{2}\n".format(size[0],size[1],mx)

	r = open('rchannel.pgm','w')
	g = open('gchannel.pgm','w')
	b = open('bchannel.pgm','w')

	r.write(header)
	g.write(header)
	b.write(header)

	#Apply grayscale
	for i in pixels:
		r.write("%d\n"%(i[0]))
		g.write("%d\n"%(i[1]))
		b.write("%d\n"%(i[2]))

	r.close()
	g.close()
	b.close()

main('Prac1-origianl.ppm')
