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
#
# DESCRIPTION
# 
# **************************************************************

# -------------------
# Application imports
# -------------------
from naoqi import ALProxy
import Routine
from Modules.CustomMotions import CustomMotions

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
        self.running = True
        motions = CustomMotions()
        speed = 1.0
        
        if not self.running:
            return
        
        self.currentStep = 0
        try:
            self.autonomousLifeProxy.setState("solitary")
        except Exception, e:
            # Intentionally left empty to let the routine run on an
            # emulated NAO bot through Choreographe
            pass
        motions.standUp(self.postureProxy, self.motionProxy, speed)

        self.currentStep = 1
        async = True
        motions.wave(self.motionProxy, async)
        self.speechProxy.say("Hi there, I'm Robbie. I was built by the Aldebaran company in France, but currently I am the property of the Montana Tech Computer Science Department.")    
            
        if not self.running:
            return
        
        self.currentStep = 2
        self.speechProxy.say("This demonstration is a much shorter version of a performance for prospective visiting students that I have been programmed to deliver by the 2016 17 senior software engineering design project team, Jesse Lieberg and Logan Warner.")
        self.speechProxy.say("One of them can show you some pictures of this performance after I sit back down. I hope you enjoy this year's Techxpo, thank you for listening.")
        
        if not self.running:
            return
        
        self.currentStep = 3
        motions.sitDown(self.postureProxy, self.motionProxy, speed)   
        try:
            self.autonomousLifeProxy.setState("disabled")
        except Exception, e:
            # Intentionally left empty to let the routine run on an
            # emulated NAO bot through Choreographe 
            pass
    
        if not self.running:
            return
        
        self.currentStep = 4
        self.running = False
    #def run

#class TechXpoRoutine
