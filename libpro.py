import ctypes
import mmap
import os
import queue
import struct
import threading
import time
# from scipy.interpolate import PchipInterpolator
import numpy as np
# date:2025-09-05
class Bee:
    # Communication Profiles for BLDCS, do not change them!
    _INDEX_BOARD_TYPE = 0
    _INDEX_DEVICE_ID = 1
    _INDEX_CONTROL_WORD = 2
    _INDEX_OPERATION_MODE = 3
    _INDEX_STATUS_WORD = 4
    _INDEX_TARGET_CURRENT = 5
    _INDEX_IO_OUT = 23

    _INDEX_VOICE_AMP = 7
    _INDEX_VOICE_T = 8
    _INDEX_VOICE_TIME = 9    
    _INDEX_VOICE_LIGHT =  11
    # _INDEX_KPP = 17
    # _INDEX_KPI = 18
    # _INDEX_KPD = 19
    # _INDEX_KFF = 20
    _INDEX_PHASE_CORRECT_CURRENT = 21
    _INDEX_HOMING_DIRECTION = 14
    _INDEX_HOMING_LEVEL = 15
    _INDEX_ACC_TIME = 11
    _INDEX_SYNC_INTERPOLATION_TARGET_POSITION = 12
    
    _INDEX_TARGET_VELOCITY = 7
    _INDEX_TARGET_POSITION = 9
    _INDEX_ACTUAL_VELOCITY = 8
    _INDEX_ACTUAL_POSITION = 10
    _INDEX_IO_INPUT = 22
    _INDEX_ENCODER_OFFSET = 24
    _INDEX_ENCODER_POLARITY = 25
    _INDEX_ENCODER_VALUE = 26
    _INDEX_CURRENT_MAX = 28
    _INDEX_POSITION_ERROR_MAX = 29

    _INDEX_CURRENT_BASE = 17
    _INDEX_CURRENT_P = 18
    _INDEX_CURRENT_N = 19

    _INDEX_HOMING_TRIGGER = 13

    _INDEX_KPP = 17
    _INDEX_KPI = 18
    _INDEX_KVF = 19
    _INDEX_KFF = 20

    _INDEX_CURRENT_BASE = 17
    _INDEX_CURRENT_P = 18
    _INDEX_CURRENT_N = 19

    _INDEX_RUNNING_CURRENT = 17
    _INDEX_KEEPING_CURRENT = 18

    _INDEX_POWER_LIMIT = 28
    _INDEX_LED_OPTION = 29
    _INDEX_SYSTEM_COUNTER = 30
    _INDEX_LED_COUNTER = 31
    _INDEX_ESTOP_DEC = 40

    _FUNC_WRITE = 1
    _FUNC_READ = 0
    _FUNC_WRITE_OK = 3
    _FUNC_READ_OK = 2
    _FUNC_OPERATION = 4
    _FUNC_OPERATION_OK = 5
    _FUNC_CHECK = 254
    _FUNC_FREE = 255
    _OPERATION_MODE_PWM = 0
    _OPERATION_MODE_PROFILE_VELOCITY = 21
    _OPERATION_MODE_PROFILE_POSITION = 31
    _OPERATION_MODE_HOMING = 40
    _OPERATION_MODE_ESTOP = 61
    _OPERATION_SYNC_INTERPOLATION_POSITION = 34
    _OPERATION_MODE_INTERPOLATION_POSITION = 34
    _OPERATION_INDEX_MEMORY = 1
    _OPERATION_INDEX_TUNING = 2

    _STATUS_DEVICE_ENABLE = 0X01
    _STATUS_HOMG_FIND = 0X02
    _STATUS_TARGET_REACHED = 0X04
    _STATUS_IO_INPUT = 0X08
    _STATUS_IO_INPUT_LIMIT_P = 0X10
    _STATUS_IO_INPUT_LIMIT_N = 0X20
    _STATUS_ESTOP = 0X40

    _STATUS_OPMODE_MASK = 0X380
    _STATUS_OPMODE_PROFILE_POSITION = (0<<7)
    _STATUS_OPMODE_PROFILE_VELOCITY = (1<<7)
    _STATUS_OPMODE_SENSOR_HOMING = (2<<7)
    _STATUS_OPMODE_SENSORLESS_HOMING = (3<<7)
    _STATUS_OPMODE_ESTOP_FAST = (4<<7)
    _STATUS_OPMODE_ESTOP_PROFILE = (5<<7)
    _STATUS_OPMODE_SYNC_INTERPOALTION = (6<<7)

    _STATUS_ERROR_OVERCURRENT = 0X20
    _STATUS_ERROR_OVERPOSITION = 0X40
    
    _BOARD_TYPE_STEPPER_ANT = 0X10
    _BOARD_TYPE_STEPPER_BEE = 0X11
    _BOARD_TYPE_STEPPER_ELEPHANT = 0X12
    _BOARD_TYPE_BDCS_BEE = 0X13
    _BOARD_TYPE_BDC_BEE = 0X14
    _BOARD_TYPE_BLDCS_BEE = 0X15

    _private_msg = ctypes.create_string_buffer(8)
    _empty_msg = ctypes.create_string_buffer(8)
    func_code = 0
    index = 0
    id = 0
    subid = 0
    data = 0
    _errorFlag = 0

    def _delay(self):
        time.sleep(0.005)

    # def getEnc(self, axis):
    #     self.m.seek(0x1000+4*(1+axis))
    #     value = int.from_bytes(self.m.read(4),"little", signed=True)
    #     return value
    
    # def clearEnc(self, axis):
    #     value = 0
    #     self.m.seek(0x1000+4*(1+axis))
    #     self.m.write(value.to_bytes(4,"little"))
    
    def clearOnline(self):
        value = 0
        self.m.seek(0x6000)
        self.m.write(value.to_bytes(4,"little"))
    
    def getUdpSharedRam(self):
        self.m.seek(0x6000)
        return self.m.read(1024)
    def setUdpSharedRam(self, tx_buf):
        self.m.seek(0x6400)
        self.m.write(tx_buf)

    def setTP(self, axis, tp):
        struct.pack_into('i', self._sip_frame_data, axis*4, *(tp,))

    def getBoardEncoderValue(self):
        self.m.seek(0x4104)
        value = int.from_bytes(self.m.read(4),"little", signed=True)
        return value
    def updateTP(self):
        self.m.seek(0x5500)
        self.m.write(self._sip_frame_data)
    
    def setUserData(self, index, value):
        self.m.seek(0x5500+index*4)
        self.m.write(value.to_bytes(4, byteorder='little', signed=True))
        
    def getUserData(self, index):
        self.m.seek(0x5500+index*4)
        value = int.from_bytes(self.m.read(4),"little", signed=True)
        return value

    def clearTxDMA(self, axis):
        self.m.seek(0x4800+4*axis)
        value = 0
        self.m.write(value.to_bytes(4,"little"))

    # def getCP(self):
    #     self.m.seek(0x2000+4*500)
    #     value = int.from_bytes(self.m.read(4),"little", signed=True)
    #     return value

    def getAcc(self):
        self.m.seek(0x5400+4*1)
        value = int.from_bytes(self.m.read(4),"little", signed=True)
        return value

    def getErrorMax(self):
        self.m.seek(0x5400+4*2)
        value = int.from_bytes(self.m.read(4),"little", signed=True)
        return value

    def getVelMax(self):
        self.m.seek(0x5400+4*3)
        value = int.from_bytes(self.m.read(4),"little", signed=True)
        return value

    def getFilter(self,n):
        self.m.seek(0x5400+4*(4+n))
        value = int.from_bytes(self.m.read(4),"little", signed=False)
        return value

    # default 50 20000 2000
    def _setTrackingParam(self, acc, range, speed):
        self.m.seek(0x5400+4)
        self.m.write(acc.to_bytes(4,"little"))
        self.m.seek(0x5400+4*2)
        self.m.write(range.to_bytes(4,"little"))
        self.m.seek(0x5400+4*3)
        self.m.write(speed.to_bytes(4,"little"))
    
    def _setTrackingFilter(self,n,value):
        if n > -1:
            if n < 2:
                self.m.seek(0x5400+4*(4+n))
                self.m.write(value.to_bytes(4,"little"))

    def setTrackingMode(self, value):
        self.m.seek(0x5400)
        self.m.write(value.to_bytes(4,"little"))

    def checkSDOTxQueueReady(self):
        self.m.seek(0x31)
        tail = int.from_bytes(self.m.read(1), "little")

        self.m.seek(0x30)
        head = int.from_bytes(self.m.read(1), "little")
        if head == tail:
            return 1
        else:
            return 0
    def _sendMessageRaw(self, message):
        # message = bytearray(8)
        # struct.pack_into('B', message, 0, *(func_code,))
        # struct.pack_into('B', message, 1, *(index,))
        # struct.pack_into('B', message, 2, *(id,))
        # struct.pack_into('B', message, 3, *(subid,))
        # struct.pack_into('i', message, 4, int(*(data,)))

        self.m.seek(0x32)
        lock = int.from_bytes(self.m.read(1), "little")
        while lock == 1:
            time.sleep(0.01)
            print("wait lock off")
            lock = int.from_bytes(self.m.read(1), "little")
        lock = 1
        self.m.write(lock.to_bytes(1, "little"))

        self.m.seek(0x31)
        tail = int.from_bytes(self.m.read(1), "little")

        self.m.seek(0x30)
        head = int.from_bytes(self.m.read(1), "little")
        # print("-")
        # print(head)

        # print(tail)
        head += 1
        if head >= self._SDO_RING_BUF_SIZE:
            head = 0
        if head == tail:
            print("tx ring buffer full")
            print(head)
        # Write Msg to SRAM
        self.m.seek(0x38 + head * 0x8)
        self.m.write(message)
        # print(msg)
        # Write head to SRAM
        self.m.seek(0x30)
        self.m.write(head.to_bytes(1, "little"))

        lock = 0
        self.m.seek(0x32)
        self.m.write(lock.to_bytes(1, "little"))
    def _sendMessage(self, func_code, index, id, subid, data):
        message = bytearray(8)
        struct.pack_into('B', message, 0, *(func_code,))
        struct.pack_into('B', message, 1, *(index,))
        struct.pack_into('B', message, 2, *(id,))
        struct.pack_into('B', message, 3, *(subid,))
        struct.pack_into('i', message, 4, int(*(data,)))

        self.m.seek(0x32)
        lock = int.from_bytes(self.m.read(1), "little")
        while lock == 1:
            time.sleep(0.01)
            print("wait lock off")
            lock = int.from_bytes(self.m.read(1), "little")
        lock = 1
        self.m.write(lock.to_bytes(1, "little"))

        self.m.seek(0x31)
        tail = int.from_bytes(self.m.read(1), "little")

        self.m.seek(0x30)
        head = int.from_bytes(self.m.read(1), "little")
        # print("-")
        # print(head)

        # print(tail)
        head += 1
        if head >= self._SDO_RING_BUF_SIZE:
            head = 0
        if head == tail:
            print("tx ring buffer full")
            print(head)
        # Write Msg to SRAM
        self.m.seek(0x38 + head * 0x8)
        self.m.write(message)
        # print(msg)
        # Write head to SRAM
        self.m.seek(0x30)
        self.m.write(head.to_bytes(1, "little"))

        lock = 0
        self.m.seek(0x32)
        self.m.write(lock.to_bytes(1, "little"))

    def _sendPDOMsg(self, pdodata):
        self.m.seek(0x2438 + 0x2)
        lock = int.from_bytes(self.m.read(1), "little")
        while lock == 1:
            time.sleep(0.01)
            print("wait lock off")
            lock = int.from_bytes(self.m.read(1), "little")
        lock = 1
        self.m.write(lock.to_bytes(1, "little"))

        self.m.seek(0x2438 + 0x1)
        self.tail = int.from_bytes(self.m.read(1), "little")

        self.m.seek(0x2438)
        self.head = int.from_bytes(self.m.read(1), "little")

        # print("head",self.head,"tail",self.tail)

        self.head += 1
        if self.head >= self._PDO_RING_BUF_SIZE:
            self.head = 0
        if self.head == self.tail:
            print("pdo tx ring buffer full")
            print(self.head)
        # Write Msg to SRAM
        self.m.seek(0x2438 + 0x4 + self.head * 256)
        self.m.write(pdodata)
        # print(msg)
        # Write head to SRAM
        self.m.seek(0x2438)
        self.m.write(self.head.to_bytes(1, "little"))

        size = self.head - self.tail
        if size < 0:
            size += self._PDO_RING_BUF_SIZE

        lock = 0
        self.m.seek(0x2438 + 2)
        self.m.write(lock.to_bytes(1, "little"))
        # print("length",size)
        return size
    def setVoiceAMP(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_VOICE_AMP, id, 0, value)

    def setVoiceTime(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_VOICE_TIME, id, 0, value)

    def setVoiceT(self,  id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_VOICE_T, id, 0, value)


    def setVoiceLight(self, id, value):
        if value > 100:
            value = 100
        self._sendMessage(self._FUNC_WRITE, self._INDEX_VOICE_LIGHT, id, 0, value)

    def setPowerOn(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_CONTROL_WORD, id, 0, 1)
    def setPowerOnPro(self, id, soft_limit, open_loop, with_break, limit_off):
        value = 1
        if soft_limit:
            value |= 0x02
        if open_loop:
            value |= 0x10
        if with_break:
            value |= 0x20
        if limit_off:
            value |= 0x40
        self._sendMessage(self._FUNC_WRITE, self._INDEX_CONTROL_WORD, id, 0, value)
    
    def setPowerOnProBeeS(self, id, limit_soft, limit_off, auto_recovery):
        value = 0x1
        if limit_soft:
            value |= 0x2
        if auto_recovery:
            value |= 0x80
        if limit_off:
            value |= 0x40
        self._sendMessage(self._FUNC_WRITE, self._INDEX_CONTROL_WORD, id, 0, value)
    def setPowerOff(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_CONTROL_WORD, id, 0, 0)

    def setTargetVelocity(self, id, value):
        # Note: Unit: pulse/ms (51200 pulse per round), this unit nearly equals to RPM
        #       and for stepper motors, 0 to 3000 is reasonable, higher speed will lose steps
        self._sendMessage(self._FUNC_WRITE, self._INDEX_TARGET_VELOCITY, id, 0, value)

    def setTargetPosition(self, id, value):
        # Note: Unit pulse, with 50000 pulse per round, and the value in should in range from -2^31 to 2^31
        self._sendMessage(self._FUNC_WRITE, self._INDEX_TARGET_POSITION, id, 0, value)

    def setPWMMode(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_OPERATION_MODE, id, 0, self._OPERATION_MODE_PWM)

    def setVelocityMode(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_OPERATION_MODE, id, 0, self._OPERATION_MODE_PROFILE_VELOCITY)

    def setPositionMode(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_OPERATION_MODE, id, 0, self._OPERATION_MODE_PROFILE_POSITION)

    def setHomingMode(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_OPERATION_MODE, id, 0, self._OPERATION_MODE_HOMING)

    def setSyncInterpolationPositionMode(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_OPERATION_MODE, id, 0,
                          self._OPERATION_SYNC_INTERPOLATION_POSITION)
        
    def setEstopMode(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_OPERATION_MODE, id, 0, self._OPERATION_MODE_ESTOP)

    def setEStopDec(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_ESTOP_DEC, id, 0, value)

    def setCurrentBase(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_CURRENT_BASE, id, 0, value)

    def setCurrentP(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_CURRENT_P, id, 0, value)

    def setCurrentN(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_CURRENT_N, id, 0, value)

    
    def setKeepingCurrent(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_KEEPING_CURRENT, id, 0, value)

    def setRunningCurrent(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_RUNNING_CURRENT, id, 0, value)

    def setKPP(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_KPP, id, 0, value)

    def setKPI(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_KPI, id, 0, value)

    def setKVF(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_KVF, id, 0, value)

    def setKFF(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_KFF, id, 0, value)

    def setTargetCurrent(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_TARGET_CURRENT, id, 0, value)

    def setBoardTypeBLDCS(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_BOARD_TYPE, id, 0, self._BOARD_TYPE_BLDCS_BEE)

    def setPhaseCorrectCurrent(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_PHASE_CORRECT_CURRENT, id, 0, value)

    def setHomingDirection(self, id, value):
        if value == 1:
            self._sendMessage(self._FUNC_WRITE, self._INDEX_HOMING_DIRECTION, id, 0, 1)
        elif value == -1:
            self._sendMessage(self._FUNC_WRITE, self._INDEX_HOMING_DIRECTION, id, 0, -1)
        else:
            print("wrong value, please try 1 or -1.")

    def setHomingLevel(self, id, value):
        if value == 1:
            self._sendMessage(self._FUNC_WRITE, self._INDEX_HOMING_LEVEL, id, 0, 1)
        elif value == 0:
            self._sendMessage(self._FUNC_WRITE, self._INDEX_HOMING_LEVEL, id, 0, 0)
        else:
            print("wrong value, please try 1 or 0.")

    def setAccTime(self, id, value):
        # Note: acc time is a parameter for accelation and deaccelation progress, unit is ms, normally 200ms to 1000ms is reasonable
        self._sendMessage(self._FUNC_WRITE, self._INDEX_ACC_TIME, id, 0, value)

    def setCurrentMax(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_CURRENT_MAX, id, 0, value)

    def setPositionErrorMax(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_POSITION_ERROR_MAX, id, 0, value)

    def setInterpolationPositionMode(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_OPERATION_MODE, id, 0,
                          self._OPERATION_MODE_INTERPOLATION_POSITION)

    def setPowerLimit(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_POWER_LIMIT, id, 0, value)

    def setHomingTriggerLevel(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_HOMING_TRIGGER, id, 0, value)

    # PDO Methods
    def setOutputIOPDO(self, value):
        self._sendMessagePDO(self._FUNC_WRITE, self._INDEX_IO_OUT, value)

    def setAccTimePDO(self, value):
        self._sendMessagePDO(self._FUNC_WRITE, self._INDEX_ACC_TIME, value)

    def setTargetVelocityPDO(self, value):
        self._sendMessagePDO(self._FUNC_WRITE, self._INDEX_TARGET_VELOCITY, value)

    def setTargetPositionPDO(self, value):
        self._sendMessagePDO(self._FUNC_WRITE, self._INDEX_TARGET_POSITION, value)

    def setHomingModePDO(self):
        self._sendMessagePDO(self._FUNC_WRITE, self._INDEX_OPERATION_MODE, self._OPERATION_MODE_HOMING)

    def setPositionModePDO(self):
        self._sendMessagePDO(self._FUNC_WRITE, self._INDEX_OPERATION_MODE, self._OPERATION_MODE_PROFILE_POSITION)

    def setPowerOnPDO(self):
        self._sendMessagePDO(self._FUNC_WRITE, self._INDEX_CONTROL_WORD, 1)

    def setPowerOffPDO(self):
        self._sendMessagePDO(self._FUNC_WRITE, self._INDEX_CONTROL_WORD, 0)

    # End of PDO Methods

    # BDO Methods (Broad Cast Message)
    def setPowerOnBDO(self):
        self._sendMessageBDO(self._INDEX_CONTROL_WORD, 1)

    def setPowerOffBDO(self):
        self._sendMessageBDO(self._INDEX_CONTROL_WORD, 0)

    def setOutputIOBDO(self, value):
        self._sendMessageBDO(self._INDEX_IO_OUT, value)

    # End of BDO Methods

    def getBoardType(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_BOARD_TYPE, id, 0, 0)
        self._delay()
        # if (self._motors[id][0][self._INDEX_BOARD_TYPE] == self._BOARD_TYPE_BLDCS_BEE):
        #     print("Brushless DC Servo Bee")
        # if (self._motors[id][0][self._INDEX_BOARD_TYPE] == self._BOARD_TYPE_BDC_BEE):
        #     print("Brushed DC Bee")
        # if (self._motors[id][0][self._INDEX_BOARD_TYPE] == self._BOARD_TYPE_BDCS_BEE):
        #     print("Brushed DC Servo Bee")
        # if (self._motors[id][0][self._INDEX_BOARD_TYPE] == self._BOARD_TYPE_STEPPER_BEE):
        #     print("Stepper Bee")
        return self._getValue(id, self._INDEX_BOARD_TYPE)
        # return self._motors[id][0][self._INDEX_BOARD_TYPE]

    def getAccTime(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_ACC_TIME, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_ACC_TIME)
        # return self._motors[id][0][self._INDEX_ACC_TIME]

    def getADC(self, channel):
        self._sendMessage(self._FUNC_READ, self._INDEX_ACTUAL_POSITION, 4, channel, 0)
        self._delay()
        return self._motors[4][channel][self._INDEX_ACTUAL_POSITION]

    def setOutputIO(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_IO_OUT, id, 0, value)

    def getHomingLevel(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_HOMING_LEVEL, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_HOMING_LEVEL)
        # return self._motors[id][0][self._INDEX_HOMING_LEVEL]

    def getHomingDirection(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_HOMING_DIRECTION, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_HOMING_DIRECTION)
        # return self._motors[id][0][self._INDEX_HOMING_DIRECTION]

    def getKPP(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_KPP, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_KPP)
        # return self._motors[id][0][self._INDEX_KPP]

    def getKPI(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_KPI, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_KPI)
        # return self._motors[id][0][self._INDEX_KPI]

    def getKPD(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_KPD, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_KPD)
        # return self._motors[id][0][self._INDEX_KPD]

    def getKFF(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_KFF, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_KFF)
        # return self._motors[id][0][self._INDEX_KFF]

    def getEncoderValue(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_ENCODER_VALUE, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_ENCODER_VALUE)
        # return self._motors[id][0][self._INDEX_ENCODER_VALUE]

    def getTargetCurrent(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_TARGET_CURRENT, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_TARGET_CURRENT)
        # return self._motors[id][0][self._INDEX_TARGET_CURRENT]

    def getInputIO(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_IO_INPUT, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_IO_INPUT)
        # return self._motors[id][0][self._INDEX_IO_INPUT]

    def getActualVelocity(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_ACTUAL_VELOCITY, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_ACTUAL_VELOCITY)
        # return self._motors[id][0][self._INDEX_ACTUAL_VELOCITY]

    def getActualPosition(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_ACTUAL_POSITION, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_ACTUAL_POSITION)
        # return self._motors[id][0][self._INDEX_ACTUAL_POSITION]

    def getTargetVelocity(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_TARGET_VELOCITY, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_TARGET_VELOCITY)
        # return self._motors[id][0][self._INDEX_TARGET_VELOCITY]

    def getTargetPosition(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_TARGET_POSITION, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_TARGET_POSITION)
        # return self._motors[id][0][self._INDEX_TARGET_POSITION]

    def getStatus(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_STATUS_WORD, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_STATUS_WORD)

    def getStatusList(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_STATUS_WORD, id, 0, 0)
        self._delay()
        st = self._getValue(id, self._INDEX_STATUS_WORD)
        st_en = 0
        st_reached = 0
        st_iop = 0
        st_ion = 0
        st_opmode = 0
        if st & self._STATUS_DEVICE_ENABLE == self._STATUS_DEVICE_ENABLE:
           st_en = 1 
        if st & self._STATUS_TARGET_REACHED == self._STATUS_TARGET_REACHED:
           st_reached = 1
        if st & self._STATUS_IO_INPUT_LIMIT_P == self._STATUS_IO_INPUT_LIMIT_P:
           st_iop = 1
        if st & self._STATUS_IO_INPUT_LIMIT_N == self._STATUS_IO_INPUT_LIMIT_N:
           st_ion = 1
        if st & self._STATUS_OPMODE_MASK == self._STATUS_OPMODE_PROFILE_POSITION:
           st_opmode = 'Position'
        if st & self._STATUS_OPMODE_MASK == self._STATUS_OPMODE_PROFILE_VELOCITY:
           st_opmode = 'Velocity'
        if st & self._STATUS_OPMODE_MASK == self._STATUS_OPMODE_SENSOR_HOMING:
           st_opmode = 'Homing'
        if st & self._STATUS_OPMODE_MASK == self._STATUS_OPMODE_SENSORLESS_HOMING:
           st_opmode = 'SensorlessHoming'
        if st & self._STATUS_OPMODE_MASK == self._STATUS_OPMODE_ESTOP_PROFILE:
           st_opmode = 'EStop'
        return [st_en, st_reached, st_iop, st_ion, st_opmode]

    def readStatus(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_STATUS_WORD, id, 0, 0)

    def readOpmode(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_OPERATION_MODE, id, 0, 0)

    def readActualPosition(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_ACTUAL_POSITION, id, 0, 0)
    
    def readActualVelocity(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_ACTUAL_VELOCITY, id, 0, 0)
    def readAccTime(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_ACC_TIME, id, 0, 0)
    def setEncoderPolarityP(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_ENCODER_POLARITY, id, 0, 1)

    def setEncoderPolarityN(self, id):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_ENCODER_POLARITY, id, 0, -1)

    def getEncoderPolarity(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_ENCODER_POLARITY, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_ENCODER_POLARITY)
        # return self._motors[id][0][self._INDEX_ENCODER_POLARITY]

    def waitHomingDone(self, id):
        condition = 1
        while condition:
            if (self.getStatus(id) & self._STATUS_TARGET_REACHED) == self._STATUS_TARGET_REACHED:
                condition = 0
            time.sleep(0.1)
    # def waitHomingDone(self, id, timeout):                                                           
    #     for i in range(0, timeout):                                                                  
    #         if (self.getStatus(id) & self._STATUS_TARGET_REACHED) == self._STATUS_TARGET_REACHED:    
    #             return i                                                                             
    #     return timeout 
    def waitTargetPositionReached(self, id):
        condition = 1
        # self._setValue(id, self._INDEX_ACTUAL_VELOCITY, 0)
        # while condition:
        #     st = self.getActualVelocity(id)
        #     if st == 0:
        #         condition = 0
        #     if self._errorFlag == 1:
        #         condition = 0
        while condition:
            if (self.getStatus(id) & self._STATUS_TARGET_REACHED) == self._STATUS_TARGET_REACHED:
                condition = 0
    def waitTargetPositionReachedPro(self, id, timeout):
        condition = 1
        # self._setValue(id, self._INDEX_ACTUAL_VELOCITY, 0)
        # while condition:
        #     st = self.getActualVelocity(id)
        #     if st == 0:
        #         condition = 0
        #     if self._errorFlag == 1:
        #         condition = 0
        t = 0
        while condition:
            t += 1
            if t > timeout:
                condition = 0
            if (self.getStatus(id) & self._STATUS_TARGET_REACHED) == self._STATUS_TARGET_REACHED:
                condition = 0
    def getDeviceID(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_DEVICE_ID, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_DEVICE_ID)

    def _getValue(self, id, index):
        self.m.seek(self._DEVICE_ADDR + id * 32 * 4 + index * 4)
        value = int.from_bytes(self.m.read(4), "little", signed=True)
        # self.m.seek(self._DMA_RX_BUF_ADDR+4)
        # value = int.from_bytes(self.m.read(4), "little", signed=True)
        # print("get value:",value)
        return value

    def _setValue(self, id, index, value):
        self.m.seek(self._DEVICE_ADDR + id * 64 * 4 + index * 4)
        self.m.write(value.to_bytes(4, "little"))

    def getDeviceType(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_BOARD_TYPE, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_BOARD_TYPE)

    def getPhaseCorrectCurrent(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_PHASE_CORRECT_CURRENT, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_PHASE_CORRECT_CURRENT)

    def getEncoderOffset(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_ENCODER_OFFSET, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_ENCODER_OFFSET)

    def getCurrentMax(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_CURRENT_MAX, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_CURRENT_MAX)

    def getPositionErrorMax(self, id):
        self._sendMessage(self._FUNC_READ, self._INDEX_POSITION_ERROR_MAX, id, 0, 0)
        self._delay()
        return self._getValue(id, self._INDEX_POSITION_ERROR_MAX)

    def scanDevices(self):
        online = []
        self.clearOnline()
        print('Searching Online Devices...')
        for i in range(0, 64):
            self._setValue(i, self._INDEX_BOARD_TYPE, 0)
        for i in range(0, 64):
            if self.getDeviceType(i) != 0:
                online.append(i)
        print('Online Devices:')
        print(online)

    def tunePhase(self, id):
        self._sendMessage(self._FUNC_OPERATION, self._OPERATION_INDEX_TUNING, id, 0, 1)

    def saveParameters(self, id):
        self._sendMessage(self._FUNC_OPERATION, self._OPERATION_INDEX_MEMORY, id, 0, 1)

    def changeID(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_DEVICE_ID, id, 0, value)
        self._delay()
        self.saveParameters(value)

    def setPWM(self, id, value):
        self._sendMessage(self._FUNC_WRITE, self._INDEX_TARGET_VELOCITY, id, 0, value)

    def t_hellolib(self):
        self.lib.hello()

    def _link_process(self):
        while self._process_flag:
            ret = 10
            if self._sip_buf_ready_flag > 0:
                if self.lib.pop(
                    self.ndarray_ring_buf.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),
                    self._BUE_SIZE_RING,
                    self.char_array.from_buffer(self._sip_frame_data)
                    ):
                # print(len(self._sip_frame_data))
                    ret = self._sendPDOMsg(self._sip_frame_data)
            
                # print(self._sip_frame_data[0])
                    # print("ret",ret)
                if ret > 8:
                    time.sleep(0.01)
            else:
                time.sleep(0.01)

    def runFile(self,filename):  
        self._sip_buf_ready_flag = 1     
        with open(filename, "r+b") as f:
            fm = mmap.mmap(f.fileno(), 0)
            fm.seek(4)
            timeline = int.from_bytes(fm.read(4), byteorder="little", signed=True)
            readbuf = fm.read(256)
            ret = 0
            counter = 0
            for i in range(0, timeline):
                counter+=1
                fm.seek(256+(0+i)*256)
                readbuf = fm.read(256)
                ret = self._sendPDOMsg(readbuf)
                if ret > 8:
                    time.sleep(0.01)
            fm.close()
        self._sip_buf_ready_flag = 0

    def stop(self):
        self._process_flag = 0
    
    def waitSIP(self, axis_num):
        while True:
            if self.lib.isEmpty(                    
                self.ndarray_ring_buf.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),
                self._BUE_SIZE_RING,axis_num) == 1:
                break
            else:
                time.sleep(0.1)
        self._sip_buf_ready_flag = 0
    
    def setKeyFrame(self, axis_num, key_time, key_position):
        if key_time >= self._BUF_SIZE_INTERPOLATION-1:
            print("axis ",axis_num," too long time:",key_time)
            return 0
        else:
            self.ndarray_key_time[axis_num, self.ndarray_index[axis_num]] = key_time
            self.ndarray_key_value[axis_num, self.ndarray_index[axis_num]] = key_position
            self.ndarray_index[axis_num] += 1    
    
    def processInterpolation(self):
        self.lib.interpolate(
            self.ndarray_key_time.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), 
            self.ndarray_key_value.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), 
            self.ndarray_index.ctypes.data_as(ctypes.POINTER(ctypes.c_float)), 
            self._BUE_SIZE_KEY_FRAME,
            self._BUF_SIZE_INTERPOLATION, 
            self.ndarray_trajectory.ctypes.data_as(ctypes.POINTER(ctypes.c_float)))
        self._sip_buf_ready_flag = 0
        self.lib.append(
            self.ndarray_ring_buf.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),
            self._BUE_SIZE_RING,
            self.ndarray_trajectory.ctypes.data_as(ctypes.POINTER(ctypes.c_float)),
            self._BUF_SIZE_INTERPOLATION)
        # for i in range(0, self._NUM_OF_AXIS):
        #     self.ndarray_index[i] = 0
        self._sip_buf_ready_flag = 1
    
    def getRingBufferLength(self, axis_num):
        return self.lib.bufLength(
            self.ndarray_ring_buf.ctypes.data_as(ctypes.POINTER(ctypes.c_int32)),
            self._BUE_SIZE_RING, axis_num)

    def clearSipFrame(self):
        self.lib.clear(self.char_array.from_buffer(self._sip_frame_data))

    def clearSipFrameAxis(self, axis):
        self.lib.clear(self.char_array.from_buffer(self._sip_frame_data),axis)            
    
    def setSDOMode(self):
        self._sip_buf_ready_flag = 0

    def setPDOMode(self):
        self._sip_buf_ready_flag = 1
    
    # Init Process
    def __init__(self):
        self.head = 0
        self.tail = 0
        self.ll = ctypes.cdll.LoadLibrary   
        self.lib = self.ll("/root/libhello.so")
        self._BUF_SIZE_INTERPOLATION = 1005 # trajectory length
        self._BUE_SIZE_KEY_FRAME = 20
        self._BUE_SIZE_RING = 1005
        self._NUM_OF_AXIS = 32

        self.ndarray_trajectory = np.zeros((self._NUM_OF_AXIS,self._BUF_SIZE_INTERPOLATION), dtype=np.float64)
        self.ndarray_key_time = np.zeros((self._NUM_OF_AXIS,self._BUE_SIZE_KEY_FRAME), dtype=np.float64)
        self.ndarray_key_value = np.zeros((self._NUM_OF_AXIS,self._BUE_SIZE_KEY_FRAME), dtype=np.float64)
        self.ndarray_index = np.zeros(self._NUM_OF_AXIS, dtype = np.int32)
        self.ndarray_ring_buf = np.zeros((self._NUM_OF_AXIS,self._BUE_SIZE_RING), dtype = np.int32)

        for axis in range(0, self._NUM_OF_AXIS):
            self.ndarray_trajectory[axis, self._BUF_SIZE_INTERPOLATION-1] = 0 # trajectory length
            self.ndarray_ring_buf[axis, self._BUE_SIZE_RING-2] = 0 # ring buf head
            self.ndarray_ring_buf[axis, self._BUE_SIZE_RING-1] = 0 # ring buf tail
        
        self._sip_last_position = []
        self._sip_buf_ready_flag = 0
        self._sip_buf = []
        self._sip_prebuf = []
        self._sip_frame_data = bytearray(256)
        self.char_array = ctypes.c_char * 256
        self._array_key_time = []
        self._array_key_position = []
        # self._UdpSharedRamBuf = bytearray(1024)
        for i in range(0, self._NUM_OF_AXIS):
            self._sip_buf.append([])
            self._sip_prebuf.append([])
            self._array_key_time.append([])
            self._array_key_position.append([])
            self._sip_last_position.append(0)
        
        struct.pack_into('B', self._private_msg, 0, *(self._FUNC_CHECK,))
        struct.pack_into('B', self._private_msg, 1, *(0,))
        struct.pack_into('B', self._private_msg, 2, *(0,))
        struct.pack_into('B', self._private_msg, 3, *(0,))
        struct.pack_into('i', self._private_msg, 4, int(*(0,)))

        self.func_code = 0
        self.index = 0
        self.id = 0
        self.subid = 0
        self.data = 0

        self._DRAM_ADDR = 0x41000000
        self._SDO_RING_BUF_SIZE = 128
        self._PDO_RING_BUF_SIZE = 16
        self._DEVICE_ADDR = 0X438
        self._DMA_RX_BUF_ADDR = 0X4000

        self.MAP_MASK = 64 * mmap.PAGESIZE - 1
        self.f = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
        self.m = mmap.mmap(self.f, 64 * mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ,
                           offset=(self._DRAM_ADDR & ~self.MAP_MASK))
        
        self._process_flag = 1
        self._thread1 = threading.Thread(target=self._link_process)
        self._thread1.start()
