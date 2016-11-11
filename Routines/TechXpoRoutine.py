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
from naoqi import ALProxy
import Routine
from Modules.customMotions import customMotions


class TechXpoRoutine(Routine.Routine):
    '''
    classdocs
    '''
    robotIP = "10.0.0.7"
    robotPort = 9559
    
    postureProxy = None
    motionProxy = None
    speechProxy = None
    autonomousLifeProxy = None    

    def __init__(self):
        '''
        Constructor
        '''
        self.numberSteps = 4
    #def __init__

    def connect(self, ip, port):
        self.robotIP = ip
        self.robotPort = port
        
        self.postureProxy = ALProxy("ALRobotPosture", self.robotIP, self.robotPort)
        self.motionProxy = ALProxy("ALMotion", self.robotIP, self.robotPort)
        self.speechProxy = ALProxy("ALTextToSpeech", self.robotIP, self.robotPort)
        self.autonomousLifeProxy = ALProxy("ALAutonomousLife", self.robotIP, self.robotPort)
    #def connect

    def run(self):
        motions = customMotions()
        speed = 1.0
        
        self.currentStep = 1
        #self.autonomousLifeProxy.setState("solitary")
        motions.standUp(self.postureProxy, self.motionProxy, speed)
        
        self.currentStep = 2
        async = True
        motions.wave(self.motionProxy, async)        
        
        self.currentStep = 3
        self.speechProxy.say("Hello, I am Robbie. I'm a NAO robot.")
        self.speechProxy.say("I'm designed and manufactured by the Aldebaran company in France, but all my present behaviors have been programmed as part of a Senior Software Engineering project.")
        self.speechProxy.say("There's very little I can do without the programs that have designed and constructed by the Senior Software Engineering students here at Montana Tech.")
        self.speechProxy.say("I'm afraid that programming me is not easy, but these students have been well equipped by their education here at Tech to deal with complex problems.")
        
        self.currentStep = 4
        motions.sitDown(self.postureProxy, self.motionProxy, speed)    
        #self.autonomousLifeProxy.setState("disabled")
    #def run

    def stop(self):
        return
    #def stop

#class TechXpoRoutine
