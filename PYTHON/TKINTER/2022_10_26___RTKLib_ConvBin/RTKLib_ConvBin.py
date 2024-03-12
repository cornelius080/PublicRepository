# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:52:37 2022
@author: gscalera
"""
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *

import RTKLib_ConvBin_support



# Support code for Balloon Help (also called tooltips).
# derived from http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
from time import time, localtime, strftime
class ToolTip(tk.Toplevel):
    """ Provides a ToolTip widget for Tkinter. """
    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
                 delay=0.5, follow=True):
        self.wdgt = wdgt
        self.parent = self.wdgt.master
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        self.withdraw()
        self.overrideredirect(True)
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                font=tooltip_font,
                aspect=1000).grid()
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')
    def spawn(self, event=None):
        self.visible = 1
        self.after(int(self.delay * 1000), self.show)
    def show(self):
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()
    def move(self, event):
        self.lastMotion = time()
        if self.follow is False:
            self.withdraw()
            self.visible = 1
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        try:
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)
    def hide(self, event=None):
        self.visible = 0
        self.withdraw()
    def update(self, msg):
        self.msgVar.set(msg)
#                   End of Class ToolTip


class App(tk.Tk):
  def __init__(self):
    super().__init__()

    # ROOT WINDOW CONFIGURATION
    self.title('RTKLib_ConvBin')
    #self.geometry('1080x750')
    self.resizable(False, False)
    self.state('zoomed')
    
    AppSupport = RTKLib_ConvBin_support.AppSupport(self)
    
    
    # %% CONTAINER EXTERNAL FRAME
    self.ExtFrame = tk.Frame(self)
    self.ExtFrame.place(relheight=1, relwidth=1)
    # self.ExtFrame.configure(bg='blue')
    # self.ExtFrame.configure(borderwidth="2")
    self.ExtFrame.rowconfigure(0, weight=1)
    self.ExtFrame.rowconfigure(1, weight=1)
    self.ExtFrame.rowconfigure(2, weight=1)
    self.ExtFrame.rowconfigure(3, weight=1)
    self.ExtFrame.rowconfigure(4, weight=1)
    self.ExtFrame.rowconfigure(5, weight=1)
    self.ExtFrame.columnconfigure(0, weight=1)

    
    # %% BUTTON OPEN FILE
    self.Button_OpenFile = ttk.Button(self.ExtFrame)
    self.Button_OpenFile.configure(text='''OPEN UBX FILE''') 
    self.Button_OpenFile.configure(command = AppSupport.Button_OpenFile_Clicked)
    self.Button_OpenFile.grid(row=0, padx=10, pady=25, sticky=tk.EW)


    # %% LABELFRAME RESULTS FOLDER LOCATION
    self.Labelframe_ResultsFolderLocation = ttk.LabelFrame(self.ExtFrame)
    self.Labelframe_ResultsFolderLocation.configure(relief='groove')
    self.Labelframe_ResultsFolderLocation.configure(text='''Results Folder Location''')  
    self.Labelframe_ResultsFolderLocation.grid(row=1, padx=10, pady=10, sticky=tk.EW)
    
    
    # %% RADIOBUTTON FOLDER SELECTION
    stickers = [tk.W, tk.E]
    self.folders = ["Input File Folder", "Selected Folder"]
    self.selectedFolder = tk.StringVar()
    
    self.Radiobuttons_Folder = []
    for folder in enumerate(self.folders):
        self.Radiobuttons_Folder.append(
            tk.Radiobutton(self.Labelframe_ResultsFolderLocation,
                           variable = self.selectedFolder, 
                           value = folder[0], 
                           text = folder[1],
                           command =  AppSupport.Radiobuttons_Selection_Changed))
        self.Radiobuttons_Folder[-1].grid(row=0,
                                          column=folder[0],
                                          padx=10,
                                          sticky=stickers[folder[0]]) 
    
    self.selectedFolder.set(0)
    
    
    # %% ENTRY OUTPUT FILE PATH
    self.outputFilepath = tk.StringVar()
    self.Entry1 = ttk.Entry(self.Labelframe_ResultsFolderLocation, textvariable=self.outputFilepath)
    self.Entry1.configure(width=150)
    #self.Entry1.insert(0,'OUTPUT FILE PATH')
    self.outputFilepath.set('OUTPUT FILE PATH')
    self.Entry1.configure(state='readonly')
    self.tooltip_font = "TkDefaultFont"
    self.Entry1_tooltip = \
    ToolTip(self.Entry1, self.tooltip_font, '''OUTPUT FILE PATH''')
    self.Entry1.grid(row=1, column=0, padx=10)
    
    
    # %% BUTTON BROWSE
    self.Button_Browse = ttk.Button(self.Labelframe_ResultsFolderLocation)
    self.Button_Browse.configure(text='''.....''')
    self.Button_Browse.configure(state='disabled')
    self.Button_Browse.configure(command = AppSupport.Button_Browse_Clicked)
    self.Button_Browse.grid(row=1, column=1, pady=10)
    
    
    
    
    
    

    # %% LABELFRAME LOGS DURATION
    self.Labelframe_LogsDuration = ttk.LabelFrame(self.ExtFrame)
    self.Labelframe_LogsDuration.configure(relief='groove')
    self.Labelframe_LogsDuration.configure(text='''Logs Duration''')
    self.Labelframe_LogsDuration.rowconfigure(0, weight=1)
    self.Labelframe_LogsDuration.rowconfigure(1, weight=1)
    self.Labelframe_LogsDuration.rowconfigure(2, weight=1)        
    self.Labelframe_LogsDuration.columnconfigure(0, weight=1)
    self.Labelframe_LogsDuration.columnconfigure(1, weight=1)
    self.Labelframe_LogsDuration.columnconfigure(2, weight=1)
    self.Labelframe_LogsDuration.columnconfigure(3, weight=1)
    self.Labelframe_LogsDuration.columnconfigure(4, weight=1)
    self.Labelframe_LogsDuration.grid(row=2, padx=10, pady=10, sticky=tk.EW)    
    
    
    # %% CHECKBUTTON START TIME
    self.Is_Checkbutton_StartTime_Checked = tk.BooleanVar()
    self.Checkbutton_StartTime = ttk.Checkbutton(self.Labelframe_LogsDuration)
    self.Checkbutton_StartTime.configure(text='''FROM''')
    self.Checkbutton_StartTime.configure(variable = self.Is_Checkbutton_StartTime_Checked)
    self.Checkbutton_StartTime.configure(onvalue = True)
    self.Checkbutton_StartTime.configure(offvalue = False)
    self.Checkbutton_StartTime.configure(command = AppSupport.Checkbutton_StartTime_Checked_Changed)
    self.Checkbutton_StartTime.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
    
    
    # %% CHECKBUTTON STOP TIME
    self.Is_Checkbutton_StopTime_Checked = tk.BooleanVar()
    self.Checkbutton_StopTime = ttk.Checkbutton(self.Labelframe_LogsDuration)
    self.Checkbutton_StopTime.configure(text='''TO''')
    self.Checkbutton_StopTime.configure(variable = self.Is_Checkbutton_StopTime_Checked)
    self.Checkbutton_StopTime.configure(onvalue = True)
    self.Checkbutton_StopTime.configure(offvalue = False)
    self.Checkbutton_StopTime.configure(command = AppSupport.Checkbutton_StopTime_Checked_Changed)
    self.Checkbutton_StopTime.grid(row=0, column=2, columnspan=2, padx=10, pady=10, sticky=tk.W)


    # %% CHECKBUTTON INTERVAL
    self.Is_Checkbutton_Interval_Checked = tk.BooleanVar()
    self.Checkbutton_Interval = ttk.Checkbutton(self.Labelframe_LogsDuration)
    self.Checkbutton_Interval.configure(text='''INTERVAL (s)''')
    self.Checkbutton_Interval.configure(variable = self.Is_Checkbutton_Interval_Checked)
    self.Checkbutton_Interval.configure(onvalue = True)
    self.Checkbutton_Interval.configure(offvalue = False)
    self.Checkbutton_Interval.configure(command = AppSupport.Checkbutton_Interval_Checked_Changed)
    self.Checkbutton_Interval.grid(row=0, column=4, columnspan=1, padx=10, pady=10, sticky=tk.W)
    
    
    # %% ENTRY START TIME YMD
    self.startTime_YMD = tk.StringVar()
    self.Entry_StartTime_YMD = ttk.Entry(self.Labelframe_LogsDuration, textvariable=self.startTime_YMD)
    self.Entry_StartTime_YMD.configure(state='disabled')
    self.tooltip_font = "TkDefaultFont"
    self.Entry_StartTime_YMD_tooltip = \
    ToolTip(self.Entry_StartTime_YMD, self.tooltip_font, '''YYYY/MM/DD''')
    self.Entry_StartTime_YMD.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)


    # %% ENTRY START TIME HMS
    self.startTime_HMS = tk.StringVar()
    self.Entry_StartTime_HMS = ttk.Entry(self.Labelframe_LogsDuration, textvariable=self.startTime_HMS)
    self.Entry_StartTime_HMS.configure(state='disabled')
    self.tooltip_font = "TkDefaultFont"
    self.Entry_StartTime_HMS_tooltip = \
    ToolTip(self.Entry_StartTime_HMS, self.tooltip_font, '''hh:mm:ss''')
    self.Entry_StartTime_HMS.grid(row=1, column=1, pady=5, sticky=tk.W)


    # %% ENTRY STOP TIME YMD
    self.stopTime_YMD = tk.StringVar()
    self.Entry_StopTime_YMD = ttk.Entry(self.Labelframe_LogsDuration, textvariable=self.stopTime_YMD)
    self.Entry_StopTime_YMD.configure(state='disabled')
    self.tooltip_font = "TkDefaultFont"
    self.Entry_StopTime_YMD_tooltip = \
    ToolTip(self.Entry_StopTime_YMD, self.tooltip_font, '''YYYY/MM/DD''')
    self.Entry_StopTime_YMD.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)


    # %% ENTRY STOP TIME HMS
    self.stopTime_HMS = tk.StringVar()
    self.Entry_StopTime_HMS = ttk.Entry(self.Labelframe_LogsDuration, textvariable=self.stopTime_HMS)
    self.Entry_StopTime_HMS.configure(state='disabled')
    self.tooltip_font = "TkDefaultFont"
    self.Entry_StopTime_HMS_tooltip = \
    ToolTip(self.Entry_StopTime_HMS, self.tooltip_font, '''hh:mm:ss''') 
    self.Entry_StopTime_HMS.grid(row=1, column=3, pady=5, sticky=tk.W)
    
    
    # %% COMBOBOX INTERVAL
    self.Selected_Interval = tk.StringVar()
    self.Picker_Interval = ttk.Combobox(self.Labelframe_LogsDuration)
    self.Picker_Interval.configure(textvariable = self.Selected_Interval)        
    self.Picker_Interval.configure(values=['0.1', '0.2', '0.5', '1', '2', '5', '10', '30'])
    self.Picker_Interval.configure(state='disabled')
    self.Picker_Interval.bind('<<ComboboxSelected>>', AppSupport.Picker_Interval_Selection_Changed)
    self.Picker_Interval.grid(row=1, column=4, padx=10, pady=5, sticky=tk.W)
    
    
    # %% CHECKBUTTON TIME ROUNDING
    self.Is_Checkbutton_TimeRounding_Checked = tk.BooleanVar()
    self.Checkbutton_TimeRounding = ttk.Checkbutton(self.Labelframe_LogsDuration)
    self.Checkbutton_TimeRounding.configure(text='''Time rounding (required for OPUS and other third-party services)''')
    self.Checkbutton_TimeRounding.configure(variable=self.Is_Checkbutton_TimeRounding_Checked)
    self.Checkbutton_TimeRounding.configure(onvalue = True)
    self.Checkbutton_TimeRounding.configure(offvalue = False)
    self.Checkbutton_TimeRounding.configure(state='disabled')
    self.Checkbutton_TimeRounding.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W)
    
    
    
    
    
    
    
    # %% FRAME RINEX - MARKER
    self.FrameMiddle = ttk.LabelFrame(self.ExtFrame)
    self.FrameMiddle.configure(relief='groove')
    self.FrameMiddle.rowconfigure(0, weight=1)
    self.FrameMiddle.rowconfigure(1, weight=1)
    self.FrameMiddle.columnconfigure(0, weight=1)
    self.FrameMiddle.columnconfigure(1, weight=5)
    self.FrameMiddle.grid(row=3, column=0, padx=10, pady=10, sticky=tk.EW)


    # %% LABEL RINEX VERSION
    self.Label1 = ttk.Label(self.FrameMiddle)
    self.Label1.configure(text='''Rinex Version''')
    self.Label1.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)


    # %% LABEL MARKER NAME
    self.Label2 = ttk.Label(self.FrameMiddle)
    self.Label2.configure(text='''Marker Name''')
    self.Label2.grid(row=0, column=1, pady=5, sticky=tk.W)
    
    
    # %% COMBOBOX RINEX VERSION
    self.Selected_RinexVersion = tk.StringVar()
    self.Picker_RinexVersion = ttk.Combobox(self.FrameMiddle)
    self.Picker_RinexVersion.configure(state='readonly')
    self.Picker_RinexVersion.configure(textvariable = self.Selected_RinexVersion)        
    self.Picker_RinexVersion.configure(values=['3.02', '2.10'])
    self.Picker_RinexVersion.set('3.02')
    self.Picker_RinexVersion.bind('<<ComboboxSelected>>', AppSupport.Picker_RinexVersion_Selection_Changed)
    self.Picker_RinexVersion.grid(row=1, column=0, padx=10, sticky=tk.W)


    # %% ENTRY MARKER NAME
    self.Entry_MarkerName = ttk.Entry(self.FrameMiddle)
    self.Entry_MarkerName.configure(width=120)
    #self.Entry_MarkerName.configure(state='disabled')
    self.tooltip_font = "TkDefaultFont"
    self.Entry_MarkerName_tooltip = \
    ToolTip(self.Entry_MarkerName, self.tooltip_font, '''Marker Name''')
    self.Entry_MarkerName.grid(row=1, column=1, pady=10, sticky=tk.W)
    
    
    
    
    
    
    
    # %% LABELFRAME SATELLITES
    self.Labelframe_Satellites = ttk.LabelFrame(self.ExtFrame)
    self.Labelframe_Satellites.configure(relief='groove')
    self.Labelframe_Satellites.configure(text='''Satellites''')
    self.Labelframe_Satellites.rowconfigure(0, weight=1)
    self.Labelframe_Satellites.rowconfigure(1, weight=1)
    self.Labelframe_Satellites.columnconfigure(0, weight=1)
    self.Labelframe_Satellites.columnconfigure(1, weight=1)
    self.Labelframe_Satellites.columnconfigure(2, weight=1)
    self.Labelframe_Satellites.columnconfigure(3, weight=1)
    self.Labelframe_Satellites.grid(row=4, padx=10, pady=10, sticky=tk.EW)
        
    
    # %% CHECKBUTTON GPS
    self.Is_Checkbutton_Gps_Checked = tk.BooleanVar()
    self.Checkbutton_Gps = ttk.Checkbutton(self.Labelframe_Satellites)
    self.Checkbutton_Gps.configure(text='''GPS''')
    self.Checkbutton_Gps.configure(onvalue = True)
    self.Checkbutton_Gps.configure(offvalue = False)
    self.Checkbutton_Gps.configure(variable = self.Is_Checkbutton_Gps_Checked)
    self.Checkbutton_Gps.configure(command = AppSupport.Checkbutton_Gps_Checked_Changed)
    self.Is_Checkbutton_Gps_Checked.set(True)
    self.Checkbutton_Gps.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)


    # %% CHECKBUTTON GLONASS
    self.Is_Checkbutton_Glonass_Checked = tk.BooleanVar()
    self.Checkbutton_Glonass = ttk.Checkbutton(self.Labelframe_Satellites)
    self.Checkbutton_Glonass.configure(text='''GLONASS''')
    self.Checkbutton_Glonass.configure(onvalue = True)
    self.Checkbutton_Glonass.configure(offvalue = False)
    self.Checkbutton_Glonass.configure(variable = self.Is_Checkbutton_Glonass_Checked)
    self.Checkbutton_Glonass.configure(command = AppSupport.Checkbutton_Glonass_Checked_Changed)
    self.Is_Checkbutton_Glonass_Checked.set(True)
    self.Checkbutton_Glonass.grid(row=0, column=1, pady=10, sticky=tk.W)


    # %% CHECKBUTTON GALILEO
    self.Is_Checkbutton_Galileo_Checked = tk.BooleanVar()
    self.Checkbutton_Galileo = ttk.Checkbutton(self.Labelframe_Satellites)
    self.Checkbutton_Galileo.configure(text='''GALILEO''')
    self.Checkbutton_Galileo.configure(onvalue = True)
    self.Checkbutton_Galileo.configure(offvalue = False)
    self.Checkbutton_Galileo.configure(variable = self.Is_Checkbutton_Galileo_Checked)
    self.Checkbutton_Galileo.configure(command = AppSupport.Checkbutton_Galileo_Checked_Changed)
    self.Is_Checkbutton_Galileo_Checked.set(True)
    self.Checkbutton_Galileo.grid(row=0, column=2, pady=10, sticky=tk.W)


    # %% CHECKBUTTON BEIDOU
    self.Is_Checkbutton_BeiDou_Checked = tk.BooleanVar()
    self.Checkbutton_BeiDou = ttk.Checkbutton(self.Labelframe_Satellites)
    self.Checkbutton_BeiDou.configure(text='''BEIDOU''')
    self.Checkbutton_BeiDou.configure(onvalue = True)
    self.Checkbutton_BeiDou.configure(offvalue = False)
    self.Checkbutton_BeiDou.configure(variable = self.Is_Checkbutton_BeiDou_Checked)
    self.Checkbutton_BeiDou.configure(command = AppSupport.Checkbutton_Beidou_Checked_Changed)
    self.Is_Checkbutton_BeiDou_Checked.set(True)
    self.Checkbutton_BeiDou.grid(row=0, column=3, pady=10, sticky=tk.W)


    # %% CHECKBUTTON QZSS
    self.Is_Checkbutton_Qzss_Checked = tk.BooleanVar()
    self.Checkbutton_Qzss = ttk.Checkbutton(self.Labelframe_Satellites)
    self.Checkbutton_Qzss.configure(text='''QZSS''')
    self.Checkbutton_Qzss.configure(onvalue = True)
    self.Checkbutton_Qzss.configure(offvalue = False)
    self.Checkbutton_Qzss.configure(variable = self.Is_Checkbutton_Qzss_Checked)
    self.Checkbutton_Qzss.configure(command = AppSupport.Checkbutton_Qzss_Checked_Changed)
    self.Checkbutton_Qzss.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)


    # %% CHECKBUTTON SBAS
    self.Is_Checkbutton_Sbas_Checked = tk.BooleanVar()
    self.Checkbutton_Sbas = ttk.Checkbutton(self.Labelframe_Satellites)
    self.Checkbutton_Sbas.configure(text='''SBAS''')
    self.Checkbutton_Sbas.configure(onvalue = True)
    self.Checkbutton_Sbas.configure(offvalue = False)
    self.Checkbutton_Sbas.configure(variable = self.Is_Checkbutton_Sbas_Checked)
    self.Checkbutton_Sbas.configure(command = AppSupport.Checkbutton_Sbas_Checked_Changed)
    self.Checkbutton_Sbas.grid(row=1, column=1, pady=10, sticky=tk.W)


    # %% CHECKBUTTON IRNSS
    self.Is_Checkbutton_Irnss_Checked = tk.BooleanVar()
    self.Checkbutton_Irnss = ttk.Checkbutton(self.Labelframe_Satellites)
    self.Checkbutton_Irnss.configure(text='''IRNSS''')
    self.Checkbutton_Irnss.configure(onvalue = True)
    self.Checkbutton_Irnss.configure(offvalue = False)
    self.Checkbutton_Irnss.configure(variable = self.Is_Checkbutton_Irnss_Checked)
    #self.Checkbutton_Irnss.configure(command = AppSupport.Checkbutton_Irnss_Checked_Changed)
    self.Checkbutton_Irnss.configure(state = 'disabled')
    self.Checkbutton_Irnss.grid(row=1, column=2, pady=10, sticky=tk.W)
    
    
    
    
    
    
    # %% BUTTON CONVERT
    self.Button_Convert = ttk.Button(self.ExtFrame)
    self.Button_Convert.configure(text='''CONVERT''')
    self.Button_Convert.configure(state='disabled')
    self.Button_Convert.configure(command = AppSupport.Button_Convert_Clicked)
    self.Button_Convert.grid(row=5, padx=10, pady=25, sticky=tk.EW)
  

if __name__ == "__main__":
  app = App()
  app.mainloop()  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
