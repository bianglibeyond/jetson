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
# frequency = 200
# the cycle time is roughly around 1.5-2.5 ms, 
# frequency of 200 can make cycle time 5 ms, 
# frequency of 300 can make cycle time 3.3 ms



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
        while userInput not in [str(n) for n in range(len(pins))] and userInput != "q":
            userInput = input("\r\nWrong input!\r\nSelect motor to control(0-{}, enter q to quit): ".format(len(pins)-1))
        if userInput=="q":
            for motor in motors: 
                motor.join()
            while not isMotorsAllShut(motors): 
                pass
            break
        motorNum = int(userInput)
        userInput = input("\r\nSet PWM capacity(0-10): ")
        while userInput not in [str(n) for n in range(11)]:
            userInput = int(input("\r\nWrong input!\r\nSet PWM capacity(0-10): "))
        pwm = int(userInput)

        motorNameSelected = "Motor {}".format(motorNum)
        motorStatus[motorNameSelected]["PWM"] = pwm

        while isMotorsAllPrinted(motors): 
            pass
        # time.sleep(0.01)



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
        # self.duration = 1.0/frequency
        threading.Thread.__init__(self)
        self.isPrint = False
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        print("\r\n{} at Pin{} starts at {}0% capacity.".format(self.motorName, self.pin, self.pwm))
        self.isPrint = True
    def run(self):
        while not self._stopevent.is_set():
            if self.pwm != motorStatus[self.motorName]["PWM"]:
                self.pwm = motorStatus[self.motorName]["PWM"]
                self.isPrint = False
                print("\r\n{} at Pin{} starts at {}0% capacity.".format(self.motorName, self.pin, self.pwm))
                self.isPrint = True
            # startTime = time.time()
            n = 0
            while n<10:
                if n<self.pwm: 
                    GPIO.output(self.pin, GPIO.HIGH)
                else: 
                    GPIO.output(self.pin, GPIO.LOW)
                n += 1
            # timePassed = time.time() - startTime
            # if timePassed<self.duration:
            #     time.sleep(self.duration-timePassed)
            #     # timePassed = time.time() - startTime
            #     # print("\r\n{} at Pin{} has 1 cycle of {}ms".format(self.motorName, self.pin, timePassed*1000))
            # else:
            #     print("\r\n{} at Pin{} overrun DURATION of {}ms!".format(self.motorName, self.pin, self.duration*1000))
    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        


if __name__ == '__main__':
    main()
