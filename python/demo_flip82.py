import time
import os
from libpro import Bee

# 显示日期
# 1984年1月1日到今天现在时间 输出年月日十分秒
import datetime

class Flip:
    # Init Process
    def __init__(self):
        self.m = Bee()
        self.resolution = 51200 / 10
        self.NUMBER_OF_AXIS = 12
        self._last_position = []
        self.last_page = []
        for axis in range(0, self.NUMBER_OF_AXIS):
            self._last_position.append(0)
            self.last_page.append(0)

    def stop(self):
        self.m.stop()

    def homeAll(self):
        print("1st homing")
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.setTargetVelocity(axis, 500)
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.setHomingMode(axis)
        time.sleep(0.1)
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.waitTargetPositionReached(axis)
            print("axis",axis,"homed")
        print("1st homing done")

        print("move a bit")
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.setTargetVelocity(axis, 500)
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.setTargetPosition(axis, 5*self.resolution)
        time.sleep(0.1)
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.waitTargetPositionReached(axis)

        print("2nd homing")
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.setTargetVelocity(axis, 500)
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.setHomingMode(axis)
        time.sleep(0.1)
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.waitTargetPositionReached(axis)
            self._last_position[axis] = 0
        print("2nd homing done")

        print("move to 0")
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.setTargetVelocity(axis, 100)
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.setTargetPosition(axis, 0)
        time.sleep(0.1)
        for axis in range(0, self.NUMBER_OF_AXIS):
            self.m.waitTargetPositionReached(axis)
    def flipNPage(self,axis,pages):
        tp = pages*self.resolution+self._last_position[axis]
        self.m.setTargetPosition(axis, tp)
        self._last_position[axis] = tp
    
    def displayPage(self,axis, page):
        dn = page - self.last_page[axis]
        if dn < 0:
            dn += 10
        self.last_page[axis] = page
        self.flipNPage(axis, dn)

    def disp_year(self, year):
        num_0 = (int)(year)%10
        num_1 = (int)(year/10)%10
        self.displayPage(0, num_1)
        self.displayPage(1, num_0)

    def disp_month(self, month):
        num_0 = (int)(month)%10
        num_1 = (int)(month/10)%10
        self.displayPage(2, num_1)
        self.displayPage(3, num_0)
    def disp_day(self, day):
        num_0 = (int)(day)%10
        num_1 = (int)(day/10)%10
        self.displayPage(4, num_1)
        self.displayPage(5, num_0)

    def disp_hour(self, hour):
        num_0 = (int)(hour)%10
        num_1 = (int)(hour/10)%10
        self.displayPage(6, num_1)
        self.displayPage(7, num_0)
    def disp_minute(self, minute):
        num_0 = (int)(minute)%10
        num_1 = (int)(minute/10)%10
        self.displayPage(8, num_1)
        self.displayPage(9, num_0)
    def disp_second(self, second):
        num_0 = (int)(second)%10
        num_1 = (int)(second/10)%10
        self.displayPage(10, num_1)
        self.displayPage(11, num_0)

    def disp_date(self):
        # 1984年1月1日
        start_date = datetime.datetime(1984, 1, 1)
        now = datetime.datetime.now()
        # 计算时间差
        delta = now - start_date
        # 输出时间差
        # print(delta)

        delta_years = delta.days // 365
        # delta_months = (delta.days % 365) // 30
        # delta_days = (delta.days % 365) % 30
        # print(delta_years, delta_months, delta_days)

        delta_hours = delta.seconds // 3600
        delta_minutes = (delta.seconds % 3600) // 60
        delta_seconds = (delta.seconds % 3600) % 60
        # print(delta_hours, delta_minutes, delta_seconds)

        self.disp_year(delta_years)
        self.disp_month(now.month)  # 月份从1开始
        self.disp_day(now.day)  # 日期从1开始
        self.disp_hour(delta_hours)
        self.disp_minute(delta_minutes)
        self.disp_second(delta_seconds)

    def displayNum(self, axis, num):
        page = (10-num)%10
        self.displayPage(axis, page)

    
    def initDevice(self):
        base_current = 800
        parameter_n = 2
        parameter_p = 3
        homing_velocity = 200
        homing_direction = 1
        homing_level = 0
        acc_time = 500
        for mid in range(0,self.NUMBER_OF_AXIS):
            self.m.setPowerOn(mid)
            self.m.setCurrentBase(mid, base_current)
            self.m.setCurrentP(mid, parameter_p)
            self.m.setCurrentN(mid, parameter_n)
            self.m.setTargetVelocity(mid, homing_velocity)
            self.m.setAccTime(mid, acc_time)
            self.m.setHomingDirection(mid, homing_direction)
            self.m.setHomingLevel(mid, homing_level)
            self.m.setPositionMode(mid)
            time.sleep(0.1)


f = Flip()
f.initDevice()
f.homeAll()
# 等待3*60s 同步时间
# time.sleep(60*3)
os.system("/usr/bin/python3 /root/timesync.py")
time.sleep(1)
while True:
    f.disp_date()
    time.sleep(0.1)



f.stop()