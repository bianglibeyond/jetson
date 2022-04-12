from random import randint
import RPi.GPIO as GPIO
import threading, time, random



# Global variables for cross-thread communication
pins = [7, 11, 19, 21, 22, 23, 24, 26, 29, 31]
# pinsLeftHand = pins[0:5]
# pinsRightHand = pins[5:10]
motorNames = ["Motor {}".format(n) for n in range(len(pins))]
motorStatus = {
        motorNames[n]: {
            "Pin": pins[n], 
            "PWM": 0,
            } 
        for n in (range(len(pins)))
    }



def main():

    global motorStatus

    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme

    motors = [MotorThread(motorName=name) for name in motorNames]
    for motor in motors: motor.start()

    while True:
        
        while not isMotorsAllPrinted(motors): 
            pass

        # Random Fingers
        # leftHandFingersWithMotor = [i for i in range(0, 5)]
        # rightHandFingersWithMotor = [i for i in range(5, 10)]
        # numLeftHandFingers = randint(0, 2)
        # numRightHandFingers = randint(0, 2)
        # pwm = 5
        # leftHandFingers = random.sample(leftHandFingersWithMotor, numLeftHandFingers)
        # rightHandFingers = random.sample(rightHandFingersWithMotor, numRightHandFingers)
        # fingers = leftHandFingers + rightHandFingers
        # for finger in fingers: 
        #     motorNameSelected = "Motor {}".format(finger)
        #     motorStatus[motorNameSelected]["PWM"] = pwm
        # time.sleep(1)
        # for n in range(10):
        #     motorNameSelected = "Motor {}".format(n)
        #     motorStatus[motorNameSelected]["PWM"] = 0
        # time.sleep(0.5)

        # Python 3
        # userInput = input("\r\nSelect motor to control(0-{}, but only 0-2 are valid now, enter q to quit): ".format(len(pins)-1))
        # while userInput not in [str(n) for n in range(len(pins))] and userInput != "q":
        #     userInput = input("\r\nWrong input!\r\nSelect motor to control(0-{}, enter q to quit): ".format(len(pins)-1))
        # if userInput=="q":
        #     for motor in motors: 
        #         motor.join()
        #     while not isMotorsAllShut(motors): 
        #         pass
        #     break
        # motorNum = int(userInput)
        # userInput = input("\r\nSet PWM capacity(0-10): ")
        # while userInput not in [str(n) for n in range(11)]:
        #     userInput = input("\r\nWrong input!\r\nSet PWM capacity(0-10): ")

        # Python 2
        userInput = raw_input("\r\nSelect motor to control(0-{}, but only 0-2 are valid now, enter q to quit): ".format(len(pins)-1))
        while userInput not in [str(n) for n in range(len(pins))] and userInput != "q":
            userInput = raw_input("\r\nWrong input!\r\nSelect motor to control(0-{}, enter q to quit): ".format(len(pins)-1))
        if userInput=="q":
            for motor in motors: 
                motor.join()
            while not isMotorsAllShut(motors): 
                pass
            break
        motorNum = int(userInput)
        userInput = raw_input("\r\nSet PWM capacity(0-10): ")
        while userInput not in [str(n) for n in range(11)]:
            userInput = raw_input("\r\nWrong input!\r\nSet PWM capacity(0-10): ")

        pwm = int(userInput)

        motorNameSelected = "Motor {}".format(motorNum)
        motorStatus[motorNameSelected]["PWM"] = pwm

        print("\r\n{} at Pin {} is set at {}0% capacity.".format(motorNameSelected, motorStatus[motorNameSelected]["Pin"], pwm))

        
        


def isMotorsAllPrinted(motors):
    isAllPrinted = True
    for motor in motors:
        if not motor.isPrint: 
            isAllPrinted = False
    return isAllPrinted



def isMotorsAllShut(motors):
    isAllShut = True
    for motor in motors:
        if motor.is_alive(): 
            isAllShut = False
    return isAllShut



class MotorThread(threading.Thread):
    def __init__(self, motorName):
        global motorStatus
        self._stopevent = threading.Event()
        self.motorName = motorName
        self.pin = motorStatus[self.motorName]["Pin"]
        self.pwm = motorStatus[self.motorName]["PWM"]
        threading.Thread.__init__(self)
        self.isPrint = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        print("\r\n{} at Pin {} starts at {}0% capacity.".format(self.motorName, self.pin, self.pwm))
        self.isPrint = True
    def run(self):
        while not self._stopevent.is_set():
            self.pwm = motorStatus[self.motorName]["PWM"]
            n = 0
            while n<10:
                if n<self.pwm: 
                    GPIO.output(self.pin, GPIO.HIGH)
                else: 
                    GPIO.output(self.pin, GPIO.LOW)
                n += 1
    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        


if __name__ == '__main__':
    main()