from ctypes import DEFAULT_MODE
import time
import mmap
import os
# PE4-NRST
# START IO5 PE17 
# STOP IO6 PE18
# ESTOP IO7 PE19
# RESET IO8 PE20
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

        # read PE_CFG2
        reg = self.getReg(0x98)
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
if __name__=="__main__":
    gpio = GPIO()
    gpio.resetMCU()