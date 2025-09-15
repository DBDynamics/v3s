import serial
import mmap
import os
import ctypes
import queue
import struct
import threading
import time

_INDEX_DEVICE_ADDR = 0
_INDEX_CONTROLWORD = 1
_INDEX_STATUSWORD = 2
_INDEX_OPMODE = 3
_INDEX_TARGET_A = 4
_INDEX_TARGET_B = 5
_INDEX_ACTUAL_A = 6
_INDEX_ACTUAL_B = 7
_INDEX_SENSOR = 8
_INDEX_OFFSET_A = 9
_INDEX_OFFSET_B = 10

_FUNC_READ = 0X03
_FUNC_WRITE = 0X06

_PARA_ADDR = 0X5000
_AP_ADDR = 0X4800
MAP_MASK = 8*mmap.PAGESIZE - 1
f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
m = mmap.mmap(f, 8*mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ, offset= (0x41000000 & ~MAP_MASK))

def _getValue(index):
    m.seek(_PARA_ADDR+index*2)
    value = int.from_bytes(m.read(2),"little", signed=True)
    return value

def _setValue( index, value):
    m.seek(_PARA_ADDR+index*2)
    m.write(value.to_bytes(2,"little", signed=True))

def _getAP(index):
    m.seek(_AP_ADDR+4+index*4)
    value = int.from_bytes(m.read(4),"little", signed=True)
    return value

portName = '/dev/ttyUSB0'

port = serial.Serial(portName, 9600, timeout=0.1)
message = bytearray(8)
message[0] = 0x01
message[1] = 0x03

message[2] = 0x00
message[3] = 0x00

message[4] = 0x00
message[5] = 0x03

message[6] = 0x05
message[7] = 0xCB

k=[]
k.append((51200.0 * 10.0)/3600.0)
k.append((51200.0 * 5.0)/3600.0)
# for loop in range(0, 100):
while True:
    port.write(message)
    time.sleep(0.1)
    ret = port.read(11)
    value = (ret[3] << 8) + ret[4]
    # print(ret, len(ret))
    # print(30000-value)
    _setValue(_INDEX_SENSOR, 30000-value)
    apa = _getAP(0)
    apb = _getAP(1)
    comp_a = _getValue(_INDEX_OFFSET_A)
    comp_b = _getValue(_INDEX_OFFSET_B)
    # print(comp_a,comp_b)
    angle_a = (apa)/k[0]-comp_a
    angle_b = (apb)/k[1]-comp_b
    # print(angle_a, angle_b)
    _setValue(_INDEX_ACTUAL_A, round(angle_a))
    _setValue(_INDEX_ACTUAL_B, round(angle_b))

port.close()
