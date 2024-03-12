# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 14:43:57 2023
@author: gscalera

"""

# %% IMPORTS
from kivy.lang import Builder
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import IRightBodyTouch, TwoLineIconListItem, ThreeLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.transition import MDSwapTransition
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dropdownitem.dropdownitem import MDDropDownItem
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout #needed by pyinstaller...do not remove
from kivymd.uix.toolbar.toolbar import MDTopAppBar #needed by pyinstaller...do not remove
from kivymd.uix.scrollview import MDScrollView #needed by pyinstaller...do not remove
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton

from kivymd.toast import toast
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp

from BLEmodule import *


# %% UI DESIGN
Builder.load_string(
    """    
<MyLabelField@MDLabel>:
    font_style: 'H6'
    

<MyLabelValue@MDLabel>:
    halign: 'center'


<MyBoxLayout@MDBoxLayout>:
    size_hint_y: None
    height: dp(50)


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

        
<Content>
    size_hint_y: None
    height: self.minimum_height
        
    TwoLineIconListItem:
        

<ListItemWithCheckbox>:
    RightCheckbox:
        id: check
        
        
<View>:
    screen_manager_view: screen_manager_view
    
    MDScreenManager:
        id: screen_manager_view
        
        Screen:
            name: 'screen_scan'
            
            MDGridLayout:
                cols: 1
                
                MDTopAppBar:
                    title:"REMOT BLE APP"
                    left_action_items: [["power", lambda x: app.stop(), 'EXIT']]
                    right_action_items: [["access-point-plus", lambda x: root.Button_Scan_On_Click(), 'SCAN FOR DEVICES']]
            
                
        Screen:
            name: 'screen_device_choice'
            
            MDGridLayout:
                rows: 2
                
                MDTopAppBar:
                    title:"SELECT DEVICES..."
                    left_action_items: [["keyboard-backspace", lambda x: root.Button_Rescan_On_Click(), 'BACK']]
                    right_action_items: [["bluetooth", lambda x: root.Button_Connect_On_Click(), 'CONNECT']]
                    
                MDScrollView:
                    MDList:
                        id: connectedDevicesMDList
                                         
                
        Screen:
            name: 'screen_device_connected'
            
            MDBoxLayout:
                orientation: "vertical"

                MDTopAppBar:
                    id: toolbar
                    title:"DEVICES CONNECTED"
                    left_action_items: [["keyboard-backspace", lambda x: root.Button_Reselect_Device_On_Click(), 'BACK']]
                    #right_action_items: [["bluetooth-off", lambda x: root.Button_Disconnect_On_Click(), 'DISCONNECT']]
                    right_action_items: [["record-circle", lambda x: root.Button_Record_On_Click(), 'REC']]

                ScrollView:
                    MDGridLayout:
                        id: selectedDevicesGridLayout
                        cols: 2
                        adaptive_height: True
                        padding: 50, 0, 50, 0
                        spacing: 10, 0
                
                MDAnchorLayout:
                    anchor_x: 'right'  
                    anchor_y: 'bottom'                    
                    MDIconButton:
                        icon: "information"
                        icon_size: dp(40)
                        theme_icon_color: 'Hint'
                        on_release: root.Button_Info_On_Click()
              
        
        Screen:
            name: 'screen_device_recording'
            
            MDBoxLayout:
                orientation: "vertical"
                                        
                MDTopAppBar:
                    title:"DEVICE RECORDING"
                    right_action_items: [["stop-circle", lambda x: root.Button_Stop_Recording_On_Click(), 'STOP RECORDING']]
                
                MDBoxLayout:
                    padding: 50, 0, 50, 0
                    MDLabel: 
                        id: elapsed_time_label
                        font_size: 52
                        halign: 'center'
                        
                MDAnchorLayout:
                    anchor_x: 'right'  
                    anchor_y: 'bottom'                    
                    MDIconButton:
                        icon: "information"
                        icon_size: dp(40)
                        theme_icon_color: 'Hint'
                        on_release: root.Button_Info_On_Click()
        
        
        Screen:
            name: 'screen_device_idle'
            MDBoxLayout:
                orientation: "vertical"
                            
                MDTopAppBar:
                    title:"DEVICE IDLE"
                    left_action_items: [["record-circle", lambda x: root.Button_Record_On_Click(), 'REC']]
                    #right_action_items: [["bluetooth-off", lambda x: root.Button_Disconnect_On_Click(), 'DISCONNECT']]
                    right_action_items: [["bluetooth-off", lambda x: root.Show_Alert_Dialog(), 'DISCONNECT OR SHUTDOWN']]
                        
                MDAnchorLayout:
                    anchor_x: 'right'  
                    anchor_y: 'bottom'                    
                    MDIconButton:
                        icon: "information"
                        icon_size: dp(40)
                        theme_icon_color: 'Hint'
                        on_release: root.Button_Info_On_Click()
                    
                    
        Screen:
            name: 'screen_device_disconnected'
            
            MDGridLayout:
                rows: 1              
                
                MDTopAppBar:
                    title:"DEVICES DISCONNECTED"
                    left_action_items: [["restart", lambda x: root.Button_Restart_On_Click(), 'RESTART']]
                    right_action_items: [["power", lambda x: app.stop(), 'EXIT']]
                    
      
    MDBoxLayout:
        # https://stackoverflow.com/questions/36821496/insert-image-in-the-middle-of-the-screen-kivy-python
        
        Image:
            size_hint_y: 0.1
            size_hint_x: 0.95
            pos_hint: {'center_x': 0.5}
            id: imageView
            source: 'Logo.png'
            allow_stretch: True 
            #keep_ratio: False                
      
        
      

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
                    
"""
)

    
    
# %% CLASSES
class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    

class ListItemWithCheckbox(ThreeLineAvatarIconListItem):
    pass


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    def on_state(self, instance, new_state):
        super(RightCheckbox, self).on_state(instance, new_state)
        MDApp.get_running_app().root.current_screen.List_Items_Selection_Changed()
        

class Content(MDBoxLayout, TwoLineIconListItem):
    pass


class View(MDScreen):
    screen_manager_view: MDScreenManager
    dialog = None
    
    # DEVICES
    detectedDevices = list() # contains the detected DeviceBLE objects
    choices = list() # contains the indexes of the selected devices; updated into the List_Items_Selection_Changed
    selectedDevices = list() # contains the selected DeviceBLE objects; defined into the Connect_On_Click  
    
    # STOPWATCH
    stopwatch_seconds = 0
    stopwatch_started = False
    
    def __init__(self, **kwargs):
        super(View, self).__init__(**kwargs)
        self.devicePositions = ['HEAD', 'LEFT FOOT', 'RIGHT FOOT']
        Clock.schedule_interval(self.Update_Device_Characteristics, timeout = 15)
        Clock.schedule_interval(self.Update_Stopwatch, timeout = 0)
        
        
    def Button_Scan_On_Click(self):
        '''
        Event generated when the Scan button is pressed (screen_scan)
        '''
        self.detectedDevices = ScanForSeconds(Secs=2)
                
        
        for dev in self.detectedDevices:            
            myItem = ListItemWithCheckbox(text = dev.identifier, secondary_text = dev.address, tertiary_text = dev.addressType)
            myItem.ids["check"].disabled = not(dev.isConnectable)
            self.ids.connectedDevicesMDList.add_widget(myItem)
            
            # ONLY FOR DEBUG PURPOSES
            print('IS_CONNECTABLE: ', dev.isConnectable)
             
        self.screen_manager_view.current = 'screen_device_choice'
                       
      
    def Button_Rescan_On_Click(self):
        '''
        Event generated when the Rescan button is pressed (screen_device_choice)
        '''
        self.screen_manager_view.current = 'screen_scan'      
        self.ids.connectedDevicesMDList.clear_widgets()
        
            
    def Button_Connect_On_Click(self):  
        '''
        Event generated when the Connect button is pressed (screen_device_choice)
        '''        
        # DEFINE A LIST FROM THE DETECTED DEVICES AND THE CHOICES
        self.selectedDevices = SelectDevices(self.detectedDevices, self.choices)
        
        if self.selectedDevices:       
            # CONNECT AND UPDATE DEVICE CHARACTERISTICS
            ConnectDevices(self.selectedDevices)
            ReadModelInfo(self.selectedDevices)
            ReadBatteryLevel(self.selectedDevices)
            ReadManufacturerInfo(self.selectedDevices)
            ReadServiceInfo(self.selectedDevices)          
            RemotWriteTime(self.selectedDevices)
            RemotReadErrors(self.selectedDevices)
            RemotReadStatus(self.selectedDevices)
            
            # UPDATE LAYOUT
            for index, dev in enumerate(self.selectedDevices):
                status = ''
                if dev.isInError:
                    status = 'ERROR'
                else:
                    if dev.isReady:
                        status = 'READY'
                    else:
                        status = 'PLUGGED'
                
                myContent = Content(
                    text = status, 
                    secondary_text = 'battery level: ' + str(dev.batteryLevel))
                
                self.ids.selectedDevicesGridLayout.add_widget(
                    MDExpansionPanel(
                        icon = 'bluetooth',
                        content = myContent,
                        panel_cls = MDExpansionPanelOneLine(
                            text = dev.identifier,
                        )
                    )
                                        
                )
                
                
                myDdi = MDDropDownItem()
                myDdi.text = 'SELECT POSITION'                  
                myMenu, scratch = self.Create_DropDown_Widget(myDdi, ['HEAD', 'R_FOOT', 'L_FOOT'], width=4)
                myDdi.on_release = myMenu.open                
                self.ids.selectedDevicesGridLayout.add_widget(myDdi)
                self.ids.selectedDevicesGridLayout.ids['ddiPos' + str(index)] = myDdi

                
            self.screen_manager_view.current = 'screen_device_connected'
            
        else:
            toast('PLEASE SELECT A DEVICE')
            
            
    def Button_Reselect_Device_On_Click(self):
        '''
        Event generated when the Back button is pressed (screen_device_connected)
        '''
        DisconnectDevices(self.selectedDevices)
        self.selectedDevices = list()
        self.ids.selectedDevicesGridLayout.clear_widgets()
        self.screen_manager_view.current = 'screen_device_choice'  
    
    
    def Button_Record_On_Click(self):
        '''
        Event generated when the Record button is pressed (screen_device_connected)
        '''
        positions = list()
        status = list()
        for index, dev in enumerate(self.selectedDevices):
            pos = self.ids.selectedDevicesGridLayout.ids['ddiPos'+str(index)].text
            positions.append(pos)
            status.append(dev.isReady)
            
            
        notReady = [i for i, val in enumerate(status) if not val]
            
        if len(notReady) == 0:        
            self.screen_manager_view.current = 'screen_device_recording' 
            RemotStartRecording(self.selectedDevices, positions)
            self.stopwatch_seconds = 0
            self.stopwatch_started = True               
        else:
            toast('RECORDING NOT STARTED: AT LEAST ONE DEVICE IS NOT READY')
          
        
    def Button_Stop_Recording_On_Click(self):
        '''
        Event generated when the Record button is pressed (screen_device_recording)
        '''
        RemotStopRecording(self.selectedDevices)
        self.stopwatch_started = False
        self.ids.elapsed_time_label.text = ''
        self.screen_manager_view.current = 'screen_device_idle' 
        
        
    def Disconnect_On_Click(self):
        '''
        Event generated when the Disconnect button of the MDDialog is pressed (screen_device_idle)
        '''
        DisconnectDevices(self.selectedDevices)
        toast('DEVICES DISCONNECTED')
        self.dialog.dismiss()
        self.screen_manager_view.current = 'screen_device_disconnected'
        
        
    
    def Shutdown_On_Click(self):
        '''
        Event generated when the Shutdown button of the MDDialog is pressed (screen_device_idle)
        '''
        RemotShutdown(self.selectedDevices)
        toast('DEVICES SHUTDOWN')
        self.dialog.dismiss()
        self.screen_manager_view.current = 'screen_device_disconnected'
        
        
    def Show_Alert_Dialog(self):
        '''
        Event generated when the Disconnect button of the toolbar is pressed (screen_device_idle)
        '''
        #text_color=MDApp.get_running_app().theme_cls.primary_color
        disconnectBtn = MDRaisedButton(text="DISCONNECT")
        disconnectBtn.on_release = self.Disconnect_On_Click
        
        shutdownBtn = MDRaisedButton(text="SHUTDOWN")
        shutdownBtn.on_release = self.Shutdown_On_Click
        
        
        if not self.dialog:
            self.dialog = MDDialog(
                text="Discard draft?",
                buttons=[
                    disconnectBtn,
                    shutdownBtn,
                ],
            )
        self.dialog.open()
    
    
    def Button_Restart_On_Click(self):
        '''
        Event generated when the Restart button is pressed (screen_device_disconnected)
        '''
        self.screen_manager_view.current = 'screen_scan'
        self.ids.connectedDevicesMDList.clear_widgets()
        self.ids.selectedDevicesGridLayout.clear_widgets()
        
        
    def Button_Info_On_Click(self):
        '''
        Event generated when the Info button is pressed (screen_device_connected)
        '''
        self.DefineParametersForViewinfo()
        MDApp.get_running_app().sm.current = 'ViewInfo'
        
        
    def DefineParametersForViewinfo(self):
        tabsLabels = ['GENERAL', 'MODEL', 'STATUS', 'ERRORS']
                
        # PASS THE PARAMETERS TO THE SCREEN
        viewInfo = self.manager.get_screen('ViewInfo')
        viewInfo.DefineParameters(tabsLabels = tabsLabels, devices = self.selectedDevices)
        
        
    def Update_Device_Characteristics(self, dt):
        '''
        Event autogenerated every N seconds to update the device characteristics

        Parameters
        ----------
        dt : delta-time / time interval
        '''
        if self.selectedDevices:    
            dev0 = self.selectedDevices[0]
            if dev0.isConnected: # AT LEAST ONE DEVICE IS CONNECTED
                ReadBatteryLevel(self.selectedDevices)
                RemotReadErrors(self.selectedDevices)
                RemotReadStatus(self.selectedDevices)
                
                # ONLY FOR DEBUG PURPOSES
                for dev in self.selectedDevices:
                    print(dev.identifier + ' - BATTERY LEVEL %: ' + str(dev.batteryLevel))
    
    
    def Update_Stopwatch(self, dt):
        '''
        Event autogenerated every N seconds to update the stopwatch

        Parameters
        ----------
        dt : delta-time / time interval
        '''
        if self.stopwatch_started:
            self.stopwatch_seconds += dt

        minutes, seconds = divmod(self.stopwatch_seconds, 60)
        self.ids.elapsed_time_label.text = ('%02d:%02d' %
                                        (int(minutes), int(seconds)))
        # self.ids.elapsed_time_label.text = ('%02d:%02d.%03d' %
        #                                 (int(minutes), int(seconds), int(seconds * 1000 % 1000)))
        
        
    def List_Items_Selection_Changed(self):
        '''
        Events generated when the selected list of items changes
        '''
        self.choices = list() #empty the list
        for count, child in enumerate(self.ids.connectedDevicesMDList.children):
            if child.ids.check.state == 'down':
                self.choices.insert(0, len(self.detectedDevices)-1-count)
                          
        # ONLY FOR DEBUG PURPOSES                
        print('selected indexes: ', self.choices)
        
        
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
        #drop_down_item.set_item(text_item)
        drop_down_item.text = text_item
        menu.dismiss()
        
    
    
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
        self.Ddi_Start(self.devices)
        
        
    
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
        
    
    def Ddi_Start(self, devices):
        self.menu_device_info, device_info_items = self.Create_DropDown_Widget(self.ids.ddi_device_info, self.ddiLabels, width=5)
        
    
    def Ddi_Selection_Changed(self, current_item):   
        green = "limegreen"
        red = "red"
        grey = "darkgrey"
        
        if len(current_item)>0:  
            exist_count = self.ddiLabels.count(current_item)
            
            if exist_count > 0: 
                current_index = self.ddiLabels.index(current_item)
            
                dev = self.devices[current_index]
                
                # UPDATE SCREEN 'GENERAL'
                self.ids.Label_manufacturer.text = str(dev.manufacturer.name)
                self.ids.Label_id.text = str(dev.identifier)
                self.ids.Label_address.text = str(dev.address)
                self.ids.Label_address_type.text = str(dev.addressType)
                self.ids.Label_power.text = str(dev.power)
                self.ids.Label_battery.text = str(dev.batteryLevel)
                
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
                    self.ids.Checkbox_error.disabled_color = green
                else:
                    self.ids.Checkbox_error.disabled_color = grey
                
                if dev.isGpsConfFileFound == True:
                    self.ids.Checkbox_gps_file_found.disabled_color = green
                else:
                    self.ids.Checkbox_gps_file_found.disabled_color = grey
                    
                if dev.isImuConfFileFound == True:
                    self.ids.Checkbox_imu_file_found.disabled_color = green
                else:
                    self.ids.Checkbox_imu_file_found.disabled_color = grey
                
                if dev.isPpsWaiting == True:
                    self.ids.Checkbox_pps_waiting.disabled_color = green
                else:
                    self.ids.Checkbox_pps_waiting.disabled_color = grey
                
                if dev.isPpsAcquired == True:
                    self.ids.Checkbox_pps_acquired.disabled_color = green
                else:
                    self.ids.Checkbox_pps_acquired.disabled_color = grey
                
                if dev.isBooting == True:
                    self.ids.Checkbox_booting.disabled_color = green
                else:
                    self.ids.Checkbox_booting.disabled_color = grey
                    
                if dev.isFwUpdating == True:
                    self.ids.Checkbox_firmware_updating.disabled_color = green
                else:
                    self.ids.Checkbox_firmware_updating.disabled_color = grey
                
                if dev.isRecording == True:
                    self.ids.Checkbox_recording.disabled_color = green
                else:
                    self.ids.Checkbox_recording.disabled_color = grey  
                    
                if dev.isShuttingDown == True:
                    self.ids.Checkbox_shutting_down.disabled_color = green
                else:
                    self.ids.Checkbox_shutting_down.disabled_color = grey
                
                if dev.isPlugged == True:
                    self.ids.Checkbox_plugged.disabled_color = green
                else:
                    self.ids.Checkbox_plugged.disabled_color = grey
                
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
        
        # RESET DROP DOWN ITEM
        self.Set_DropDown_Item(self.ids.ddi_device_info, self.menu_device_info, 'SELECT DEVICE')         
        
        MDApp.get_running_app().sm.current = 'View'
        
    
    def ResetLabel(self, label):
        label.text = ''
        
        
    def ResetCheckbox(self, checkbox):
        checkbox.disabled_color = [1, 1, 1, 1]    

  

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sm = MDScreenManager(transition = MDSwapTransition())
        self.sm.add_widget(View(name="View"))
        self.sm.add_widget(ViewInfo(name="ViewInfo"))


    def build(self):
        self.title = 'REMOT BLE APP'
        self.icon = 'remot.png'
        return self.sm   
    
    


if __name__ == '__main__':
    MainApp().run()




















































