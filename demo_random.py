from DBDynamics import Ant
import time
import random
from libio import GPIO
io = GPIO()

axis_s = 1
axis_e = 4
p=[]
for i in range(0, 6):
    p.append(0)
def homeAll():
    for mid in range(axis_s, 6):
        m.setPowerOn(mid)
        m.setTargetVelocity(mid, 50)
        m.setHomingLevel(mid, 0)
        m.setHomingMode(mid)
    time.sleep(1)
    for mid in range(axis_s, axis_e):
        m.waitTargetPositionReached(mid)
    time.sleep(1)
    for mid in range(axis_s, axis_e):
        m.setTargetPosition(mid,25000)
    time.sleep(1)
    for mid in range(axis_s, axis_e):
        m.waitTargetPositionReached(mid)
        m.setHomingMode(mid)
    time.sleep(1)
    for mid in range(axis_s, axis_e):
        m.waitTargetPositionReached(mid)
    time.sleep(1)

mid = 5
m = Ant('/dev/ttyUSB0')  # COM3
homeAll()
m.setTargetVelocity(mid, 50)
tp0 = 0
last_key = 0
# for loop in range(0, 1000):
while True:
    # print("loop")
    time.sleep(0.1)
    ret = io.getInput()
    if ret&0x8:
        # print("Button pressed")
        if last_key!=ret:
            print("Button pressed")
            for mid in range(axis_s, axis_e):
                tp = random.randint(1, 4)
                print(tp)
                p[mid] += tp*50000/4+50000*5
                m.setTargetPosition(mid, p[mid])
            time.sleep(0.1)
            for mid in range(axis_s, axis_e):
                m.waitTargetPositionReached(mid)

    last_key = ret
    

m.stop()