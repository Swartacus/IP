import vid_in
import os

# unpack video
vid = vid_in.getVid('video.mp4')
back = vid[0]
threshold = 15

for h in xrange(len(vid)):
    fwrite = open('Frames/back_sub{0}.ppm'.format(str(h).zfill(4)),'w')
    fwrite.write("P3\n{0} {1}\n{2}\n".format(640,360,255))

    # do background subtraction
    for i in xrange(len(vid[h])):
        for j in xrange(len(vid[h][i])):
            d = abs((0.21*back[i][j][0]+0.72*back[i][j][1]+0.07*back[i][j][2])-(0.21*vid[h][i][j][0]+0.72*vid[h][i][j][1]+0.07*vid[h][i][j][2]))
            if d > threshold:
                fwrite.write("{0}\n{1}\n{2}\n".format(vid[h][i][j][0],vid[h][i][j][1],vid[h][i][j][2]))
            else:
                fwrite.write("0\n0\n0\n")

# repack video
os.system("ffmpeg -f image2 -i Frames/back_sub%04d.ppm back_sub.mp4")
os.system("rm Frames/back_sub*")
