from libpro import Bee
import time

m = Bee()

for mid in range(0,2):
    m.setTargetVelocity(mid, 5000)
    m.setAccTime(mid, 200)
    m.setPositionMode(mid)
    m.setPowerOn(mid)
time.sleep(1)
for loop in range(0, 3):
    for mid in range(0,2):
        m.setTargetPosition(mid, 0)
    for mid in range(0,2):
        m.waitTargetPositionReached(mid)

    for mid in range(0,2):
        m.setTargetPosition(mid, 51200*10)
    for mid in range(0,2):
        m.waitTargetPositionReached(mid)


m.stop()