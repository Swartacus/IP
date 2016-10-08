def getVid(vid):
    import subprocess as sp
    import numpy

    FFMPEG_BIN = "ffmpeg"

    command = [ FFMPEG_BIN,
                '-i', vid,
                '-f', 'image2pipe',
                '-pix_fmt', 'rgb24',
                '-vcodec', 'rawvideo', '-']
    pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    video = []
    while True:
        raw_img = pipe.stdout.read(640*360*3)
        if not raw_image: break
        img =  numpy.fromstring(raw_img, dtype='uint8')
        img = img.reshape((640,360,3))
        pipe.stdout.flush()
        video.append(img)

    return video
