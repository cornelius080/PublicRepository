# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 14:40:57 2023
@author: gscalera

"""
import os, numpy as np
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.widget import MDWidget
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty, ObjectProperty
from kivy.metrics import dp

import MTi_LowLevelProtocol as Model



kv = Builder.load_string('''
<MyBoxLayout@MDBoxLayout>:
    size_hint_y: None
    height: dp(75)
                         
<MyLabel@MDLabel>:
    size_hint_y: None
    height: dp(50)
              
<MySwitch@MDSwitch>:
    width: dp(64)
    pos_hint: {'center_x': .5, 'center_y': .5}                    
   
                      
<View>:
    screen_manager: screen_manager
    _tabs: _tabs
    
    MDAnchorLayout:
        anchor_x: 'center'
        anchor_y: 'top'   
        MDBoxLayout:
            size_hint: 1, 0.2
            MDTabs:
                id: _tabs
                on_tab_switch: root.on_tab_switch(*args)
    
    
    MDAnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        MDScreenManager:
            size_hint: 1, 0.7
            id: screen_manager  
            Screen:
                name: 'screen_timestamp'
                MDGridLayout:
                    rows: 3
                    padding: 50, 0, 50, 0
                                    
                    MyBoxLayout:
                        MDLabel:
                            text: 'PACKET COUNTER'
                        MySwitch:
                            id: switch_packet_counter 
                            active: False
                    
                    MyBoxLayout:  
                        MDLabel:
                            text: 'SAMPLE TIME FINE'
                        MySwitch:
                            id: switch_sample_time 
                            active: False
                    
                    MyBoxLayout: 
                        MDLabel:
                            text: 'UTC' 
                        MySwitch:
                            id: switch_utc
                            active: True
                
                           
            Screen:
                name: 'screen_data'
                MDGridLayout:
                    rows: 6
                    padding: 50, 0, 50, 0
                    
                    MyBoxLayout:
                        MDLabel:
                            text: 'RATE OF TURN'  
                        MySwitch:
                            id: switch_rate_turn
                            active: True
                    
                    MyBoxLayout:
                        MDLabel:
                            text: 'ACCELERATION'  
                        MySwitch:
                            id: switch_acceleration
                            active: True
                            
                    MyBoxLayout:
                        MDLabel:
                            text: 'FREE ACCELERATION'   
                        MySwitch:
                            id: switch_free_acceleration
                            active: False
                        
                    MyBoxLayout:
                        MDLabel:
                            text: 'MAGNETIC FIELD'
                        MySwitch:
                            id: switch_magnetic_field
                            active: True
                    
                    MyBoxLayout:
                        spacing: dp(50)
                        MDLabel:
                            text: 'RATE OF TURN HR'
                        MDDropDownItem:
                            id: ddi_rate_turn_hr
                            text: '200 Hz'
                            pos_hint: {"center_y":0.5} 
                            on_release: root.menu_sampling_rate_rate_turn_hr.open()
                        MySwitch:
                            id: switch_rate_turn_hr
                            active: False
                             
                    MyBoxLayout:
                        spacing: dp(50)
                        MDLabel:
                            text: 'ACCELERATION HR'
                        MDDropDownItem:
                            id: ddi_acceleration_hr
                            text: '200 Hz'
                            pos_hint: {"center_y":0.5}
                            on_release: root.menu_sampling_rate_acceleration_hr.open()
                        MySwitch:
                            id: switch_acceleration_hr
                            active: False
                            
            Screen:
                name: 'screen_environment'
                MDGridLayout:
                    rows: 2
                    padding: 50, 0, 50, 0
                    
                    MyBoxLayout:
                        MDLabel:
                            text: 'TEMPERATURE'  
                        MySwitch:
                            id: switch_temperature
                            active: False
                                            
                    MyBoxLayout:
                        MDLabel:
                            text: 'PRESSURE'
                        MySwitch:
                            id: switch_pressure
                            active: False
                          
            Screen:
                name: 'screen_settings'
                MDGridLayout:
                    rows: 5
                    padding: 50, 0, 50, 0
                                                
                    MyBoxLayout:
                        MDLabel: 
                            text: 'SAMPLING FREQUENCY'
                        MDDropDownItem:
                            id: ddi_sampling_rate
                            text: '100 Hz'
                            pos_hint: {"center_y":0.5}  
                            on_release: root.menu_sampling_rate.open()
                                                        
                    MyBoxLayout:
                        MDLabel: 
                            text: 'PRECISION'
                        MDDropDownItem:
                            id: ddi_precision
                            text: 'Float 64-bit'
                            pos_hint: {"center_y":0.5}  
                            on_release: root.menu_precision.open()
                    
                    MyBoxLayout:
                        MDLabel: 
                            text: 'COORDINATE SYSTEM'
                        MDDropDownItem:
                            id: ddi_coordinate
                            text: 'NED'
                            pos_hint: {"center_y":0.5}  
                            on_release: root.menu_coordinate.open()
                    
                    MyBoxLayout:
                        MDLabel: 
                            text: 'ORIENTATION'
                        MDDropDownItem:
                            id: ddi_orientation
                            text: 'QUATERNION'
                            pos_hint: {"center_y":0.5}  
                            on_release: root.menu_orientation.open()
                                                        
                    MyBoxLayout:
                        MDLabel: 
                            text: 'FILTER SETTINGS'
                        MDDropDownItem:
                            id: ddi_filter_settings
                            text: 'GENERAL'
                            pos_hint: {"center_y":0.5}  
                            on_release: root.menu_filter_settings.open()

    MDAnchorLayout:
        anchor_x: 'center'
        anchor_y: 'bottom'
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint: 1, 0.1	
            padding: 10, 0, 10, 10
            MDRaisedButton:
                text: 'CONFIGURE'
                size_hint_x: 1
                # pos_hint: {"y":0}
                on_release: root.on_click(self)
''')




class Tab(MDFloatLayout, MDTabsBase):
    # Class implementing content for a tab.
    pass



class View(MDFloatLayout):
    # type-hints
    screen_manager: MDScreenManager
    _tabs: Tab

    tab_icons = ["clock", "waveform", "thermometer", "cog-stop"]
    sampling_rate = ['100 Hz', '75 Hz', '50 Hz']
    sampling_rate_hr = ['200 Hz', '300 Hz', '400 Hz']
    orientation = ['QUATERNION', 'ROTATION MATRIX', 'EULER ANGLES']
    filter_settings = ['GENERAL', 'GENERAL_NO_BARO', 'GENERAL_MAG']
    precision = ['Float 64-bit', 'Float 32-bit', 'Fp 12.20', 'Fp 16.32']
    coordinate = ['NED', 'ENU', 'NWU']


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = None
        self.on_tab_start()
        self.on_drop_down_start()
                
                
    def on_tab_start(self):
        for tab_name in self.tab_icons:
            self._tabs.add_widget(Tab(icon=tab_name))
            
            
    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        """
        Called when switching tabs
        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        """
        count_icon = instance_tab.icon

        if count_icon == self.tab_icons[0]:
            self.screen_manager.current = 'screen_timestamp'
        elif count_icon == self.tab_icons[1]:
            self.screen_manager.current = 'screen_data'
        elif count_icon == self.tab_icons[2]:
            self.screen_manager.current = 'screen_environment'
        elif count_icon == self.tab_icons[3]:
            self.screen_manager.current = 'screen_settings'
            
            
    def on_drop_down_start(self):
        ##########################
        # ddi_rate_turn_hr
        ##########################
        self.menu_sampling_rate_rate_turn_hr, sampling_rate_rate_turn_hr_items = self.Create_DropDown_Widget(self.ids.ddi_rate_turn_hr, self.sampling_rate_hr, width=2)
                        
        ##########################
        # ddi_acceleration_hr
        ##########################
        self.menu_sampling_rate_acceleration_hr, sampling_rate_acceleration_hr_items = self.Create_DropDown_Widget(self.ids.ddi_acceleration_hr, self.sampling_rate_hr, width=2)        

        ##########################
        # ddi_sampling_rate
        ##########################
        self.menu_sampling_rate, sampling_rate_items = self.Create_DropDown_Widget(self.ids.ddi_sampling_rate, self.sampling_rate, width=2)
                
        ##########################
        # ddi_coordinate
        ##########################
        self.menu_coordinate, coordinate_items = self.Create_DropDown_Widget(self.ids.ddi_coordinate, self.coordinate, width=2)
                
        ##########################
        # ddi_orientation
        ##########################
        self.menu_orientation, orientation_items = self.Create_DropDown_Widget(self.ids.ddi_orientation, self.orientation, width=3)
                
        ##########################
        # ddi_filter_settings
        ##########################
        self.menu_filter_settings, filter_settings_items = self.Create_DropDown_Widget(self.ids.ddi_filter_settings, self.filter_settings, width=3)
                
        ##########################
        # ddi_precision
        ##########################
        self.menu_precision, precision_items = self.Create_DropDown_Widget(self.ids.ddi_precision, self.precision, width=3)
                
        
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
                                        
        
    def on_click(self, myButton):
        if self.controller:
            samplingRate = self.ids.ddi_sampling_rate.current_item
            samplingRateHR = self.ids.ddi_acceleration_hr.current_item
            coordinate = self.ids.ddi_coordinate.current_item
            precision = self.ids.ddi_precision.current_item
            filterSettings = self.ids.ddi_filter_settings.current_item
            
            if len(samplingRate)==0:
                samplingRate = self.sampling_rate[0]
            if len(samplingRateHR)==0:
                samplingRateHR = self.sampling_rate_hr[0]
            if len(coordinate)==0:
                coordinate = self.coordinate[0]
            if len(precision)==0:
                precision = self.precision[0]
            if len(filterSettings)==0:
                filterSettings = self.filter_settings[0]          
                
                
            self.controller.set_model_variables(coordinate, precision, samplingRate, samplingRateHR, filterSettings)
            
            
            
            isAcc = self.ids.switch_acceleration.active
            isFreeAcc = self.ids.switch_free_acceleration.active
            isAccHr = self.ids.switch_free_acceleration.active
            isGyro = self.ids.switch_rate_turn.active
            isGyroHr = self.ids.switch_rate_turn_hr.active
            isMag = self.ids.switch_magnetic_field.active
            isUtc = self.ids.switch_utc.active
            isPacketCounter = self.ids.switch_packet_counter.active
            isSampleTimeFine = self.ids.switch_sample_time.active
            isTemperature = self.ids.switch_temperature.active
            isPressure = self.ids.switch_pressure.active
            
            isQuat = 0
            isRotMat = 0
            isEuler = 0
            attitude = self.ids.ddi_orientation.current_item
            if len(attitude)==0:
                attitude = self.orientation[0]
            print('\n\nORIENTATION = ', attitude)
            if str(attitude) == self.orientation[0]:
                isQuat = 1
            elif str(attitude) == self.orientation[1]:
                isRotMat = 1
            elif str(attitude) == self.orientation[2]:
                isEuler = 1
            
            
            ##########################
            # ONLY FOR DEBUG PURPOSES
            print('isQuat = ', isQuat)
            print('isRotMat = ', isRotMat)
            print('isEuler = ', isEuler)
            ##########################                
            
            self.controller.compose_configuration_messages(isAcc, isFreeAcc, isAccHr, isGyro, isGyroHr, isMag, isQuat, isRotMat, isEuler, isUtc, isPacketCounter, isSampleTimeFine, isTemperature, isPressure)
            
            
        
    def set_controller(self, controller):
       """
       Set the controller
       :param controller:
       :return:
       """
       self.controller = controller


       


class Controller():
    OutputConfigurator = None
    FilterConfigurator = None
    
    def __init__(self, view):
        self.view = view
    
   
            
    def set_model_variables(self, coordinateSystem, precision, samplingRate, samplingRateHr, filterSettings):
        try:
            ParameterConfigurator = Model.SetConfigurationParameters(coordinateSystem, precision, samplingRate, samplingRateHr, filterSettings)
            self.OutputConfigurator = Model.SetOutputConfiguration(ParameterConfigurator.coordinate_System, ParameterConfigurator.data_Precision, ParameterConfigurator.sampling_Frequency, ParameterConfigurator.sampling_FrequencyHR)
            self.FilterConfigurator = Model.SetFilterProfile(ParameterConfigurator.filter_Settings)
            
            
            ##########################
            # ONLY FOR DEBUG PURPOSES
            print('\n\n\n')
            print('COORDINATE SYSTEM = ', ParameterConfigurator.coordinate_System)
            print('PRECISION = ', ParameterConfigurator.data_Precision)
            print('SAMPLING RATE = ', ParameterConfigurator.sampling_Frequency)
            print('SAMPLING RATE HR = ', ParameterConfigurator.sampling_FrequencyHR)
            print('FILTER SETTINGS = ', ParameterConfigurator.filter_Settings)
            ##########################
        except Exception as ex:
            print(ex)
    
    
    def compose_configuration_messages(self, isAcc, isFreeAcc, isAccHr, isGyro, isGyroHr, isMag, isQuat, isRotMat, isEuler, isUtc, isPacketCounter, isSampleTimeFine, isTemperature, isPressure):
        
        try:
            self.OutputConfigurator.ComposeMessage(isAcc, isFreeAcc, isAccHr, isGyro, isGyroHr, isMag, isQuat, isRotMat, isEuler, isUtc, isPacketCounter,isSampleTimeFine, isTemperature, isPressure)
            self.FilterConfigurator.ComposeMessage()
            
            self.save_settings_into_file(self.OutputConfigurator.MSG, self.FilterConfigurator.MSG)
        except Exception as ex:
            print(ex)
        
        
        ##########################
        # ONLY FOR DEBUG PURPOSES
        print('\n')
        print(self.OutputConfigurator.MSG)
        print(self.FilterConfigurator.MSG)
        ##########################
    
    
    def save_settings_into_file(self, outputMsg, filterMsg):
        # FILE HEADER
        header1 = self.convert_string_into_hex('REMOTV2 IMU CONFIG FILE\0')
        header2 = self.convert_string_into_hex('V1.00\0\0\0')        
        mySettings = header1 + ' ' + header2
        
        # ALIGNMENT ROTATION LOCAL
        msg = 'FA FF EC 11 01 3F 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00 44'
        length = self.calc_msg_len(msg)
        mySettings = mySettings + ' ' + length + ' ' + msg
        
        # ALIGNMENT ROTATION SENSOR
        msg = 'FA FF EC 11 00 3F 80 00 00 00 00 00 00 00 00 00 00 00 00 00 00 45'
        length = self.calc_msg_len(msg)
        mySettings = mySettings + ' ' + length + ' ' + msg
        
        # BAUDRATE
        msg = 'FA FF 18 01 0C DC'
        length = self.calc_msg_len(msg)
        mySettings = mySettings + ' ' + length + ' ' + msg
        
        # FILTER CONFIGURATION
        length = self.calc_msg_len(self.FilterConfigurator.MSG)
        mySettings = mySettings + ' ' + length + ' ' + self.FilterConfigurator.MSG
        
        # GNSS PLATFORM
        msg = 'FA FF 76 02 00 00 89'
        length = self.calc_msg_len(msg)
        mySettings = mySettings + ' ' + length + ' ' + msg
        
        # GNSS RECEIVER TYPE
        msg = 'FA FF AC 0A 00 01 00 02 00 0A 00 00 00 01 3D'
        length = self.calc_msg_len(msg)
        mySettings = mySettings + ' ' + length + ' ' + msg
        
        # LAT LON ALT
        msg = 'FA FF 6E 18 40 4A 1E C8 6E 8C 85 64 40 1B 5A 55 7F 4C D1 61 00 00 00 00 00 00 00 00 21'
        length = self.calc_msg_len(msg)
        mySettings = mySettings + ' ' + length + ' ' + msg
        
        # LOCATION ID
        msg = 'FA FF 84 02 00 00 7B'
        length = self.calc_msg_len(msg)
        mySettings = mySettings + ' ' + length + ' ' + msg
        
        # OPTION FLAGS
        msg = 'FA FF 48 08 00 00 00 00 FF FF FF FF B5'
        length = self.calc_msg_len(msg)
        mySettings = mySettings + ' ' + length + ' ' + msg
        
        # OUTPUT CONFIGURATION
        length = self.calc_msg_len(self.OutputConfigurator.MSG)
        mySettings = mySettings + ' ' + length + ' ' + self.OutputConfigurator.MSG
        
        # SYNC CONFIGURATION
        msg = 'FA FF 2C 18 09 01 01 00 00 00 00 00 00 00 03 E8 0E 08 01 00 00 00 00 00 01 F4 00 00 BB'
        length = self.calc_msg_len(msg)
        mySettings = mySettings + ' ' + length + ' ' + msg
        
        
        # STRING CONVERSION
        mySettings1 = ['0x{}'.format(i) for i in mySettings.split()]
        mySettings2 = [int(i, 16) for i in mySettings1]
        mySettings3 = bytes(mySettings2)
        
        
        filename = os.getcwd() + '\\imu_config.txt'        
        with open(filename, 'wb') as fid:
            fid.write(mySettings3)
        fid.close()
        

        

    def convert_string_into_hex(self, myString):
        # converts the string into bytes with the upper case
        myHex = bytes(myString, 'utf-8').hex().upper()
        # adds a white space every byte (two characters)
        myHex = ' '.join(myHex[i:i+2] for i in range(0, len(myHex), 2))
        return myHex
    
    
    def calc_msg_len(self, hexMessage):
        # counts the number spaces between each value and increment its value by one. The result is converted into hexadecimal
        return hex(1 + hexMessage.count(' '))[2:].zfill(2).upper()
        
        
class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.view = View()
        
                        
        self.controller = Controller(self.view)
        
        
        # set the controller to view
        self.view.set_controller(self.controller)


    def build(self):
        #self.theme_cls.material_style = "M3"
        self.title = 'XSENS MTi-7 CONFIGURATION'
        return self.view
    


if __name__ == '__main__':
    MainApp().run()

















