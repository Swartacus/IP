import vid_in
import os

# unpack video
vid = vid_in.getVid('video.mp4')

threshold = 15

for h in xrange(len(vid)):
    fwrite = open('Frames/frame_diff{0}.ppm'.format(str(h).zfill(4)),'w')
    fwrite.write("P3\n{0} {1}\n{2}\n".format(640,360,255))

    # do frame differencing
    for i in xrange(len(vid[h])):
        for j in xrange(len(vid[h][i])):
            diff = abs((0.21*vid[h][i][j][0]+0.72*vid[h][i][j][1]+0.07*vid[h][i][j][2])-(0.21*vid[h-1][i][j][0]+0.72*vid[h-1][i][j][1]+0.07*vid[h-1][i][j][2]))
            if diff > threshold:
               fwrite.write("{0}\n{1}\n{2}\n".format(vid[h][i][j][0],vid[h][i][j][1],vid[h][i][j][2]))
            else:
                fwrite.write("0\n0\n0\n")

# repack video
os.system("ffmpeg -framerate 10 -f image2 -i Frames/frame_diff%04d.ppm frame_diff.mp4")
os.system("rm Frames/frame_diff*")
