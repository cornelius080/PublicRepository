# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 13:33:17 2023
@author: gscalera

Classes that interact with the SimplePYBLE package
"""

from dataclasses import dataclass
import datetime
import simplepyble


@dataclass
class BatteryService:
    uuid: str
    battery_level_uuid: str


@dataclass
class DeviceInfoService:
    uuid: str
    model_uuid: str
    serial_uuid: str
    firmware_uuid: str
    hardware_uuid: str
    manufacturer_uuid: str


@dataclass
class RemotControlService:
    uuid: str
    device_clock_uuid: str
    device_status_uuid: str
    recording_start_uuid: str
    recording_stop_uuid: str
    device_shutdown_uuid: str



class Manufacturer():    
    def __init__(self, Name: str, Identifier: list, Data: list):
        self.name = Name
        self.id = Identifier
        self.data = Data

            
class Service():
    def __init__(self, Uuid: str, Data: str, Characteristics: list):
        self.uuid = Uuid
        self.data = Data
        self.characteristics = Characteristics


class DeviceBLE():    
    # DEVICE INFO
    isConnectable = None
    identifier = None
    address = None
    addressType = None
    power = None
    
    # CONNECTION INFO
    isConnected = False
    
    # MODEL INFO
    modelNumber = None
    serialNumber = None
    hardwareNumber = None
    firmwareNumber = None
    
    # BATTERY 
    batteryLevel = None
            
    # MANUFACTURER INFO
    manufacturer = None
            
    # SERVICES INFO
    services = None
    
    
    def __init__(self, **kwargs):
        super(DeviceBLE, self).__init__(**kwargs)        
        
        
    def UpdateDeviceInfo(self, IsConnectable: bool, Identifier: str, Address: str, AddressType: str, Power: str):
        self.isConnectable = IsConnectable
        self.identifier = Identifier
        self.address = Address
        self.addressType = AddressType
        self.power = Power
        
    
    def UpdateConnectionStatus(self, IsConnected: bool):
        self.isConnected = IsConnected
        

    def UpdateModelInfo(self, ModelNumber: str, SerialNumber: str, HardwareNumber: str, FirmwareNumber: str):
        self.modelNumber = ModelNumber
        self.serialNumber = SerialNumber
        self.hardwareNumber = HardwareNumber
        self.firmwareNumber = FirmwareNumber
        

    def UpdateBatteryLevel(self, BatteryLevel: int):
        self.batteryLevel = BatteryLevel


    def UpdateManufacturerInfo(self, Manufacturer: Manufacturer):
        self.manufacturer = Manufacturer
        
    
    def UpdateServiceInfo(self, Service: Service):
        self.services = Service
                            
        
class RemotBLE(DeviceBLE):
    # TIME 
    time = None
    
    # ERRORS
    isLowBattery = None
    isGpsFault = None 
    isImuFault = None 
    isUsbFault = None
    isSdFault = None
    isGpsBadConfigured = None
    isImuBadConfigured = None
    
    # STATUS
    isGpsConfFileFound = None
    isImuConfFileFound = None
    isBooting = None 
    isPpsWaiting = None
    isPpsAcquired = None
    isReady = None
    isPlugged = None
    isRecording = None
    isInError = None
    isShuttingDown = None
    isFwUpdating = None
    isBleConnected = None
      
    
    def __init__(self, **kwargs):
        super(RemotBLE, self).__init__(**kwargs)
        
        
    def UpdateRemotTime(self, time: datetime):
        self.time = time
        
    
    def UpdateRemotErrors(self, IsLowBattery: bool, IsGpsFault: bool, IsImuFault: bool, IsUsbFault: bool, IsSdFault: bool, IsGpsBadConfigured: bool, IsImuBadConfigured: bool):
        self.isLowBattery = IsLowBattery
        self.isGpsFault = IsGpsFault 
        self.isImuFault = IsImuFault 
        self.isUsbFault = IsUsbFault
        self.isSdFault = IsSdFault
        self.isGpsBadConfigured = IsGpsBadConfigured
        self.isImuBadConfigured = IsImuBadConfigured
        
        
    def UpdateRemotStatus(self, isGpsConfFileFound: bool, isImuConfFileFound: bool, isBooting: bool, isPpsWaiting: bool, isPpsAcquired: bool, isReady: bool, isPlugged: bool, isRecording: bool, isInError: bool, isShuttingDown: bool, isFwUpdating: bool, isBleConnected: bool):
        self.isGpsConfFileFound = isGpsConfFileFound
        self.isImuConfFileFound = isImuConfFileFound
        self.isBooting = isBooting 
        self.isPpsWaiting = isPpsWaiting
        self.isPpsAcquired = isPpsAcquired
        self.isReady = isReady
        self.isPlugged = isPlugged
        self.isRecording = isRecording
        self.isInError = isInError
        self.isShuttingDown = isShuttingDown
        self.isFwUpdating = isFwUpdating
        self.isBleConnected = isBleConnected
           

def ScanForSeconds(Secs: int = 5):
    '''
    Scan for peripherals founding for N seconds

    Parameters
    ----------
    Secs : int
        Duration of scan

    Returns
    -------
    devices : List
        List of found devices BLE

    '''
    __adapter.scan_for(Secs * 1000)    
    global __peripherals
    __peripherals = __adapter.scan_get_results()
    
    # conversion into RemotBLE class
    devices = []
    for peripheral in __peripherals:
        dev = RemotBLE()
        dev.UpdateDeviceInfo(peripheral.is_connectable(), peripheral.identifier(), peripheral.address(), str(peripheral.address_type()), str(peripheral.tx_power()))
        
        devices.append(dev)
    
    return devices
    
  
def SelectDevices(Devices: list, Choices: list):
    '''
    List slicing

    Parameters
    ----------
    Devices : list
        The list of devices
    Choices : list
        The list containing the indices for slicing

    Returns
    -------
    list
        The sliced list.

    '''
    global __peripherals, __selectedPeripherals
    __selectedPeripherals = [__peripherals[choice] for choice in Choices]
    return [Devices[choice] for choice in Choices]


def ConnectDevices(Devices: list):
    '''
    Connects the list of devices passed as argument and update their connection status

    Parameters
    ----------
    Devices : list
        The list of devices to connect.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        dev = Devices[i]
        if peripheral.is_connectable():
            try:
                peripheral.connect()
                if peripheral.is_connected():
                    dev.UpdateConnectionStatus(True)
            except Exception as ex:
                print('\nException during connection')
                print(ex + '\n\n')
                

def DisconnectDevices(Devices: list):
    '''
    Disconnects the list of devices passed as argument and update their connection status

    Parameters
    ----------
    Devices : list
        The list of devices to disconnect.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        dev = Devices[i]
        if peripheral.is_connected():
            dev.UpdateConnectionStatus(False)
            try:
                peripheral.disconnect()
            except Exception as ex:
                print('\nException during disconnection')
                print(ex + '\n\n')
            

    
def ReadModelInfo(Devices: list):
    '''
    Read and update the info (modelNumber, serialNumber, hardwareNumber, firmwareNumber) of the devices 

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        modelNumber = ReadCharacteristicValue(peripheral, __DeviceInfo.uuid, __DeviceInfo.model_uuid).decode("utf-8")
        serialNumber = ReadCharacteristicValue(peripheral, __DeviceInfo.uuid, __DeviceInfo.serial_uuid).decode("utf-8")
        firmwareNumber = ReadCharacteristicValue(peripheral, __DeviceInfo.uuid, __DeviceInfo.firmware_uuid).decode("utf-8")
        hardwareNumber = ReadCharacteristicValue(peripheral, __DeviceInfo.uuid, __DeviceInfo.hardware_uuid).decode("utf-8")
        
        dev = Devices[i]        
        dev.UpdateModelInfo(ModelNumber = str(modelNumber), SerialNumber = str(serialNumber), FirmwareNumber = str(firmwareNumber), HardwareNumber = str(hardwareNumber))


def ReadBatteryLevel(Devices: list):
    '''
    Read and update the battery level of the devices 

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        batteryLevel = ReadCharacteristicValue(peripheral, __BatteryInfo.uuid, __BatteryInfo.battery_level_uuid)
        batteryLevel = int.from_bytes(batteryLevel, byteorder='big')
        
        dev = Devices[i]   
        dev.UpdateBatteryLevel(BatteryLevel = batteryLevel)
  

def ReadManufacturerInfo(Devices: list):
    '''
    Read and update the manufacturer info (name, identifier, data) of the devices 

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        name = ReadCharacteristicValue(peripheral, __DeviceInfo.uuid, __DeviceInfo.manufacturer_uuid).decode("utf-8")
        
        manufacturer_data = peripheral.manufacturer_data()
        ids = []
        data = []
        for manufacturer_id, value in manufacturer_data.items():
            ids.append(str(manufacturer_id.decode("utf-8")))
            data.append(str(value.decode("utf-8")))
            
        man = Manufacturer(Name=str(name), Identifier = ids, Data = data)
        dev = Devices[i]   
        dev.UpdateManufacturerInfo(man)


def ReadServiceInfo(Devices: list):
    '''
    Read and update the service info (uuid, data, characteristic uuid) of the devices 

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        services = peripheral.services()      
        
        myServices = []
        for service in services:
            uuid = str(service.uuid())
            data = str(service.data().decode('utf-8'))
            
            characteristics = []
            for characteristic in service.characteristics():
                characteristics.append(str(characteristic.uuid()))
        
            myServices.append(Service(Uuid = uuid, Data = data, Characteristics = characteristics))            
            
        dev = Devices[i]   
        dev.UpdateServiceInfo(myServices)               


def RemotWriteTime(Devices: list):
    '''
    Set and update the time of the devices 

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''
    now = datetime.datetime.now()
    currentTime = [0, now.year - 2000, now.month, now.day, 0, now.hour, now.minute, now.second]
    content = bytes(currentTime)
    
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        WriteCharacteristicValue(peripheral, __RemotControl.uuid, __RemotControl.device_clock_uuid, content)
        
        dev = Devices[i]   
        dev.UpdateRemotTime(time = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second))
        
        
def RemotReadTime(Devices: list):
    '''
    Get and update the time of the devices 

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):  
        deviceClock = ReadCharacteristicValue(peripheral, __RemotControl.uuid, __RemotControl.device_clock_uuid)
        dClock = deviceClock.hex()
        dClock = [dClock[i:i+2] for i in range(0, len(dClock), 2)] #split every two
        dClock = [int(i, 16) for i in dClock] #converts into list of int
        dClock = datetime.datetime(2000+dClock[1], dClock[2], dClock[3], dClock[5], dClock[6], dClock[7])    
        
        dev = Devices[i]   
        dev.UpdateRemotTime(time = dClock)
    
    
def RemotReadErrors(Devices: list):
    '''
    Read and update the errors (is_Low_Battery, is_Gps_Fault, is_Imu_Fault, is_Usb_Fault, is_Sd_Fault, is_Gps_Bad_Conf, is_Imu_Bad_Conf) of the devices 

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        deviceStatus = ReadCharacteristicValue(peripheral, __RemotControl.uuid, __RemotControl.device_status_uuid)
        
        #bits of error
        is_Low_Battery = ScanAcrossBits(deviceStatus[0], 0)
        is_Gps_Fault = ScanAcrossBits(deviceStatus[0], 1)
        is_Imu_Fault = ScanAcrossBits(deviceStatus[0], 2)
        is_Usb_Fault = ScanAcrossBits(deviceStatus[0], 3)
        is_Sd_Fault = ScanAcrossBits(deviceStatus[0], 4)
        is_Gps_Bad_Conf = ScanAcrossBits(deviceStatus[0], 5)
        is_Imu_Bad_Conf = ScanAcrossBits(deviceStatus[0], 6)
        
        dev = Devices[i]   
        dev.UpdateRemotErrors(IsLowBattery = is_Low_Battery, IsGpsFault = is_Gps_Fault, IsImuFault = is_Imu_Fault, IsUsbFault = is_Usb_Fault, IsSdFault = is_Sd_Fault, IsGpsBadConfigured = is_Gps_Bad_Conf, IsImuBadConfigured = is_Imu_Bad_Conf)
    
    
def RemotReadStatus(Devices: list):
    '''
    Read and update the status (is_Gps_File, is_Imu_File, is_Booting, is_Pps_Waiting, is_Pps_Acquired, is_Ready, is_Plugged, is_Recording, is_In_Error, is_Shutting_Down, is_Fw_Updating, is_Ble_Connected) of the devices 

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        deviceStatus = ReadCharacteristicValue(peripheral, __RemotControl.uuid, __RemotControl.device_status_uuid)
        
        #bits of status
        is_Gps_File = ScanAcrossBits(deviceStatus[2], 3)
        is_Imu_File = ScanAcrossBits(deviceStatus[2], 4)
        is_Booting = ScanAcrossBits(deviceStatus[2], 5)
        is_Pps_Waiting = ScanAcrossBits(deviceStatus[2], 6)
        is_Pps_Acquired = ScanAcrossBits(deviceStatus[2], 7)
        
        is_Ready = ScanAcrossBits(deviceStatus[3], 0)
        is_Plugged = ScanAcrossBits(deviceStatus[3], 1)
        is_Recording = ScanAcrossBits(deviceStatus[3], 2)
        is_In_Error = ScanAcrossBits(deviceStatus[3], 3) 
        is_Shutting_Down = ScanAcrossBits(deviceStatus[3], 4) 
        is_Fw_Updating = ScanAcrossBits(deviceStatus[3], 5) 
        is_Ble_Connected = ScanAcrossBits(deviceStatus[3], 6) 
        
        
        dev = Devices[i]   
        dev.UpdateRemotStatus(isGpsConfFileFound = is_Gps_File, isImuConfFileFound = is_Imu_File, isBooting = is_Booting, isPpsWaiting = is_Pps_Waiting, isPpsAcquired = is_Pps_Acquired, isReady = is_Ready, isPlugged = is_Plugged, isRecording = is_Recording, isInError = is_In_Error, isShuttingDown = is_Shutting_Down, isFwUpdating = is_Fw_Updating, isBleConnected = is_Ble_Connected)
    

def RemotStartRecording(Devices: list, Notes: list):
    '''
    For each device in the list, starts the recording and adds a note in the corresponding logfile

    Parameters
    ----------
    Devices : list
        The list of devices.
    Notes : list
        the list of notes to write in the logfile.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        note = Notes[i] + '\0'
        note = note.encode(encoding="utf-8", errors="strict")
        WriteCharacteristicValue(peripheral, __RemotControl.uuid, __RemotControl.recording_start_uuid, note)
    

def RemotStopRecording(Devices: list):
    '''
    For each device in the list, stops the recording

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''    
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        WriteCharacteristicValue(peripheral, __RemotControl.uuid, __RemotControl.recording_stop_uuid, 'q'.encode(encoding='utf-8', errors='strict'))
        
        
def RemotShutdown(Devices: list):
    '''
    Shutdown each device in the list and update their connection status

    Parameters
    ----------
    Devices : list
        The list of devices.

    Returns
    -------
    '''
    global __selectedPeripherals
    for i, peripheral in enumerate(__selectedPeripherals):
        WriteCharacteristicValue(peripheral, __RemotControl.uuid, __RemotControl.device_shutdown_uuid, 'q'.encode(encoding='utf-8', errors='strict'))
        
        dev = Devices[i]
        dev.UpdateConnectionStatus(False)


def ReadCharacteristicValue(peripheral: simplepyble.Peripheral, service_uuid: str, characteristic_uuid: str):
    '''
    Parameters
    ----------
    peripheral : simplepyble.Peripheral
        A simplepyble peripheral object.
    service_uuid : str
        A string defining the UUID of the service.
    characteristic_uuid : str
        A string defining the UUID of the characteristic.

    Returns
    -------
    Value : Bytes 
        The read value.
    '''
    Value = None
    try:
        Value = peripheral.read(service_uuid, characteristic_uuid)        
        return Value
    except Exception as ex:
        print('\nException during the reading of the characteristic value')
        print(ex + '\n\n')


def WriteCharacteristicValue(peripheral: simplepyble.Peripheral, service_uuid: str, characteristic_uuid: str, content: bytes):
    '''
    Parameters
    ----------
    peripheral : simplepyble.Peripheral
        A simplepyble peripheral object.
    service_uuid : str
        A string defining the UUID of the service.
    characteristic_uuid : str
        A string defining the UUID of the characteristic.
    content : bytes
        The value to write.
    '''
    try:
        peripheral.write_request(service_uuid, characteristic_uuid, content)
    except Exception as ex:
        print('\nException during the writing of a chracteristic value')
        print(ex + '\n\n')


def ScanAcrossBits(singleByte: int, nShifts: int):
    '''   
    Checks if a bit has value 0 or 1. Performs a logic AND between the input byte and a shifted 1.
    Parameters
    ----------
    singleByte : int
        Byte containing the bit to be checked.
    nShifts : int
        Number of shifts to be performed. Corresponds to the position that the bit has into the byte (right-to-left). E.g. Bit 2 has index 2 into the byte, so nShifts is 2.

    Returns
    -------
    Returns TRUE if the logic AND has value 1, or FALSE if has value 0.

    '''
    
    mask = 1 << nShifts
    bit = singleByte & mask
    if bit != 0:
        return True
    else: 
        return False


# %% VARIABLES DEFINITION (PRIVATE SCOPE)
__BatteryInfo = BatteryService(
    uuid = '0000180f-0000-1000-8000-00805f9b34fb', 
    battery_level_uuid = '00002a19-0000-1000-8000-00805f9b34fb')

__DeviceInfo = DeviceInfoService(
    uuid = '0000180a-0000-1000-8000-00805f9b34fb', 
    model_uuid = '00002a24-0000-1000-8000-00805f9b34fb',
    serial_uuid = '00002a25-0000-1000-8000-00805f9b34fb',
    firmware_uuid = '00002a26-0000-1000-8000-00805f9b34fb',
    hardware_uuid = '00002a27-0000-1000-8000-00805f9b34fb',
    manufacturer_uuid = '00002a29-0000-1000-8000-00805f9b34fb')

__RemotControl = RemotControlService(
    uuid = '0000fe40-cc7a-482a-984a-7f2ed5b3e58f', 
    device_clock_uuid = '0000fe41-8e22-4541-9d4c-21edae82ed19',
    device_status_uuid = '0000fe42-8e22-4541-9d4c-21edae82ed19',
    recording_start_uuid = '0000fe43-8e22-4541-9d4c-21edae82ed19',
    recording_stop_uuid = '0000fe44-8e22-4541-9d4c-21edae82ed19',
    device_shutdown_uuid = '0000fe45-8e22-4541-9d4c-21edae82ed19')

__adapters = simplepyble.Adapter.get_adapters() # list of found adapters

__adapter = __adapters[0] # default adapter is the first

global __peripherals # list of peripherals: populated during scan
__peripherals = []

global __selectedPeripherals # list of selected peripherals: populated during device selection
__selectedPeripherals = []






























