from libpro import Bee
import time

m = Bee()

m.t_hellolib()
m.setSDOMode()
lp = []

for i in range(0,32):
    lp.append(0)
for axis in range(0, 32):
    lp[axis]= m.getActualPosition(axis)

# m.setPDOMode()
for axis in range(0,24):
    m.setKeyFrame(axis_num=axis, key_time=0, key_position=lp[axis])
    m.setKeyFrame(axis_num=axis, key_time=1, key_position=lp[axis])
    m.setKeyFrame(axis_num=axis, key_time=99, key_position=0)
    m.setKeyFrame(axis_num=axis, key_time=100, key_position=0)
m.processInterpolation()
m.waitSIP(0)

time.sleep(5)

# 转360度 耗时60s 停止 30s 循环
time_cost = 60*100
time_display = 30

for axis in range(0,23):
    m.setKeyFrame(axis_num=axis, key_time=0, key_position=0)
    m.setKeyFrame(axis_num=axis, key_time=1, key_position=0)

    m.setKeyFrame(axis_num=axis, key_time=time_cost-1, key_position=51200)
    m.setKeyFrame(axis_num=axis, key_time=time_cost, key_position=51200)

m.processInterpolation()
m.waitSIP(0)
time.sleep(time_display)

time.sleep(1)
m.stop()

