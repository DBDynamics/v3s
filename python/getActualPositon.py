from libpro import Bee
import time
m = Bee()
mid  = 2

for loop in range(100):
    ret = m.getActualPosition(mid)

    print(ret)
    time.sleep(0.1)