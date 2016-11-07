# *******************************************************
# PROJECT:
#
# EXECUTION ENVIRONMENTS:
# Python 2.7 on Windows 7
#
# AUTHORS: Unknown, Logan Warner
#
# DESCRIPTION: Convenience functions for moving the robot
# *******************************************************

# --------------
# Python imports
# --------------
import time
import math

# -------------------
# Application imports
# -------------------
import NaoMarkModule
from naoqi import ALModule
from naoqi import ALProxy

# ----------------
# Global constants
# ----------------
robotIP = "10.0.0.7"
PORT = 9559
naomarkSize = .12
stepArray = [["StepHeight", 0.015],["MaxStepX", 0.02], ["MaxStepTheta", .18]]

# ----------------
# Global variables
# ----------------
postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
lifeProxy = ALProxy("ALAutonomousLife", robotIP, PORT)
tts = ALProxy("ALTextToSpeech", robotIP, PORT)
motionProxy = ALProxy("ALMotion", robotIP, PORT)
curAngle = 0
BotFreezer = None
cmModule = None


class CustomMotions(ALModule):
    """A module for all the motions defined by the Senior Design team"""

    def turnLeft(self, degreesPR):
        motionProxy.moveInit()
        motionProxy.setMoveArmsEnabled(True, True)
        time.sleep(1)
        motionProxy.moveTo(0, 0, math.radians(degreesPR), stepArray)

    def turnRight(self, degreesPr):
        self.turnLeft(-degreesPr)

    def turnAround(self, directionrPR="left"):
        if directionrPR is "left":
            self.turnLeft(180)
        else:
            self.turnRight(180)

    def lookAround(self):
        motionProxy.moveInit()
        time.sleep(1)

        names = "HeadYaw"
        angleLists = [1.0, -1.0, 1.0, -1.0, 0.0]
        times = [1.0,  2.0, 3.0,  4.0, 5.0]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)

    def lookTo(self, angle):
        motionProxy.moveInit()
        time.sleep(1)

        motionProxy.changeAngles("HeadYaw", angle, .1)

    def lookAroundForMark(self, markNumPR=None):
        motionProxy.moveInit()
        time.sleep(1)

        names = "HeadYaw"
        markFound = False
        angleLists = .25
        back = False
        markData = NaoMarkModule.getMarkData(robotIP, PORT)
        first = True

        while not markFound:

            if back:
                angleLists = angleLists -.125
            else:
                angleLists = angleLists + .125

            if angleLists > 1.0:
                angleLists = 1.0
                back = True
            else:
                if angleLists < -1.0:
                    angleLists = -1.0
                    back = False

            times = .15
            if first:
                times = 1.0
            isAbsolute = True
            motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)

            markData = NaoMarkModule.getMarkData(robotIP, PORT)

            if not (markData is None or len(markData) == 0):
                if markNumPR is None or (NaoMarkModule.getMarkNumber(markData) == markNumPR):
                    markFound = True
            first = False
        return markData

    def lookAroundForMarkMoving(self, number):
        motionProxy.moveInit()
        time.sleep(1)

        names = "HeadYaw"
        markFound = False
        angleLists = .25
        back = False
        markData = NaoMarkModule.getMarkData(robotIP, PORT)
        first = True
        attempts = 0

        while not markFound:
            # TODO REPLACE THIS NONSENSE
            if attempts >=2:
                return None
            if back:
                angleLists = angleLists -.125
            else:
                angleLists = angleLists + .125

            if angleLists > 1.0:
                angleLists = 1.0
                back = True
                attempts = attempts + 1
            else:
                if angleLists < -1.0:
                    angleLists = -1.0
                    back = False

            times = .15
            if first:
                times = 1.0
            isAbsolute = True
            motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)

            markData = NaoMarkModule.getMarkData(robotIP, PORT)

            if not (markData is None or len(markData) == 0):
                if NaoMarkModule.getMarkNumber(markData) == number:
                    markFound = True
            first = False
        return markData

    def detectMarkSearch(self, number, directionPR="forward"):
        markD = None
        searching = True
        global naomarkSize
        global robotIP
        global PORT
        while searching:
            markD = CustomMotions.lookAroundForMarkMoving(self, number)
            if not (markD is None or len(markD) == 0):
                print "found something"
                searching = False
            else:
                print "tried turn"
                CustomMotions.turnRight30(self)

        x, y, z = NaoMarkModule.getMarkXYZ(robotIP, PORT, markD, naomarkSize)

        if directionPR == "l":
            CustomMotions.moveForwardY(self, x, y + .35)
        elif directionPR == "s":
            CustomMotions.moveForwardY(self, x, y - .35)
        else:
            CustomMotions.moveForwardY(self, x, y)

    def turnToHeadStraight(self, markData):
        motionProxy.moveInit()
        time.sleep(1)
        global curAngle

        angle = motionProxy.getAngles("HeadYaw", False)
        print angle[0]

        motionProxy.moveTo(0, 0, angle[0])
        print "Moved to head straight"

    def detectMarkWalkStraight(self):
        markD = CustomMotions.lookAroundForMark(self)
        global naomarkSize
        CustomMotions.turnToHeadStraight(self, markD)
        CustomMotions.detectMarkAndMoveTo(self)

    # non-0 theta is strafing according to old code
    def moveForward(self, distance, y=0, theta=0):
        motionProxy.moveInit()
        motionProxy.setMoveArmsEnabled(True, True)
        time.sleep(1)
        print "moving x:" + str(distance) + "y " + str(y)
        motionProxy.moveTo(distance, y, theta, stepArray)

    def wave(self):
        names = ["RShoulderRoll", "RShoulderPitch", "RElbowYaw", "RWristYaw", "RElbowRoll"]

        motionProxy.openHand("RHand")
        angleLists = [[-75.0], [0.0], [60.0], [60.0], [0.0, 87.0, 0.0, 87.0]]
        [[math.radians(angle) for angle in x] for x in angleLists]
        timeLists = [[1.0], [1.0], [1.0], [1.0], [1.0, 1.5, 2.0, 2.5]]
        isAbsolute = True
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

        names = ["RShoulderRoll", "RShoulderPitch", "RElbowYaw","RWristYaw", "RElbowRoll"]
        angleLists = [0.0, 100.0, 0.0, 0.0, 3.0]
        [math.radians(x) for x in angleLists]
        timeLists = [[1.0], [1.0], [1.0], [1.0], [1.0]]
        isAbsolute = True
        motionProxy.closeHand("RHand")
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

    def fistBump(self):
        time.sleep(1)
        names = ["RShoulderRoll", "RShoulderPitch", "RElbowRoll"]
        motionProxy.setStiffnesses("Body", 1)
        motionProxy.closeHand("RHand")
        angleLists = [0.0, -30.0, 3.0]
        [math.radians(x) for x in angleLists]
        timeLists = [[1.0], [1.0], [1.0]]
        isAbsolute = True
        tts.say("Pound it")
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

        motionProxy.post.openHand("RHand")
        angleLists = [-50.0, -10.0, 86.0]
        [math.radians(x) for x in angleLists]
        timeLists = [[1.0], [1.0], [1.0]]
        isAbsolute = True
        motionProxy.post.angleInterpolation(names, angleLists, timeLists, isAbsolute)
        tts.say("balalalalalala")

    # TODO figure out why x has .15 subtracted (hardcoded robot height?)
    # many of them did not subtract from x at all
    def detectMarkAndMoveTo(self, markNumPR=None, offsetY=0):
        markD = CustomMotions.lookAroundForMark(self, markNumPR)
        x, y, z = NaoMarkModule.getMarkXYZ(robotIP, PORT, markD, naomarkSize)
        CustomMotions.moveForward(self, x - .15, y + offsetY)

#end motionsWLS.py