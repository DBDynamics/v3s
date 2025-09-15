from libpro import Bee
import time


class CNC:
    def __init__(self):
        self.Ox = 0
        self.Oy = 0
        self.Oz = 0
        self.Lx = 0
        self.Ly = 0
        self.Lz = 0
        self.resolution = 51200/8.0
        self.m = Bee()
        self.m.setTrackingMode(0)


    def stop(self):
        self.m.stop()

    def ServoOn(self):
        self.m.setPowerOn(0)
        self.m.setPowerOn(1)
        self.m.setPowerOn(2)
        time.sleep(3)

    def Zero(self):
        self.m.setTargetPosition(0,0)
        self.m.setTargetPosition(1,0)
        self.m.setTargetPosition(2,0)

    def moveAbs(self,x,y,z):
        self.m.setTargetPosition(0,x*self.resolution)
        self.m.setTargetPosition(1,y*self.resolution)
        self.m.setTargetPosition(2,z*self.resolution)
        self.m.waitTargetPositionReached(0)
        self.m.waitTargetPositionReached(1)
        self.m.waitTargetPositionReached(2)

    def drillOn(self):
        self.m.setOutputIO(0,1)
    def drillOff(self):
        self.m.setOutputIO(0,0)

    def setVelocityZ(self, v):
        self.m.setTargetVelocity(2,v)

    def movZ(self, z):
        self.m.setTargetPosition(2,z*self.resolution)
        self.m.waitTargetPositionReached(2)

    def movXY(self,x,y):
        self.m.setTargetPosition(0,x*self.resolution)
        self.m.setTargetPosition(1,y*self.resolution)
        self.m.waitTargetPositionReached(0)
        self.m.waitTargetPositionReached(1)

    def movXbyEnc(self):
        cp0 = self.m.getActualPosition(0)
        ep0 = self.m.getBoardEncoderValue()
        while True:
            ep = self.m.getBoardEncoderValue()
            self.m.setTargetPosition(0,cp0+(ep-ep0)*0.01*self.resolution)
            time.sleep(0.01)
    def movYbyEnc(self):
        cp0 = self.m.getActualPosition(1)
        ep0 = self.m.getBoardEncoderValue()
        while True:
            ep = self.m.getBoardEncoderValue()
            self.m.setTargetPosition(1,cp0+(ep-ep0)*0.01*self.resolution)
            time.sleep(0.01)

    def movZbyEnc(self):
        cp0 = self.m.getActualPosition(2)
        ep0 = self.m.getBoardEncoderValue()
        while True:
            ep = self.m.getBoardEncoderValue()
            self.m.setTargetPosition(2,cp0+(ep-ep0)*0.01*self.resolution)
            time.sleep(0.01)
    def sync(self):
        self.Ox = self.m.getActualPosition(0)
        self.Oy = self.m.getActualPosition(1)
        self.Oz = self.m.getActualPosition(2)
        print("Ox:",self.Ox,"Oy:",self.Oy,"Oz:",self.Oz)
        self.Lx = self.Ox
        self.Ly = self.Oy
        self.Lz = self.Oz

    def mvIncX(self,x):
        tx = self.Lx+x*self.resolution
        self.m.setTargetPosition(0,self.tx)
        self.Lx = tx
    
    def mvIncY(self,y):
        ty = self.Ly+y*self.resolution
        self.m.setTargetPosition(1,self.ty)
        self.Ly = ty
    
    def mvIncZ(self,z):
        tz = self.Lz+z*self.resolution
        self.m.setTargetPosition(2,tz)
        self.Lz = tz
        print(tz)
    def getEncoder(self):
        return self.m.getBoardEncoderValue()

c = CNC()
c.sync()
# c.ServoOn()
# c.movXbyEnc()
# c.drillOn()
c.drillOff()
# c.movYbyEnc()
# c.movZbyEnc()
# c.drillOn()

# c.mvIncZ(10)
c.stop()
