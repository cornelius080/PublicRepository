# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 21:42:26 2022
@author: gscalera

https://base.xsens.com/s/article/How-to-use-Device-Data-View-to-learn-MT-Low-Level-Communications?language=en_US
"""

from enum import Enum
        

class DataPrecision(Enum):
    FLOAT32 = 0
    FP1220 = 1
    FP1632 = 2
    FLOAT64 = 3


class CoordinateSystem(Enum):
    ENU = 0
    NED = 4
    NWU = 8
    
    
class FilterProfile(Enum):
    GENERAL = hex(11)[2:].zfill(2).upper()
    GENERAL_NO_BARO = hex(12)[2:].zfill(2).upper()
    GENERAL_MAG = hex(13)[2:].zfill(2).upper()  
    
            
class Xsens_DataMessage():
    PREAMBLE = 'FA'
    BID = 'FF'
    MID = ''
    LEN = ''
    DATA = ''
    CHECKSUM = ''
    
    
    def CalcDataLen(self, hexMessage):
        # count the number spaces between each value and increment its value by one. The result is converted into hexadecimal
        return hex(1 + hexMessage.count(' '))[2:].zfill(2).upper()
        
        
    def CalcChecksum(self, hexMessage):
        hex_data = hexMessage.replace(" ", "")
        checksum = 0

        for i in range(2,len(hex_data),2):
            hexVal = hex_data[i:i+2]
            # cast to integer
            intVal = int(hexVal,16)
            checksum -= intVal
            # get lower 8bits
            checksum &= 0xff
        return hex(checksum)[2:].upper()



class SetOutputConfiguration(Xsens_DataMessage):
    MID = 'C0'   
    MSG = ''
    
    suffix = '' #represents the OR logic between the coordinate system and the data precision
    sampleRate = ''
    sampleRateHR = ''
    
    # ACCELERATION
    msg_acc = '40 2'
    msg_accFree = '40 3'
    msg_accHR = '40 4'
    
    # ANGULAR VELOCITY
    msg_angVel = '80 2'
    msg_angVelHR = '80 4'
    
    # MAGNETIC FIELD
    msg_magField = 'C0 2'
    
    # ORIENTATION
    msg_quaternion = '20 1'
    msg_rotationMatrix = '20 2'
    msg_eulerAngles = '20 3'
    
    # TIMESTAMP
    msg_utc = '10 10'
    msg_packetCounter = '10 20'
    msg_sampleTimeFine = '10 60'
    
    # TEMPERATURE
    msg_temperature = '08 1'
    
    # PRESSURE
    msg_pressure = '30 1' 
         
    
    def __init__(self, coordinateSystem, dataPrecision, samplingFrequency, samplingFrequencyHR):
        self.suffix = str(coordinateSystem | dataPrecision)
        
        self.sampleRate = hex(samplingFrequency)[2:].zfill(4)
        self.sampleRate = ' '.join(self.sampleRate[i:i+2] for i in range(0, len(self.sampleRate), 2))
        
        self.sampleRateHR = hex(samplingFrequencyHR)[2:].zfill(4)
        self.sampleRateHR = ' '.join(self.sampleRateHR[i:i+2] for i in range(0, len(self.sampleRateHR), 2))
        
    
    def ComposeMessage(self, isAcc, isFreeAcc, isAccHR, isGyro, isGyroHR, isMag, isQuat, isRotMat, isEuler, isUtc, isPacketCounter, isSampleTimeFine, isTemperature, isPressure):
        # ACCELERATION
        if isAcc:
            self.DATA = self.DATA + ' ' + self.msg_acc + self.suffix + ' ' + self.sampleRate
        if isFreeAcc:
            self.DATA = self.DATA + ' ' + self.msg_accFree + self.suffix + ' ' + self.sampleRate
        if isAccHR:
            self.DATA = self.DATA + ' ' + self.msg_accHR + self.suffix + ' ' + self.sampleRateHR
            
            
        # ANGULAR VELOCITY
        if isGyro:
            self.DATA = self.DATA + ' ' + self.msg_angVel + self.suffix + ' ' + self.sampleRate
        if isGyroHR:
            self.DATA = self.DATA + ' ' + self.msg_angVelHR + self.suffix + ' ' + self.sampleRateHR
            
            
        # MAGNETIC FIELD
        if isMag:
            self.DATA = self.DATA + ' ' + self.msg_magField + self.suffix + ' ' + self.sampleRate
            
            
        # ORIENTATION
        if isQuat:
            self.DATA = self.DATA + ' ' + self.msg_quaternion + self.suffix + ' ' + self.sampleRate
        if isRotMat:
            self.DATA = self.DATA + ' ' + self.msg_rotationMatrix + self.suffix + ' ' + self.sampleRate
        if isEuler:
            self.DATA = self.DATA + ' ' + self.msg_eulerAngles + self.suffix + ' ' + self.sampleRate
            
            
        # TIMESTAMP
        if isUtc:
            self.DATA = self.DATA + ' ' + self.msg_utc + ' FF FF'
        if isPacketCounter:
            self.DATA = self.DATA + ' ' + self.msg_packetCounter + ' FF FF'
        if isSampleTimeFine:
            self.DATA = self.DATA + ' ' + self.msg_sampleTimeFine + ' FF FF'
        
        
        # TEMPERATURE
        if isTemperature:
            self.DATA = self.DATA + ' ' + self.msg_temperature + self.suffix + ' ' + self.sampleRate
            
        # PRESSURE
        if isPressure:
            self.DATA = self.DATA + ' ' + self.msg_pressure + self.suffix + ' 00 32' #impostato alla massima frequenza (50Hz)
        
        
        if self.DATA[0] == ' ':
            self.DATA = self.DATA[1:]
        
        
        self.LEN = self.CalcDataLen(self.DATA)
        if self.DATA[0] == ' ':
            self.MSG = self.PREAMBLE + ' ' + self.BID + ' ' + self.MID + ' ' + self.LEN + self.DATA
        else:
            self.MSG = self.PREAMBLE + ' ' + self.BID + ' ' + self.MID + ' ' + self.LEN + ' ' + self.DATA
            
        self.CHECKSUM = self.CalcChecksum(self.MSG)
        self.MSG = self.MSG + ' ' + self.CHECKSUM
    


class SetFilterProfile(Xsens_DataMessage):
    MID = '64'
    #LEN = '02'
    MSG = ''
    filterProf = ''
    
    def __init__(self, filterProfile):
        self.filterProf = str(filterProfile)
    
    
    def ComposeMessage(self):
        self.DATA = '00 ' + self.filterProf
        self.LEN = self.CalcDataLen(self.DATA)
        self.MSG = self.PREAMBLE + ' ' + self.BID + ' ' + self.MID + ' ' + self.LEN + ' ' + self.DATA
        self.CHECKSUM = self.CalcChecksum(self.MSG)
        self.MSG = self.MSG + ' ' + self.CHECKSUM
        


class SetConfigurationParameters():
    coordinate_System = None
    data_Precision = None
    sampling_Frequency = None
    sampling_FrequencyHR = None
    filter_Settings = None
    
    def __init__(self, coordinateSystem, dataPrecision, samplingFrequency, samplingFrequencyHR, filterSettings):
            if str(coordinateSystem).lower() == 'ned':
                self.coordinate_System = CoordinateSystem.NED.value
            elif str(coordinateSystem).lower() == 'enu':
                self.coordinate_System = CoordinateSystem.ENU.value
            elif str(coordinateSystem).lower() == 'nwu':
                self.coordinate_System = CoordinateSystem.NWU.value
            
            if str(dataPrecision).lower() == 'float 64-bit':
                self.data_Precision = DataPrecision.FLOAT64.value
            elif str(dataPrecision).lower() == 'float 32-bit':
                self.data_Precision = DataPrecision.FLOAT32.value
            elif str(dataPrecision).lower() == 'fp 12.20':
                self.data_Precision = DataPrecision.FP1220.value
            elif str(dataPrecision).lower() == 'fp 16.32':
                self.data_Precision = DataPrecision.FP1632.value
                
            if str(filterSettings).lower() == 'general':
                self.filter_Settings = FilterProfile.GENERAL.value
            elif str(filterSettings).lower() == 'general_mag':
                self.filter_Settings = FilterProfile.GENERAL_MAG.value
            elif str(filterSettings).lower() == 'general_no_baro':
                self.filter_Settings = FilterProfile.GENERAL_NO_BARO.value
            
            self.sampling_Frequency = int(samplingFrequency[:-3])
            self.sampling_FrequencyHR = int(samplingFrequencyHR[:-3])
































