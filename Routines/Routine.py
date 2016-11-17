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
from abc import ABCMeta, abstractmethod

class Routine(object):
    '''
    
    '''
    __metaclass__ = ABCMeta
    
    progressVar = None
    
    numberSteps = -1    
    currentStep = 0
        
    def __init__(self):
        '''
        Default constructor
        '''
    #def __init__
    
    @abstractmethod
    def connect(self, ip, port):
        return
    #def connect
        
    @abstractmethod
    def run(self):
        return
    #def run
    
    @abstractmethod
    def stop(self):
        return
    #def stop
    
    def getPercent(self):
        print(str(self.currentStep) + "," + str(self.numberSteps))
        return self.currentStep / float(self.numberSteps) * 100
    #def getPercent
    
#class Routine