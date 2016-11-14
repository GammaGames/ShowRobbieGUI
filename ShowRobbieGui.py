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
    
    availableRoutinesLabel = None
    availableRoutines = None
    availableRoutinesScrollbar = None
    
    connectLabel = None
    connectIP = None
    connectPort = None
    connectButton = None
    videoFeed = None
    batteryBar = None
    
    progressBar = None
    playButton = None
    stopButton = None
    
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
        self.availableRoutinesLabel = Label(self.window, text="Routines")
        self.availableRoutinesScrollbar = Scrollbar(self.window)
        self.availableRoutines = Listbox(self.window, 
            yscrollcommand = self.availableRoutinesScrollbar.set)
        
        # Create connection components
        self.connectLabel = Label(self.window, text="Connect")
        self.connectIP = Entry(self.window, textvariable = "10.0.0.7 ")
        self.connectPort = Entry(self.window, textvariable = "9559")
        self.connectButton = Button(self.window, text = "Connect")
        
        # Create control components
        self.playButton = Button(self.window, text = unichr(9658))
        self.stopButton = Button(self.window, text = unichr(9642))
        self.progressBar = Progressbar(self.window, orient = HORIZONTAL, mode = "determinate")
        
        # Set component options0 
        self.window.wm_title("ShowRobbie")
        self.window.minsize(width=512, height=512)
        #self.window.resizable(width=False, height=False)
        
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
        self.availableRoutinesLabel.grid(row = 0, column = 0, sticky = W)
        self.availableRoutines.grid(row = 1, column = 0, rowspan = 4, 
            sticky = N+W+S)
        self.availableRoutinesScrollbar.grid(row = 1, column = 1, rowspan = 4, 
            sticky = N+W+S)
        
        # Pack connection stuff
        self.connectLabel.grid(row = 0, column = 1, sticky = W)
        self.connectIP.grid(row = 1, column = 1, sticky = W)
        self.connectPort.grid(row = 1, column = 2, sticky = W)
        self.connectButton.grid(row = 1, column = 3, sticky = E)
        
        #Pack progress stuff
        self.playButton.grid(row = 3, column = 1)
        self.stopButton.grid(row = 3, column = 2)
        self.progressBar.grid(row = 4, column = 1, rowspan = 2)
        
    #def packAndConfigureWindow                              
    
    def main(self):
        print "heh"
    #def main

#class showRobbieGui

c = ShowRobbieGui()
