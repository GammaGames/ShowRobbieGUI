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
# 11/2/16     Jesse Lieberg      Initial Creation
#
# DESCRIPTION
# 
# **************************************************************

# -------------------
# Application imports
# -------------------
import os
import glob
from Tkinter import *
from ttk import *
from Routines import Routine

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
    
    routines = {}
    routineFilesToIgnore = {
        "Routine.py",
        "__init__.py"
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
        self.connectButton = Button(self.connectFrame, text = "Connect")
        
        # Create stats components (battery, video)
        self.batteryFrame = Frame(self.window)
        self.videoFeed = PhotoImage(master = self.batteryFrame, 
            file="img/placeholder_image.gif")
        self.videoFeedLabel = Label(self.batteryFrame, image = self.videoFeed)
        self.batteryVar = DoubleVar()
        self.batteryLabel = Label(self.batteryFrame, text="0%")
        self.batteryBar = Progressbar(self.batteryFrame, orient = VERTICAL, 
            mode = "determinate", variable = self.batteryVar, length = 30)
        
        # Create control components
        self.controlsFrame = Frame(self.window)
        self.playButton = Button(self.controlsFrame, text = "Run", 
            state = DISABLED)
        self.stopButton = Button(self.controlsFrame, text = "Stop",
            state = DISABLED)
        self.progressVariable = DoubleVar()
        self.progressBar = Progressbar(self.controlsFrame, orient = HORIZONTAL, 
           mode = "determinate", variable = self.progressVar, length = 600)
        
        # Set component options
        self.window.wm_title("ShowRobbie")
        self.window.minsize(width=700, height=500)
        self.window.resizable(width=False, height=False)
        
        # Create array of available routines
        self.routines = glob.glob("Routines/*.py")
        self.routines = [os.path.split(p)[1] for p in self.routines]
        
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
    
    def clickPlay(self):
        print "play"
    #def clickPlay
    
    def clickStop(self):
        print "stop"
    #def clickStop
    
    def updateUi(self):
        if self.connected:
            print "connected"
        else:
            print "disconnected"
    #def updateUi
    
    def updateImage(self):
        print "updating image"
    #def updateImage
    
    def main(self):
        print "heh"
    #def main

#class showRobbieGui

c = ShowRobbieGui()
