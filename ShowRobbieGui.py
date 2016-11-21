# *************************************************************
# PROJECT:    ShowRobbieGUI
#
# FILE:       Routine.py
#
# DEVELOPMENT ENVIRONMENTS:
# Eclipse Neon.1 with PyDev  with Python 2.7.11
#
# EXECUTION ENVIRIONMENTS
# Eclipse Neon.1 with PyDev with Python 2.7.11
#
# HISTORY:
# Date        Author            Description
# ====        ======            ===========
# 11/2/16     Jesse Lieberg     Initial Creation
# Check githut commit history
#
# DESCRIPTION
# https://github.com/GammaGames/ShowRobbieGUI
# **************************************************************

# -------------------
# Application imports
# -------------------
import os
import glob
import threading
import imp
import time

from Tkinter import *
from ttk import *

import Routines
from Routines import Routine
from Modules.BatteryStats import BatteryStats

class ShowRobbieGui(object):
    '''
    classdocs
    '''
    # Create element variables 
    window = None
    
    routinesFrame = None
    availableRoutinesLabel = None
    availableRoutines = None
    availableRoutinesScrollbar = None
    
    connectFrame = None
    connectLabel = None
    connectIP = None
    connectPort = None
    connectButton = None
    
    batteryFrame = None
    videoFeed = None
    videoFeedLabel = None
    batteryLabel = None
    batteryBar = None
    
    controlsFrame = None
    playButton = None
    stopButton = None
    progressBar = None

    ipVar = None
    portVar = None
    progressVar = None
    batteryVar = None
    connected = False
    
    batteryProxy = None
    routine = None
    routineThread = None
    
    routines = {}
    routineFilesToIgnore = {
        "Routine",
        "__init__"
        }

    def __init__(self):
        '''
        '''
        self.createComponents()
        self.configureWindow()
        self.window.mainloop()   
    #def __init__
    
    def createComponents(self):
        
        # Create window
        self.window = Tk("ShowRobbie")
        
        # Create Routine components
        self.routinesFrame = Frame(self.window)
        self.availableRoutinesLabel = Label(self.routinesFrame, text="Routines")
        self.availableRoutinesScrollbar = Scrollbar(self.routinesFrame)
        self.availableRoutines = Listbox(self.routinesFrame, 
            yscrollcommand = self.availableRoutinesScrollbar.set, width = 32)
        
        # Create connection components
        self.connectFrame = Frame(self.window)
        self.connectLabel = Label(self.connectFrame, text="Connection")
        self.ipVar = StringVar()
        self.ipVar.set("10.0.0.7")
        self.connectIP = Entry(self.connectFrame, textvariable = self.ipVar, 
           width = 16)
        self.portVar = IntVar()
        self.portVar.set(9559)
        self.connectPort = Entry(self.connectFrame, textvariable = self.portVar, 
            width = 8)
        self.connectButton = Button(self.connectFrame, text = "Connect", 
            command = self.clickConnect)
        
        # Create stats components (battery, video)
        self.batteryFrame = Frame(self.window)
        self.videoFeed = PhotoImage(master = self.batteryFrame, 
            file="img/placeholder_image.gif")
        self.videoFeedLabel = Label(self.batteryFrame, image = self.videoFeed)
        self.batteryVar = DoubleVar()
        self.batteryLabel = Label(self.batteryFrame, text="0", 
            justify = RIGHT)
        self.batteryBar = Progressbar(self.batteryFrame, orient = VERTICAL, 
            mode = "determinate", variable = self.batteryVar, length = 30)
        
        # Create control components
        self.controlsFrame = Frame(self.window)
        self.playButton = Button(self.controlsFrame, text = "Run", 
            state = DISABLED, command = self.clickPlay)
        self.stopButton = Button(self.controlsFrame, text = "Stop",
            state = DISABLED, command = self.clickStop)
        self.progressVar = DoubleVar()
        self.progressBar = Progressbar(self.controlsFrame, orient = HORIZONTAL, 
           mode = "determinate", variable = self.progressVar, length = 600)
        
        # Set component options
        self.window.wm_title("ShowRobbie")
        self.window.minsize(width=700, height=500)
        self.window.resizable(width=False, height=False)
        
        # Create array of available routines
        self.routines = glob.glob("Routines/*.py")
        self.routines = [os.path.split(p)[1][:-3] for p in self.routines]
        
        ignoreFiles = ""
        for filename in self.routineFilesToIgnore:
            ignoreFiles += "(" + filename + ")|"
        ignoreFiles = ignoreFiles[:-1]

        # Add routines to Listbox
        for index, routine in enumerate(self.routines):
            if not re.match(ignoreFiles, routine, flags=0):
                self.availableRoutines.insert(index, routine)
                
    #def createComponents
    
    def configureWindow(self):
        self.window.rowconfigure(1, weight = 1)

        # Pack routines list
        self.availableRoutinesLabel.pack(side = TOP, fill = X)
        self.availableRoutines.pack(side = LEFT, expand = True, fill = Y)
        self.availableRoutinesScrollbar.pack(side = RIGHT, fill = Y)
        
        self.routinesFrame.grid(column = 0, row = 0, rowspan = 3, 
            sticky = W+N+S, padx = (10, 0), pady = 10)
        
        # Pack connection stuff
        self.connectLabel.pack(side = TOP, expand = True, fill = X)
        self.connectIP.pack(side = LEFT, padx = (0, 2))
        self.connectPort.pack(side = LEFT)
        self.connectButton.pack(side = LEFT, padx = (2, 0))
        
        self.connectFrame.grid(column = 1, row = 0, sticky = N+S,
           padx = (0, 10), pady = (10, 0))
        
        # Pack stat stuff (battery, video)
        self.videoFeedLabel.pack(side = TOP)
        self.batteryBar.place(x = -25, y = 5, relx = 1.0, width = 20)
        self.batteryLabel.place(x = -47, y = 10, relx = 1.0, width = 20)
        
        self.batteryFrame.grid(column = 1, row = 1,
            padx = (0, 10), pady = 0)
        
        # Pack control stuff       
        self.playButton.grid(row = 1, column = 0, sticky = E, pady = (0, 5),
            padx = (0, 1))
        self.stopButton.grid(row = 1, column = 1, sticky = W, pady = (0, 5),
            padx = (1, 0))
        self.progressBar.grid(row = 2, column = 0, columnspan = 2, sticky = E+W)
        
        self.controlsFrame.grid(column = 1, row = 2, sticky = S+N,
           padx = (0, 10), pady = (0, 10))
        
    #def packAndConfigureWindow
    
    def clickConnect(self):
        try:
            self.batteryProxy = BatteryStats()
            self.ipVar.set(self.connectIP.get())
            self.portVar.set(int(self.connectPort.get()))
            print "connecting"
            self.batteryProxy.connect(self.ipVar.get(), self.portVar.get())
            self.connected = True
            print "updating ui"
            t = threading.Thread(target = self.updateUi)
            t.start()
        except  Exception:
            self.connected = False
    #def clickConnect
    
    def clickDisconnect(self):
        print "disconnecting"
        self.batteryProxy = None
        self.connected = False
        print "updating ui"
        t = threading.Thread(target = self.updateUi)
        t.start()
    #def clickDisconnect
    
    def clickPlay(self):
        script = self.availableRoutines.get(ACTIVE)
        print ("constructing " + script)      
        src = imp.load_source("Routines", "Routines/" + script + ".py")
        class_ = getattr(src, script)
        self.routine = class_()        
        print ("connecting")
        self.routine.connect(self.ipVar.get(), self.portVar.get())
        print ("running " + script)
        self.routineThread = threading.Thread(target = self.routine.run)
        self.routineThread.start()  
        
        t = threading.Thread(target = self.updateUi)
        t.start()
    #def clickPlay
    
    def clickStop(self):
        self.routineThread = None
        self.routine.stop()
        self.routine = None
        self.progressBar["value"] = 0.0
        t = threading.Thread(target = self.updateUi)
        t.start()
    #def clickStop
    
    def updateUi(self):
        self.updateConnect()
        self.updateControls()
        self.updateBattery()
    #def updateUi
    
    def updateImage(self):
        print "updating image"
    #def updateImage
    
    def updateBattery(self):
        self.batteryVar = self.batteryProxy.getBatteryPercentage()
        self.batteryLabel.config(text = str(self.batteryVar) + "%")
        self.batteryBar["value"] = self.batteryVar
    #def updateBattery
    
    def updateConnect(self):
        if self.connected:
            self.connectButton.config(text = "Disconnect")
            self.connectButton.config(command = self.clickDisconnect)
            self.connectIP.config(state = DISABLED)
            self.connectPort.config(state = DISABLED)
        else:
            self.connectButton.config(text = "Connect")
            self.connectButton.config(command = self.clickConnect)
            self.connectIP.config(state = NORMAL)
            self.connectPort.config(state = NORMAL)
    #def updateConnect
    
    def updateControls(self):
        if self.connected:
            self.updateControlButtons()
        else:
            self.playButton.config(state = DISABLED)
            self.stopButton.config(state = DISABLED)
    #def disableControls
    
    def updateControlButtons(self):
        if self.routineThread is not None:
            self.playButton.config(state = DISABLED)
            self.stopButton.config(state = NORMAL)
        else:
            self.playButton.config(state = NORMAL)
            self.stopButton.config(state = DISABLED)
        self.updatePercentage()
    #def updateControls
    
    def updatePercentage(self):
        while self.routineThread is not None:
            self.progressVar = self.routine.getPercent()
            self.progressBar["value"] = self.progressVar
            if not self.routine.running:
                self.clickStop()
            time.sleep(1.0)
    #def updatePercentage

#class showRobbieGui

c = ShowRobbieGui()
