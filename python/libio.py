from ctypes import DEFAULT_MODE
import time
import mmap
import os
# PE4-NRST
# PG5-BAT
# START IO5 PE17 
# STOP IO6 PE18
# ESTOP IO7 PE19
# RESET IO8 PE20
# OUT1 PE13
# OUT2 PE14
# OUT3 PE15
# OUT4 PE16
class GPIO:
    # Init Process
    def __init__(self):
        self.MAP_MASK = mmap.PAGESIZE - 1
        self.f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
        self.m = mmap.mmap(self.f, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ,offset=  (0x01C20800 & ~self.MAP_MASK))
        self.offset = 0x01C20800 & ~self.MAP_MASK
        print("offset=",self.offset)
        # self.m = mmap.mmap(self.f, 4*mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ,offset=  (0x01C20800))
        self.initIO()

    def getReg(self, offset): 
        self.m.seek(offset+0x800)
        value = int.from_bytes(self.m.read(4),"little")
        # print("Reg Read:", hex(offset),hex(value))
        return value
        
    def setReg(self, offset, value):
        self.m.seek(offset+0x800)
        self.m.write(value.to_bytes(4,"little"))
        # print("Reg Write", hex(offset), hex(value))

    def initIO(self):
        # set PE4 as Output
        # read PE_CFG0
        reg = self.getReg(0x90)
        # PE4 as output
        reg &=~ (0x1<<(4*4))
        reg |= (0x1<<(4*4))
        # write PE_CFG0
        self.setReg(0x90,reg)

        # set PE13 14 15 16 as Output
        # read PE_CFG1
        reg = self.getReg(0x94)
        # PE13 as output
        reg &=~ (0xf<<((13-8)*4))
        reg |= (0x1<<((13-8)*4))
        # PE14 as output
        reg &=~ (0xf<<((14-8)*4))
        reg |= (0x1<<((14-8)*4))
        # PE15 as output
        reg &=~ (0xf<<((15-8)*4))
        reg |= (0x1<<((15-8)*4))
        # write PE_CFG1
        self.setReg(0x94,reg)

        # read PE_CFG2
        # PE16 as output
        reg = self.getReg(0x98)
        reg &=~ (0xf<<((16-16)*4))
        reg |= (0x1<<((16-16)*4))
        # PE17 as input
        reg &=~ (0x7<<4)
        # PE18 as input
        reg &=~ (0x7<<8)
        # PE19 as input
        reg &=~ (0x7<<12)
        # PE20 as input
        reg &=~ (0x7<<16)
        # write PE_CFG2
        self.setReg(0x98,reg)

        # read PE_PULL1
        reg = self.getReg(0xB0)
        # PE17 as PULLUP
        reg |= (0x1<<((17-16)*2))
        # PE18 as PULLUP
        reg |= (0x1<<((18-16)*2))
        # PE19 as PULLUP
        reg |= (0x1<<((19-16)*2))
        # PE20 as PULLUP
        reg |= (0x1<<((20-16)*2))
        # write PE_PULL1
        self.setReg(0xB0,reg) 

        # read PG_CFG0
        reg = self.getReg(0xD8)
        # PG5 as input
        reg &=~ (0x7<<20)
        # write PG_CFG0
        self.setReg(0xD8,reg)

        # read PG_PULL0
        reg = self.getReg(0xF4)
        # PG5 as PULLUP
        reg |= (0x1<<((5)*2))
        # write PG_PULL0
        self.setReg(0xF4,reg) 
    
    def resetMCU(self):
        # read PE_DAT
        reg = self.getReg(0xA0)
        # clear PE4
        reg &=~ (0x1<<4)
        # set PE_DAT PE4
        self.setReg(0xA0,reg)

        time.sleep(0.5)

        # read DAT
        reg = self.getReg(0xA0)
        # set 
        reg |= (0x1<<4)
        # set
        self.setReg(0xA0,reg)

    def getInput(self):
        reg = self.getReg(0xa0)
        reg = reg >>17
        return reg&0xf
    
    def getIOStop(self):
        reg = self.getReg(0xa0)
        if reg & (0x1<<18):
            return 1
        else:
            return 0
    
    def getIO0(self):
        reg = self.getReg(0xa0)
        if reg & (0x1<<17):
            return 1
        else:
            return 0
    def getIO1(self):
        reg = self.getReg(0xa0)
        if reg & (0x1<<18):
            return 1
        else:
            return 0
    def getIO2(self):
        reg = self.getReg(0xa0)
        if reg & (0x1<<19):
            return 1
        else:
            return 0
    def getIO3(self):
        reg = self.getReg(0xa0)
        if reg & (0x1<<20):
            return 1
        else:
            return 0
        
    def setIO1(self, value):
        # read PE_DAT
        reg = self.getReg(0xA0)
        # clear PE13
        if value:
            reg |= (0x1<<13)
        else:
            reg &=~ (0x1<<13)
        # set PE_DAT
        self.setReg(0xA0,reg)
    def setIO2(self, value):
        # read PE_DAT
        reg = self.getReg(0xA0)
        # clear PE14
        if value:
            reg |= (0x1<<14)
        else:
            reg &=~ (0x1<<14)
        # set PE_DAT 
        self.setReg(0xA0,reg)

    def setIO3(self, value):
        # read PE_DAT
        reg = self.getReg(0xA0)
        # clear PE15
        if value:
            reg |= (0x1<<15)
        else:
            reg &=~ (0x1<<15)
        # set PE_DAT 
        self.setReg(0xA0,reg)

    def setIO4(self, value):
        # read PE_DAT
        reg = self.getReg(0xA0)
        # clear PE16 
        if value:
            reg |= (0x1<<16)
        else:
            reg &=~ (0x1<<16)
        # set PE_DAT 
        self.setReg(0xA0,reg)

    def getPowerState(self):
        # get PG_DAT
        reg = self.getReg(0xE8)
        if reg & (0x1<<5):
            return 1
        else:
            return 0


if __name__=="__main__":
    gpio = GPIO()
    gpio.resetMCU()