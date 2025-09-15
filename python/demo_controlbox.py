from libio import GPIO
import time

io = GPIO()

while True:
# for loop in range(100):
    ret = io.getInput()
    if ret&0x1:
        print("Button 0 pressed")
    if ret&0x2:
        print("Button 1 pressed")
    if ret&0x4:
        print("Button 2 pressed")
        io.setIO2(1)
        time.sleep(5)
    else:
        io.setIO2(0)
    if ret&0x8:
        print("Button 3 pressed")
    time.sleep(0.1)