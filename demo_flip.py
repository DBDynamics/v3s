from libflip import Flip
import time

f = Flip()

f.homeAll()

for i in range(0, 30):
    time.sleep(1)
    for axis in range(4, 8):
        f.flipNPage(axis, 1)

f.stop()