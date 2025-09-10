from libpro import Bee
import time

m = Bee()

for l in range(100):
    print(m.getBoardEncoderValue())
    time.sleep(0.05)


m.stop()