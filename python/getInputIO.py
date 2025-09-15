from libio import GPIO
import time

io = GPIO()

for loop in range(0, 100):
    ret = io.getInput()
    if ret&0x1==0:
        print("Button 0 pressed")
    if ret&0x2==0:
        print("Button 1 pressed")
    if ret&0x4==0:
        print("Button 2 pressed")
    if ret&0x8==0:
        print("Button 3 pressed")
    # ret = io.getPowerState()
    # if ret:
    #     print("power state 1")
    # else:
    #     print("power state 0")
    time.sleep(0.1)

# for loop in range(0, 100):
#     ret = io.getInput()
#     if ret&0x1==0:
#         print("Button 0 pressed")
#     if ret&0x2==0:
#         print("Button 1 pressed")
#     if ret&0x4==0:
#         print("Button 2 pressed")
#     if ret&0x8==0:
#         print("Button 3 pressed")
#     time.sleep(0.1)