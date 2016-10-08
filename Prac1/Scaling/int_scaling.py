f = open("Scaling.ppm")
pixels = []
i = 0

R = 0
B = 0
G = 0

for line in f:
	i += 1
	if (i > 4):
		if (i % 3) == 2:
			R = int(line)
		if (i % 3) == 0:
			G = int(line)
		if (i % 3) == 1:
			B = int(line)
			pixels.append([R, G, B])

x_ratio = 2.0
y_ratio = 2.0


out = [0]*500*500


for j in range(500):
	for k in range(500):
		x = int(k/x_ratio)
		y = int(j/y_ratio)
		xdiff = (k/x_ratio)-x
		ydiff = (j/y_ratio)-y
		idx = y*250+x
		a = pixels[idx]
		b = pixels[(idx+1)%len(pixels)]
		c = pixels[(idx+250)%len(pixels)]
		d = pixels[(idx+250+1)%len(pixels)]

		r = int((a[0])*(1-xdiff)*(1-ydiff) + (b[0])*xdiff*(1-ydiff) + (c[0])*ydiff*(1-xdiff) + d[0]*xdiff*ydiff)
		g = int((a[1])*(1-xdiff)*(1-ydiff) + (b[1])*xdiff*(1-ydiff) + (c[1])*ydiff*(1-xdiff) + d[1]*xdiff*ydiff)
		b = int((a[2])*(1-xdiff)*(1-ydiff) + (b[2])*xdiff*(1-ydiff) + (c[2])*ydiff*(1-xdiff) + d[2]*xdiff*ydiff)

		out[(j*500)+k] = [r,g,b]

fileout = open("IntBigger.ppm","w")
fileout.write("P3\n# CREATOR: int_scaling.py\n500 500\n255\n")
for p in out:
	fileout.write("{0}\n{1}\n{2}\n".format(p[0],p[1],p[2]))