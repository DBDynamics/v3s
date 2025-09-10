from libpro import Bee
import time

time.sleep(5)
m = Bee()
time.sleep(1)
for axis in range(0, 22):
    m.setAccTime(axis, 200)
    m.setTargetVelocity(axis, 50)
    m.setPositionMode(axis)
time.sleep(1)
# for loop in range(0, 3):
while True:
    for axis in range(0, 22):
        m.setTargetPosition(axis, 51200*10)
    time.sleep(1)
    m.waitTargetPositionReached(0)
    time.sleep(30)

    for axis in range(0, 22):
        m.setTargetPosition(axis, 0)
    time.sleep(1)
    m.waitTargetPositionReached(0)
    time.sleep(30)

time.sleep(1)
m.stop()