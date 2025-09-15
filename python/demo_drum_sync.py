from libpro import Bee
import time
import random

from libio import GPIO
import time

io = GPIO()



m = Bee()
NUM_OF_AXIS = 4
# home_offset = []
last_pos = []
tp = []
tp0 = []
tp1 = []
tp2 = []
tp3 = []

tp0A = -51200*14
tp0B = -51200*9
tp0C = -51200*6
tp0D = -51200*8

tp1A = -51200*35
tp1B = -51200*33
tp1C = -51200*35
tp1D = -51200*35

tp0.append(tp0A)
tp0.append(tp0B)
tp0.append(tp0C)
tp0.append(tp0D)
           
tp1.append(tp1A)
tp1.append(tp1B)
tp1.append(tp0C)
tp1.append(tp0D)

tp2.append(tp1A)
tp2.append(tp1B)
tp2.append(tp1C)
tp2.append(tp1D)

tp3.append(tp0A)
tp3.append(tp0B)
tp3.append(tp1C)
tp3.append(tp1D)

# tp2 = []
# tp2.append(-51200*42)
# tp2.append(-51200*40)
# tp2.append(-51200*38)
# tp2.append(-51200*40)

def home():
    print("start 1st homimng ...")
    for mid in range(0,NUM_OF_AXIS):
        m.setHomingDirection(mid, 1)
        m.setHomingLevel(mid, 0)
        m.setAccTime(mid, 1000)
        m.setTargetVelocity(mid, 1000)
    for mid in range(0,NUM_OF_AXIS):  
        m.setHomingMode(mid)
    time.sleep(0.1)
    for mid in range(0,NUM_OF_AXIS):  
        m.waitTargetPositionReached(mid)
    print("1st home done")

    for mid in range(0,NUM_OF_AXIS): 
        tp.append(0)
        last_pos.append(0)
        m.setPositionMode(mid)
    time.sleep(0.1)

def syncPos():
    for axis in range(0,NUM_OF_AXIS):
        last_pos[axis] = m.getActualPosition(axis)
def mov(tp):
    for axis in range(0,NUM_OF_AXIS):
        m.setKeyFrame(axis_num=axis, key_time=0, key_position=last_pos[axis])
        m.setKeyFrame(axis_num=axis, key_time=1, key_position=last_pos[axis])
        m.setKeyFrame(axis_num=axis, key_time=989, key_position=tp[axis])
        m.setKeyFrame(axis_num=axis, key_time=990, key_position=tp[axis])
        last_pos[axis] = tp[axis]
    m.processInterpolation()
    m.waitSIP(0)

def movTp(tp):
    for axis in range(0,NUM_OF_AXIS):
        m.setTargetVelocity(axis, 2400)
        m.setTargetPosition(axis, tp[axis])

home()
syncPos()
for axis in range(0,NUM_OF_AXIS):
    tp[axis] = tp0[axis]
movTp(tp)
# for loop in range(0, 100):
while True:
    ret = io.getInput()

    if ret&0x2:
        print("sensor triggered")
        # for loop in range(0, 5):
        #     for axis in range(0,NUM_OF_AXIS):
        #         tp[axis] = tp1[axis]+random.randint(-50, 50)*512
        #     mov(tp)
        #     # time.sleep(5+random.randint(-3,3))
        #     for axis in range(0,NUM_OF_AXIS):
        #         tp[axis] = tp3[axis]+random.randint(-50, 50)*512    
        #     mov(tp)
        #     # time.sleep(5+random.randint(-3,3))
        delay = 7
        for loop in range(0, 5):
            for axis in range(0,NUM_OF_AXIS):
                tp[axis] = tp1[axis]+random.randint(-50, 50)*512
            movTp(tp)
            time.sleep(delay+0.1*random.randint(-10,10))
            # time.sleep(5+random.randint(-3,3))
            for axis in range(0,NUM_OF_AXIS):
                tp[axis] = tp2[axis]+random.randint(-50, 50)*512    
            movTp(tp)
            time.sleep(delay+0.1*random.randint(-10,10))
            for axis in range(0,NUM_OF_AXIS):
                tp[axis] = tp3[axis]+random.randint(-50, 50)*512    
            movTp(tp)
            time.sleep(delay+0.1*random.randint(-10,10))
            for axis in range(0,NUM_OF_AXIS):
                tp[axis] = tp0[axis]+random.randint(-50, 50)*512    
            movTp(tp)
            time.sleep(delay+0.1*random.randint(-10,10))
    time.sleep(0.1)


print("done")
m.stop()