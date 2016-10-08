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

x_ratio = 0.5
y_ratio = 0.5


out = [0]*125*125


for j in range(125):
	for k in range(125):
		x = int(k/x_ratio)
		y = int(j/y_ratio)
		out[(j*125)+k] = pixels[(y*250)+x]

fileout = open("NNSmaller.ppm","w")
fileout.write("P3\n# CREATOR: nnsmaller.py\n125 125\n255\n")
for p in out:
	fileout.write("{0}\n{1}\n{2}\n".format(p[0],p[1],p[2]))