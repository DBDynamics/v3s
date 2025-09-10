from libdoor import Door
import time

d = Door()
d.homeAll()

key_state = 0
last_key_state = 0
state = 0
print("home done")
while True:
    time.sleep(0.1)
    key_state = d.io.getIO0()
    if key_state != last_key_state:
        if key_state == 0:
            if state == 0:
                print("open")
                d.mov_file("/root/open.npy")
                state= 1
            else:
                print("Close")
                d.mov_file("/root/close.npy")
                state= 0
    last_key_state = key_state
d.stop()
