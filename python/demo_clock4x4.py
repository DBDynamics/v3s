from libclock import clock

cc = clock()

while True:

    cc.homeAll()


    for x in range(0, cc.x_num):
        for y in range(0, cc.y_num):
            cc.insertKeyFrame(x,y,0,0,0)
            cc.insertKeyFrame(x,y,0,1,0)
            cc.insertKeyFrame(x,y,1,0,0)
            cc.insertKeyFrame(x,y,1,1,0)

    for x in range(0, cc.x_num):
        for y in range(0, cc.y_num):
            cc.insertKeyFrame(x,y,0,300,360)
            cc.insertKeyFrame(x,y,1,300,-360)

    for x in range(0, cc.x_num):
        for y in range(0, cc.y_num):
            cc.insertKeyFrame(x,y,0,600,0)
            cc.insertKeyFrame(x,y,0,601,0)
            cc.insertKeyFrame(x,y,1,600,0)
            cc.insertKeyFrame(x,y,1,601,0)
    cc.processInterpolation()
    cc.waitSIPose(0, 0, 1)

cc.stop()