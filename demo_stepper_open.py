from libpro import Bee
import time

m = Bee()
amid = 0
m.setPowerOnPro(id=amid, soft_limit=0, open_loop=1, with_break=0, limit_off=0)


m.setTargetVelocity(amid, 500)

m.setHomingDirection(amid, 1)
m.setHomingLevel(amid, 0)
m.setHomingMode(amid)
time.sleep(1)
m.waitHomingDone(amid)

m.stop()