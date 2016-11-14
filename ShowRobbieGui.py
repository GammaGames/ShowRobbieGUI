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
    
    batteryBar = None
    
    controlsFrame = None
    videoFeed = None
    videoFeedLabel = None
    playButton = None
    stopButton = None
    progressBar = None
    
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
            yscrollcommand = self.availableRoutinesScrollbar.set)
        
        # Create connection components
        self.connectFrame = Frame(self.window)
        self.connectLabel = Label(self.connectFrame, text="Connection")
        self.connectIP = Entry(self.connectFrame, textvariable = "10.0.0.7 ")
        self.connectPort = Entry(self.connectFrame, textvariable = "9559")
        self.connectButton = Button(self.connectFrame, text = "Connect")
        
        # Create control components
        self.controlsFrame = Frame(self.window)
        self.videoFeed = PhotoImage(file="img/placeholder_image.gif")
        self.videoFeedLabel = Label(self.controlsFrame, image = self.videoFeed)
        self.playButton = Button(self.controlsFrame, text = "Play")
        self.stopButton = Button(self.controlsFrame, text = "Stop")
        self.progressBar = Progressbar(self.controlsFrame, orient = HORIZONTAL, mode = "determinate")
        
        # Set component options
        self.window.wm_title("ShowRobbie")
        self.window.minsize(width=1024, height=728)
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
        
        self.routinesFrame.grid(column = 0, row = 0, rowspan = 2, sticky = W+N+S)
        
        # Pack connection stuff
        self.connectLabel.pack(side = TOP, expand = True, fill = X)
        self.connectIP.pack(side = LEFT)
        self.connectPort.pack(side = LEFT)
        self.connectButton.pack(side = LEFT)
        #self.videoFeedLabel.pack(side = BOTTOM)
        
        self.connectFrame.grid(column = 1, row = 0, sticky = N+E+W)
        
        # Pack progress stuff
        self.progressBar.pack(side = BOTTOM, expand = True, fill = X)
        self.playButton.pack(side = LEFT, fill = X)
        self.stopButton.pack(side = RIGHT, fill = X)
        
        self.controlsFrame.grid(column = 1, row = 1, sticky = S+W+E)
        
    #def packAndConfigureWindow                              
    
    def main(self):
        print "heh"
    #def main

#class showRobbieGui

c = ShowRobbieGui()
