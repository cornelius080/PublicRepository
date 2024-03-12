# -*- coding: utf-8 -*-
"""
https://www.w3.org/TR/SVG11/types.html#ColorKeywords

Created on Wed Mar 29 15:09:27 2023
@author: gscalera
"""
# %% IMPORTS
import datetime

from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp

from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.tab import MDTabsBase



# %% LOAD STRING
Builder.load_string(
    """ 
<MyLabelField@MDLabel>:
    font_style: 'H6'
    
<MyLabelValue@MDLabel>:
    halign: 'center'
    
<MyCheckbox@MDCheckbox>:
    active: True
    disabled: True
    disabled_color: [1, 1, 1, 1]
       
<MyGridLayout@MDGridLayout>:
    #md_bg_color: 0.4, 0.6, 0.5, 0.9
    padding: dp(100), dp(20), dp(100), 0   
    size_hint_y: None
    height: self.minimum_height
    row_force_default: True
    row_default_height: dp(50)
        
<ViewInfo>:
    screen_manager: screen_manager
    tabs: tabs
    
    MDAnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'   
        MDBoxLayout:
            size_hint: 1, 0.2
            orientation: 'vertical'
            #md_bg_color: 0.1, 0.8, 0.4, 0.6
            MDTabs:
                id: tabs
                on_tab_switch: root.Tab_Switch(*args)
            MDRelativeLayout:
                padding: dp(10), dp(0), dp(10), dp(0)
                MDDropDownItem:
                    id: ddi_device_info
                    size_hint_x: None
                    width: dp(100)
                    pos_hint: {"right": 1, "center_y": 0.5}  
                    on_release: root.menu_device_info.open()
                    select: root.Ddi_Selection_Changed(self.current_item)
                    text: 'SELECT DEVICE'
    
    
    MDAnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'   
        MDScreenManager:
            size_hint: 1, 0.8
            id: screen_manager  
            
            Screen:
                name: 'screen_general'
                MDScrollView:
                    MyGridLayout:
                        rows: 6
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'MANUFACTURER'
                            MyLabelValue: 
                                id: Label_manufacturer
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'ID'
                            MyLabelValue: 
                                id: Label_id
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'ADDRESS'
                            MyLabelValue: 
                                id: Label_address
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'ADDRESS_TYPE'
                            MyLabelValue: 
                                id: Label_address_type
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'POWER'
                            MyLabelValue: 
                                id: Label_power
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'BATTERY'
                            MyLabelValue: 
                                id: Label_battery
            
            Screen:
                name: 'screen_model'
                MDScrollView:
                    MyGridLayout:
                        rows: 4
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'MODEL'
                            MyLabelValue: 
                                id: Label_model                                
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'SERIAL'
                            MyLabelValue: 
                                id: Label_serial                                
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'HARDWARE'
                            MyLabelValue: 
                                id: Label_hardware                                
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'FIRMWARE'
                            MyLabelValue: 
                                id: Label_firmware 
                                
            Screen:
                name: 'screen_status'
                MDScrollView:
                    MyGridLayout:
                        rows: 12
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'READY'
                            MyCheckbox:
                                id: Checkbox_ready
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'ERROR'
                            MyCheckbox:
                                id: Checkbox_error
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'GPS FILE FOUND'
                            MyCheckbox:
                                id: Checkbox_gps_file_found
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'IMU FILE FOUND'
                            MyCheckbox:
                                id: Checkbox_imu_file_found
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'PPS WAITING'
                            MyCheckbox:
                                id: Checkbox_pps_waiting
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'PPS ACQUIRED'
                            MyCheckbox:
                                id: Checkbox_pps_acquired
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'BOOTING'
                            MyCheckbox:
                                id: Checkbox_booting
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'FIRMWARE UPDATING'
                            MyCheckbox:
                                id: Checkbox_firmware_updating
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'RECORDING'
                            MyCheckbox:
                                id: Checkbox_recording
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'SHUTTING DOWN'
                            MyCheckbox:
                                id: Checkbox_shutting_down
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'PLUGGED'
                            MyCheckbox:
                                id: Checkbox_plugged
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'BLE CONNECTED'
                            MyCheckbox:
                                id: Checkbox_ble_connected
                        
            Screen:
                name: 'screen_errors'
                MDScrollView:
                    MyGridLayout:
                        rows: 7
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'LOW BATTERY'
                            MyCheckbox:
                                id: Checkbox_low_battery
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'GPS FAULT'
                            MyCheckbox:
                                id: Checkbox_gps_fault
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'IMU FAULT'
                            MyCheckbox:
                                id: Checkbox_imu_fault
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'GPS BAD CONFIGURED'
                            MyCheckbox:
                                id: Checkbox_gps_bad_configured
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'IMU BAD CONFIGURED'
                            MyCheckbox:
                                id: Checkbox_imu_bad_configured
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'USB FAULT'
                            MyCheckbox:
                                id: Checkbox_usb_fault
                        MDBoxLayout:
                            MyLabelField: 
                                text: 'SD FAULT'
                            MyCheckbox:
                                id: Checkbox_sd_fault

    
    MDFloatLayout:
        MDFloatingActionButton:
            icon: "arrow-left"
            md_bg_color: app.theme_cls.primary_color
            pos_hint: {"x": 0.01, "y": 0.01}
            on_release: root.Switch_To_View()
            

<View>:
    MDRelativeLayout:
        MDIconButton:
            icon: "information"
            icon_size: dp(40)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_release: root.Switch_To_ViewInfo()
"""
)

    
class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    
    
class ViewInfo(MDScreen):
    screen_manager: MDScreenManager
    tabs: Tab
        
        
    def __init__(self, **kwargs):
        super(ViewInfo, self).__init__(**kwargs)   
                
    
    def DefineParameters(self, tabsLabels: list, devices: list):
        self.tabsTitles = tabsLabels
        self.devices = devices
        
        # create labels for ddi
        self.ddiLabels = []
        for dev in devices:
            self.ddiLabels.append(dev.identifier)
        
        self.Tab_Start()
        self.Ddi_Start()
        
        
    
    def Tab_Start(self):
        for label in self.tabsTitles:
            self.ids.tabs.add_widget(Tab(title=label))
    
    
    def Tab_Switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        if tab_text == self.tabsTitles[0]:
            self.screen_manager.current = 'screen_general'
        elif tab_text == self.tabsTitles[1]:
            self.screen_manager.current = 'screen_model'
        elif tab_text == self.tabsTitles[2]:
            self.screen_manager.current = 'screen_status'
        elif tab_text == self.tabsTitles[3]:
            self.screen_manager.current = 'screen_errors'
        
    
    def Ddi_Start(self):    
        self.menu_device_info, device_info_items = self.Create_DropDown_Widget(self.ids.ddi_device_info, self.ddiLabels, width=5)
        
    
    def Ddi_Selection_Changed(self, current_item):   
        green = "limegreen"
        red = "red"
        grey = "darkgrey"
        
        if len(current_item)>0:   
            current_index = self.ddiLabels.index(current_item)
        
            dev = self.devices[current_index]
            
            # UPDATE SCREEN 'GENERAL'
            self.ids.Label_manufacturer.text = str(dev.manufacturerName)
            self.ids.Label_id.text = str(dev.identifier)
            self.ids.Label_address.text = str(dev.address)
            self.ids.Label_address_type.text = str(dev.addressType)
            self.ids.Label_power.text = str(dev.power)
            self.ids.Label_battery.text = (dev.batteryLevel)
            
            # UPDATE SCREEN 'MODEL'
            self.ids.Label_model.text = str(dev.modelNumber)
            self.ids.Label_serial.text = str(dev.serialNumber)
            self.ids.Label_hardware.text = str(dev.hardwareNumber)
            self.ids.Label_firmware.text = str(dev.firmwareNumber)
            
            # UPDATE SCREEN 'STATUS'
            if dev.isReady == True:
                self.ids.Checkbox_ready.disabled_color = green
            else:
                self.ids.Checkbox_ready.disabled_color = grey
            
            if dev.isInError == True:
                self.ids.Checkbox_error.disabled_color = grey
            else:
                self.ids.Checkbox_error.disabled_color = green
            
            if dev.isGpsConfFileFound == True:
                self.ids.Checkbox_gps_file_found.disabled_color = green
            else:
                self.ids.Checkbox_gps_file_found.disabled_color = grey
                
            if dev.isImuConfFileFound == True:
                self.ids.Checkbox_imu_file_found.disabled_color = green
            else:
                self.ids.Checkbox_imu_file_found.disabled_color = grey
            
            if dev.isPpsWaiting == True:
                self.ids.Checkbox_pps_waiting.disabled_color = grey
            else:
                self.ids.Checkbox_pps_waiting.disabled_color = green
            
            if dev.isPpsAcquired == True:
                self.ids.Checkbox_pps_acquired.disabled_color = green
            else:
                self.ids.Checkbox_pps_acquired.disabled_color = grey
            
            if dev.isBooting == True:
                self.ids.Checkbox_booting.disabled_color = grey
            else:
                self.ids.Checkbox_booting.disabled_color = green
                
            if dev.isFwUpdating == True:
                self.ids.Checkbox_firmware_updating.disabled_color = grey
            else:
                self.ids.Checkbox_firmware_updating.disabled_color = green
            
            if dev.isRecording == True:
                self.ids.Checkbox_recording.disabled_color = green
            else:
                self.ids.Checkbox_recording.disabled_color = grey  
                
            if dev.isShuttingDown == True:
                self.ids.Checkbox_shutting_down.disabled_color = grey
            else:
                self.ids.Checkbox_shutting_down.disabled_color = green
            
            if dev.isPlugged == True:
                self.ids.Checkbox_plugged.disabled_color = grey
            else:
                self.ids.Checkbox_plugged.disabled_color = green
            
            if dev.isBleConnected == True:
                self.ids.Checkbox_ble_connected.disabled_color = green
            else:
                self.ids.Checkbox_ble_connected.disabled_color = grey
                        
            # UPDATE SCREEN 'ERRORS'
            if dev.isLowBattery == True:
                self.ids.Checkbox_low_battery.disabled_color = red
            else:
                self.ids.Checkbox_low_battery.disabled_color = green
            
            if dev.isGpsFault == True:
                self.ids.Checkbox_gps_fault.disabled_color = red
            else:
                self.ids.Checkbox_gps_fault.disabled_color = green
                
            if dev.isImuFault == True:
                self.ids.Checkbox_imu_fault.disabled_color = red
            else:
                self.ids.Checkbox_imu_fault.disabled_color = green
            
            if dev.isGpsBadConfigured == True:
                self.ids.Checkbox_gps_bad_configured.disabled_color = red
            else:
                self.ids.Checkbox_gps_bad_configured.disabled_color = green
            
            if dev.isImuBadConfigured == True:
                self.ids.Checkbox_imu_bad_configured.disabled_color = red
            else:
                self.ids.Checkbox_imu_bad_configured.disabled_color = green
                
            if dev.isUsbFault == True:
                self.ids.Checkbox_usb_fault.disabled_color = red
            else:
                self.ids.Checkbox_usb_fault.disabled_color = green
            
            if dev.isSdFault == True:
                self.ids.Checkbox_sd_fault.disabled_color = red
            else:
                self.ids.Checkbox_sd_fault.disabled_color = green
                       
    
    def Create_DropDown_Widget(self, drop_down_item, item_list, width):
        items_collection = [
            {
                "viewclass": "OneLineListItem",
                "text": item_list[i],
                "height": dp(56),
                "on_release": lambda x = item_list[i]: self.Set_DropDown_Item(drop_down_item, menu, x),
            } for i in range(len(item_list))
        ]
        
        menu = MDDropdownMenu(caller=drop_down_item, items=items_collection, width_mult=width)
        menu.bind()
        
        return menu, items_collection

         
    def Set_DropDown_Item(self, drop_down_item, menu, text_item):
        drop_down_item.set_item(text_item)
        menu.dismiss()
        
        
    def Switch_To_View(self):
        # REMOVE LABELS FROM TAB OBJECT
        self.ids.tabs.ids.layout.clear_widgets()
        
        # RESET TEXT FROM LABELS
        self.ResetLabel(self.ids.Label_manufacturer)
        self.ResetLabel(self.ids.Label_id)
        self.ResetLabel(self.ids.Label_address)
        self.ResetLabel(self.ids.Label_address_type)
        self.ResetLabel(self.ids.Label_power)
        self.ResetLabel(self.ids.Label_battery)
        
        self.ResetLabel(self.ids.Label_model)
        self.ResetLabel(self.ids.Label_serial)
        self.ResetLabel(self.ids.Label_hardware)
        self.ResetLabel(self.ids.Label_firmware)
        
        # RESET CHECKBOX STATUS
        self.ResetCheckbox(self.ids.Checkbox_ready)
        self.ResetCheckbox(self.ids.Checkbox_error)
        self.ResetCheckbox(self.ids.Checkbox_gps_file_found)
        self.ResetCheckbox(self.ids.Checkbox_imu_file_found)
        self.ResetCheckbox(self.ids.Checkbox_pps_waiting)
        self.ResetCheckbox(self.ids.Checkbox_pps_acquired)
        self.ResetCheckbox(self.ids.Checkbox_booting)
        self.ResetCheckbox(self.ids.Checkbox_firmware_updating)
        self.ResetCheckbox(self.ids.Checkbox_recording)        
        self.ResetCheckbox(self.ids.Checkbox_shutting_down)
        self.ResetCheckbox(self.ids.Checkbox_plugged)
        self.ResetCheckbox(self.ids.Checkbox_ble_connected)
        
        self.ResetCheckbox(self.ids.Checkbox_low_battery)
        self.ResetCheckbox(self.ids.Checkbox_gps_fault)
        self.ResetCheckbox(self.ids.Checkbox_imu_fault)
        self.ResetCheckbox(self.ids.Checkbox_gps_bad_configured)
        self.ResetCheckbox(self.ids.Checkbox_imu_bad_configured)
        self.ResetCheckbox(self.ids.Checkbox_usb_fault)
        self.ResetCheckbox(self.ids.Checkbox_sd_fault)
        
        
        MDApp.get_running_app().sm.current = 'View'
        
    
    def ResetLabel(self, label):
        label.text = ''
        
        
    def ResetCheckbox(self, checkbox):
        checkbox.disabled_color = [1, 1, 1, 1]
    
   
class View(MDScreen):
    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)
                
        
    def DefineParametersForViewinfo(self):
        tabsLabels = ['GENERAL', 'MODEL', 'STATUS', 'ERRORS']
        
        # create fake devices
        remot0 = RemotBLE(clock=datetime.datetime.now(), isLowBattery=False, isGpsFault=False, isImuFault=False, isUsbFault=False, isSdFault=False, isGpsBadConfigured=True, isImuBadConfigured=True, isGpsConfFileFound=True, isImuConfFileFound=True, isBooting=False, isPpsWaiting=False, isPpsAcquired=True, isReady=True, isPlugged=False, isRecording=False, isInError=False, isShuttingDown=False, isFwUpdating=False, isBleConnected=True)       
                
        remot0.ConfigureGeneralProperties(manufacturerName='Stonex', identifier='DEV_0', add='[00:11]', addType='PUBLIC', power='32678', battery='87', model='REMOT2', serial='SERIAL_0', hardware='HARD_0', firmware='FIRM_0')
                
                
        remot1 = RemotBLE(clock=datetime.datetime.now(), isLowBattery=True, isGpsFault=False, isImuFault=True, isUsbFault=True, isSdFault=True, isGpsBadConfigured=False, isImuBadConfigured=True, isGpsConfFileFound=True, isImuConfFileFound=True, isBooting=True, isPpsWaiting=True, isPpsAcquired=True, isReady=True, isPlugged=False, isRecording=True, isInError=False, isShuttingDown=False, isFwUpdating=False, isBleConnected=False) 
                
        remot1.ConfigureGeneralProperties(manufacturerName='Stonex', identifier='DEV_1', add='[11:22]', addType='PUBLIC', power='33678', battery='78', model='REMOT2', serial='SERIAL_1', hardware='HARD_1', firmware='FIRM_1')                           
                

        remot2 = RemotBLE(clock=datetime.datetime.now(), isLowBattery=False, isGpsFault=False, isImuFault=True, isUsbFault=False, isSdFault=True, isGpsBadConfigured=False, isImuBadConfigured=True, isGpsConfFileFound=True, isImuConfFileFound=True, isBooting=False, isPpsWaiting=True, isPpsAcquired=True, isReady=True, isPlugged=False, isRecording=True, isInError=False, isShuttingDown=False, isFwUpdating=True, isBleConnected=False) 
                
        remot2.ConfigureGeneralProperties(manufacturerName='Stonex', identifier='DEV_2', add='[22:33]', addType='RANDOM', power='32478', battery='69', model='REMOT2', serial='SERIAL_2', hardware='HARD_2', firmware='FIRM_2')
        
        
        # PASS THE PARAMETERS TO THE SCREEN
        viewInfo = self.manager.get_screen('ViewInfo')
        viewInfo.DefineParameters(tabsLabels = tabsLabels, devices = [remot0, remot1, remot2])
        
        
        
    def Switch_To_ViewInfo(self):
        self.DefineParametersForViewinfo()
        MDApp.get_running_app().sm.current = 'ViewInfo'
        
        
class DeviceBLE():    
    manufacturerName = ''
    
    # DEVICE INFO
    identifier = ''
    address = ''
    addressType = ''
    power = ''
    
    # BATTERY 
    batteryLevel = None
    
    # MODEL INFO
    modelNumber = ''
    serialNumber = ''
    hardwareNumber = ''
    firmwareNumber = ''
    
    
    def __init__(self, manufacturerName: str, identifier: str, add: str, addType: str, power: str, battery: int, model: str, serial: str, hardware: str, firmware: str):
        
        # MANUFACTURER
        self.manufacturerName = manufacturerName
        
        # DEVICE INFO
        self.identifier = identifier
        self.address = add
        self.addressType = addType
        self.power = power
        
        # BATTERY 
        self.batteryLevel = battery
        
        # MODEL INFO
        self.modelNumber = model
        self.serialNumber = serial
        self.hardwareNumber = hardware
        self.firmwareNumber = firmware
  
        
class RemotBLE(DeviceBLE):
    def __init__(self, clock: datetime, isLowBattery: bool, isGpsFault: bool, isImuFault: bool, isUsbFault: bool, isSdFault: bool, isGpsBadConfigured: bool, isImuBadConfigured: bool, isGpsConfFileFound: bool, isImuConfFileFound: bool, isBooting: bool, isPpsWaiting: bool, isPpsAcquired: bool, isReady: bool, isPlugged: bool, isRecording: bool, isInError: bool, isShuttingDown: bool, isFwUpdating: bool, isBleConnected: bool):
        # TIME 
        self.clock = clock
        
        # ERRORS
        self.isLowBattery = isLowBattery
        self.isGpsFault = isGpsFault 
        self.isImuFault = isImuFault 
        self.isUsbFault = isUsbFault
        self.isSdFault = isSdFault
        self.isGpsBadConfigured = isGpsBadConfigured
        self.isImuBadConfigured = isImuBadConfigured
        
        # STATUS
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
        
        
    def ConfigureGeneralProperties(self, manufacturerName: str, identifier: str, add: str, addType: str, power: str, battery: int, model: str, serial: str, hardware: str, firmware: str):
        
        # MANUFACTURER
        self.manufacturerName = manufacturerName
        
        # DEVICE INFO
        self.identifier = identifier
        self.address = add
        self.addressType = addType
        self.power = power
        
        # BATTERY 
        self.batteryLevel = battery
        
        # MODEL INFO
        self.modelNumber = model
        self.serialNumber = serial
        self.hardwareNumber = hardware
        self.firmwareNumber = firmware
        
        
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = MDScreenManager()
        self.sm.add_widget(View(name="View"))
        self.sm.add_widget(ViewInfo(name="ViewInfo"))       
        

    def build(self):
        self.title = 'DEVICE INFO APP'
        return self.sm
    

if __name__ == '__main__':
    MainApp().run()
    
    
    
    
    
    
    
    
    
    
    