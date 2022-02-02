import RPi.GPIO as GPIO
import threading, time



# Global variables for cross-thread communication
pins = [7, 11, 19, 21, 22, 23, 24, 26, 29, 31, 32, 33, 35, 36, 37, 38, 40]
motorNames = ["Motor {}".format(n) for n in range(len(pins))]
motorStatus = {
        motorNames[n]: {
            "Pin": pins[n], 
            "PWM": 0,
            } 
        for n in (range(len(pins)))
    }
frequency = 50



def main():

    global motorStatus

    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme

    motors = [MotorThread(motorName=name) for name in motorNames]
    for motor in motors: 
        motor.start()

    while True:
        
        while not isMotorsAllPrinted(motors): 
            pass
        userInput = input("\r\nSelect motor to control(0-{}, but only 0-2 are valid now, enter q to quit): ".format(len(pins)-1))
        while userInput not in range(len(pins)) and userInput != "q":
            userInput = input("\r\nWrong input!\r\nSelect motor to control(0-{}, enter q to quit): ".format(len(pins)-1))
        if userInput=="q":
            for motor in motors: 
                motor.join()
            while not isMotorsAllShut(motors): 
                pass
            break
        motorNum = int(userInput)
        userInput = int(input("\r\nSet PWM capacity(0-10): "))
        while userInput not in range(11):
            userInput = int(input("\r\nWrong input!\r\nSet PWM capacity(0-10): "))
        pwm = int(userInput)

        motorNameSelected = "Motor {}".format(motorNum)
        motorStatus[motorNameSelected]["PWM"] = pwm



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
        global motorStatus, frequency
        self._stopevent = threading.Event()
        self.motorName = motorName
        self.pin = motorStatus[self.motorName]["Pin"]
        self.pwm = motorStatus[self.motorName]["PWM"]
        self.duration = 1.0/frequency
        threading.Thread.__init__(self)
        self.isPrint = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        print("\r\n{} at Pin{} starts at {}0% capacity.".format(self.motorName, self.pin, self.pwm))
        self.isPrint = True
    def run(self):
        while not self._stopevent.is_set():
            self.pwm = motorStatus[self.motorName]["PWM"]
            startTime = time.time()
            n = 0
            while n<10:
                if n<self.pwm: 
                    GPIO.output(self.pin, GPIO.HIGH)
                else: 
                    GPIO.output(self.pin, GPIO.LOW)
                n += 1
            timePassed = time.time() - startTime
            print("\r\n{} at Pin{} has 1 cycle of {}ms".format(self.motorName, self.pin, self.duration*100))
            if timePassed<self.duration:
                time.sleep(self.duration-timePassed)
            else:
                print("\r\n{} at Pin{} overrun DURATION of {}ms!".format(self.motorName, self.pin, self.duration*100))
    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        


if __name__ == '__main__':
    main()
