from libdarm import DArm
from libio import GPIO
import time

io = GPIO()
arm = DArm()

def textA():
    offset = [-90,200,50]
    arm.movj(arm.invK(offset),2)

    offset = [-200,450,z-1.5]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t1-001.npy",offset)

    offset = [-150,400,z-1.5]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t1-002.npy",offset)

    offset = [-65,350,z]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t1-003.npy",offset)

    offset = [-125,300,z-0.5]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t1-004.npy",offset)

    offset = [280,0,100]
    arm.movj(arm.invK(offset),1)
    # time.sleep(30)

    offset = [-90,-200,50]
    arm.movj(arm.invK(offset),2)

    offset = [-150,-200,z+10]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t2-001.npy",offset)

    offset = [-90,-250,z+9.5]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t2-002.npy",offset)

    offset = [-100,-300,z+9]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t2-003.npy",offset)

    offset = [-100,-350,z+9.2]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t2-004.npy",offset)

    offset = [280,0,50]
    arm.movj(arm.invK(offset),1.5)

def textB():
    offset = [-90,200,50]
    arm.movj(arm.invK(offset),2)

    offset = [-90,450,z-1.5]
    arm.movj(arm.invK(offset),1.5)
    arm.mov_file("/root/t3-001.npy",offset)

    offset = [-130,400,z-1.5]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t3-002.npy",offset)

    offset = [-90,350,z-1.5]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t3-003.npy",offset)

    offset = [-90,300,z]
    arm.movj(arm.invK(offset),0.6)
    arm.mov_file("/root/t3-004.npy",offset)

    offset = [280,0,100]
    arm.movj(arm.invK(offset),1)
    # time.sleep(30)

    offset = [0,-200,50]
    arm.movj(arm.invK(offset),2)

    offset = [-150,-250,z+9]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t4-001.npy",offset)

    offset = [-130,-300,z+8.5]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t4-002.npy",offset)

    offset = [-100,-350,z+8.5]
    arm.movj(arm.invK(offset),1)
    arm.mov_file("/root/t4-003.npy",offset)


    offset = [280,0,50]
    arm.movj(arm.invK(offset),1.5)

z = 50
# arm.getJointAngle()
arm.homeAll()
# arm.syncPos()
# offset = [280,0,100]
# arm.movj(arm.invK(offset),1)

# textA()

arm.syncPos()
while True:
    offset = [280,0,100]
    arm.movj(arm.invK(offset),1)
    textA()
    # time.sleep(60)
    textB()
    # time.sleep(60)



arm.stop()
