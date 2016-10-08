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
		out[(j*500)+k] = pixels[(y*250)+x]

fileout = open("NNBigger.ppm","w")
fileout.write("P3\n# CREATOR: nnbigger.py\n500 500\n255\n")
for p in out:
	fileout.write("{0}\n{1}\n{2}\n".format(p[0],p[1],p[2]))