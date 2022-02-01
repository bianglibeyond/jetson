import RPi.GPIO as GPIO
import threading, time



def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme

    motorPins = [7, 11, 15, 19]

    control = ControlThread(motorPins=motorPins)
    control.start()

    try: 
        while True: pass
    finally:
        GPIO.cleanup()  # cleanup all GPIO
    


class ControlThread(threading.Thread):
    def __init__(self, motorPins):
        self.motorPins = motorPins
        self.numMotors = len(self.motorPins)
        threading.Thread.__init__(self)
        print("Control Panel is ready!")
        self.motorThreads = [MotorThread(jetsonPin=pin, pwmStrength=0) for pin in self.motorPins]
        for motor in self.motorThreads: motor.start()
        while not self.isMotorsAllAlive(): pass
    def run(self):
        while(True):
            while not self.isMotorsAllPrint(): pass
            motorIndex = int(input("\r\nSelect motor to control(0-{}, enter 9 to quit): ".format(self.numMotors)))
            if motorIndex==9: self.shutProgram()
            motorSelected = self.motorThreads[motorIndex]
            pinSelected = self.motorPins[motorIndex]
            pwmStrength = int(input("\r\nSet PWM capacity(0-10): "))
            # for motor in self.motorThreads: motor.join()
            # self.motor1.join()
            motorSelected.join()
            while motorSelected.is_alive(): pass
            newMotor = MotorThread(jetsonPin=pinSelected, pwmStrength=pwmStrength)
            self.motorThreads.insert(motorIndex, newMotor)
            newMotor.start()
    def isMotorsAllAlive(self):
        isAllAlive = True
        for motor in self.motorThreads:
            if not motor.is_alive(): isAllAlive = False 
        return isAllAlive
    def isMotorsAllPrint(self):
        isAllPrint = True
        for motor in self.motorThreads:
            if not motor.isPrint: isAllPrint = False
        return isAllPrint
    def shutProgram(self):
        for motor in self.motorThreads: motor.join()
        self.join()




class MotorThread(threading.Thread):
    def __init__(self, jetsonPin, pwmStrength):
        self._stopevent = threading.Event()
        self.jetsonPin = jetsonPin
        self.pwmStrength = pwmStrength
        threading.Thread.__init__(self)
        self.isPrint = False
    def run(self):
        GPIO.setup(self.jetsonPin, GPIO.OUT)
        GPIO.output(self.jetsonPin, GPIO.LOW)
        print("\r\nMotor at Pin{} starts at {}0% capacity.".format(self.jetsonPin, self.pwmStrength))
        self.isPrint = True
        while not self._stopevent.is_set():
            n = 0
            while n<10:
                if n<self.pwmStrength:
                    GPIO.output(self.jetsonPin, GPIO.HIGH)
                else:
                    GPIO.output(self.jetsonPin, GPIO.LOW)
                n += 1
    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)

if __name__ == '__main__':
    main()
