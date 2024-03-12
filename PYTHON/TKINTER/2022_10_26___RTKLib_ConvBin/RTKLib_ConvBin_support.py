# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 17:23:05 2022
@author: gscalera
"""
#import RTKLib_ConvBin  
#import tkinter as tk
import subprocess
from tkinter import filedialog
import tkinter.messagebox as messagebox

class AppSupport():
    fullFileName = ''
    outputDir = ''
    start_YMD = ''
    start_HMS = ''
    stop_YMD = ''
    stop_HMS = ''
    timeInterval = ''
    rinexVersion = '3.02'
    markerName = ''
    isGps = True
    isGlonass = True
    isGalileo = True
    isBeidou = True
    isQzss = False
    isSbas = False
    

    def __init__(self, rootApp):
        self.myApp = rootApp
        
    
    def Button_OpenFile_Clicked(self):
        fileTypes = (('Ubx files', '*.ubx'), ('All files', '*.*'))
        fullFileName = filedialog.askopenfilename(title='SELECT UBX FILE', initialdir='\\', filetypes=fileTypes)        

        self.fullFileName = fullFileName.replace("/", "\\")

        if self.fullFileName:
            allIndices = [i for i, val in enumerate(self.fullFileName) if val == '\\']
            self.outputDir = self.fullFileName[ : max(allIndices)]
            
            self.myApp.outputFilepath.set(self.outputDir)       
            self.myApp.Button_Convert.configure(state='!disabled')        
                
        
    def Radiobuttons_Selection_Changed(self):
        messagebox.showinfo(title='SERVICE MESSAGEBOX',
                               message='Verifica come cambiare la directory di convbin')
        
        # if self.myApp.selectedFolder.get() == '0':
        #     self.myApp.Button_Browse.configure(state='disabled')  
        # else:
        #     self.myApp.Button_Browse.configure(state='!disabled')  
            
        
    def Button_Browse_Clicked(self):
        path = filedialog.askdirectory(title='SELECT OUTPUT PATH', initialdir='/')
        if path:
            self.outputDir = path
            self.myApp.outputFilepath.set(self.outputDir) 
        
        
    def Checkbutton_StartTime_Checked_Changed(self):
        if self.myApp.Is_Checkbutton_StartTime_Checked.get():
            self.myApp.Entry_StartTime_YMD.configure(state='!disabled')
            self.myApp.Entry_StartTime_HMS.configure(state='!disabled')
        else:
            self.myApp.Entry_StartTime_YMD.configure(state='disabled')
            self.myApp.Entry_StartTime_HMS.configure(state='disabled')
            self.myApp.startTime_YMD.set('')
            self.myApp.startTime_HMS.set('')
                    

    def Checkbutton_StopTime_Checked_Changed(self):
        if self.myApp.Is_Checkbutton_StopTime_Checked.get():
            self.myApp.Entry_StopTime_YMD.configure(state='!disabled')
            self.myApp.Entry_StopTime_HMS.configure(state='!disabled')
        else:
            self.myApp.Entry_StopTime_YMD.configure(state='disabled') 
            self.myApp.Entry_StopTime_HMS.configure(state='disabled')
            self.myApp.stopTime_YMD.set('')
            self.myApp.stopTime_HMS.set('')
        
        
    def Checkbutton_Interval_Checked_Changed(self):    
        if self.myApp.Is_Checkbutton_Interval_Checked.get():
            self.myApp.Picker_Interval.configure(state='!disabled')
            self.myApp.Picker_Interval.configure(state='readonly')
        else:
            self.myApp.Picker_Interval.configure(state='disabled')
            self.timeInterval = ''
            
            
    def Picker_Interval_Selection_Changed(self, event):  
        self.timeInterval = self.myApp.Selected_Interval.get()
        
        
    def Picker_RinexVersion_Selection_Changed(self, event):    
        self.rinexVersion = self.myApp.Selected_RinexVersion.get()
        
        
    def Checkbutton_Gps_Checked_Changed(self):    
        if self.myApp.Is_Checkbutton_Gps_Checked.get():
            self.isGps = True
        else:
            self.isGps = False
    
    
    def Checkbutton_Glonass_Checked_Changed(self):    
        if self.myApp.Is_Checkbutton_Glonass_Checked.get():
            self.isGlonass = True
        else:
            self.isGlonass = False
    
    
    def Checkbutton_Galileo_Checked_Changed(self):    
        if self.myApp.Is_Checkbutton_Galileo_Checked.get():
            self.isGalileo = True
        else:
            self.isGalileo = False
    
    
    def Checkbutton_Beidou_Checked_Changed(self):    
        if self.myApp.Is_Checkbutton_BeiDou_Checked.get():
            self.isBeidou = True
        else:
            self.isBeidou = False
    
    
    def Checkbutton_Qzss_Checked_Changed(self):    
        if self.myApp.Is_Checkbutton_Qzss_Checked.get():
            self.isQzss = True
        else:
            self.isQzss = False
    
    
    def Checkbutton_Sbas_Checked_Changed(self):    
        if self.myApp.Is_Checkbutton_Sbas_Checked.get():
            self.isSbas = True
        else:
            self.isSbas = False
        
        
    def Button_Convert_Clicked(self):
        self.start_YMD = self.myApp.startTime_YMD.get()
        self.start_HMS = self.myApp.startTime_HMS.get()
        
        self.stop_YMD = self.myApp.stopTime_YMD.get()
        self.stop_HMS = self.myApp.stopTime_HMS.get()
        
        self.markerName = self.myApp.Entry_MarkerName.get()
        
        
        cmd = self.fullFileName
        if self.start_YMD != '' and self.start_HMS != '':
            cmd = cmd + ' -ts ' + self.start_YMD + ' ' + self.start_HMS
        
        if self.stop_YMD != '' and self.stop_HMS != '':
            cmd = cmd + ' -te ' + self.stop_YMD + ' ' + self.stop_HMS
        
        if self.timeInterval != '':
            cmd = cmd + ' -ti ' + self.timeInterval
            
        if self.rinexVersion != '':
            cmd = cmd + ' -v ' + self.rinexVersion
        
        if self.markerName != '':
            cmd = cmd + ' -hm ' + self.markerName
            
        if not self.isGps:
            cmd = cmd + ' -y G'
        
        if not self.isGlonass:
            cmd = cmd + ' -y R'
        
        if not self.isGalileo:
            cmd = cmd + ' -y E'
            
        if not self.isBeidou:
            cmd = cmd + ' -y C'
            
        if not self.isQzss:
            cmd = cmd + ' -y J'
            
        if not self.isSbas:
            cmd = cmd + ' -y S'
        
        #print(cmd)
        converter = ConvBin()
        converter.ConvertUbxIntoRinex(cmd)
        
        
        
class ConvBin():    
    def __init__(self):
        self.process = subprocess.Popen(['cmd.exe'], stdin=subprocess.PIPE, text=True)
        self.functionCommand = 'convbin.exe'
    
    def ConvertUbxIntoRinex(self, cmd):
        command = self.functionCommand + ' ' + cmd + '\n'
        self.process.stdin.write(command)
        self.process.stdin.close()
        self.process.wait()
        
        
        
        
        
        
        
        
        
        
        