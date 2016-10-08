import vid_in
import os

# unpack video
vid = vid_in.getVid('video.mp4')
B   = vid[0]
a   = 0.4
threshold = 15

for h in xrange(len(vid)):
    fwrite = open('Frames/run_avg_sel{0}.ppm'.format(str(h).zfill(4)),'w')
    fwrite.write("P3\n{0} {1}\n{2}\n".format(640,360,255))

    for i in xrange(len(vid[h])):
        for j in xrange(len(vid[h][i])):
            diff = abs((0.21*B[i][j][0]+0.72*B[i][j][1]+0.07*B[i][j][2])-(0.21*vid[h][i][j][0]+0.72*vid[h][i][j][1]+0.07*vid[h][i][j][2]))
            if diff > threshold:
                fwrite.write("{0}\n{1}\n{2}\n".format(vid[h][i][j][0],vid[h][i][j][1],vid[h][i][j][2]))
            else:
                fwrite.write("0\n0\n0\n")
                B[i][j] = a*vid[h][i][j] + (1-a)*B[i][j]

# repack video
os.system("ffmpeg -f image2 -i Frames/run_avg_sel%04d.ppm run_avg_sel.mp4")
os.system("rm Frames/run_avg_sel*")
