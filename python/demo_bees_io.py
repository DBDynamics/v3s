from libpro import Bee
import time
mid = 0
m = Bee()
for i in range(0, 100):
    time.sleep(0.1)
    print(m.getInputIO(mid))
m.stop()