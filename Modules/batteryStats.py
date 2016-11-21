# *************************************************************
# PROJECT:    ShowRobbieGUI
#
# FILE:       BatteryStats.py
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
from naoqi import ALProxy

class BatteryStats():
    '''
    
    '''
    robotIP = "10.0.0.7"
    robotPort = 9559
    
    batteryProxy = None
    
    def __init__(self):
        '''
        '''
    #def __init__
    
    def connect(self, ip, port):
        self.robotIP = ip
        self.robotPort = port
        self.batteryProxy = ALProxy("ALBattery", self.robotIP, self.robotPort)
        
    def getBatteryPercentage(self):
        return self.batteryProxy.getBatteryCharge()
        
#class BatteryStats