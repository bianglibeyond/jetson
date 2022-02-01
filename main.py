import RPi.GPIO as GPIO
import threading



def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme

    pins = [7, 11, 19]
    motorNames = ["Motor {}".format(n) for n in range(len(pins))]
    motorStatus = {
        motorNames[n]: {
            "Pin": pins[n], 
            "PWM": 0,
            } 
        for n in (range(len(pins)))
    }

    motors = [MotorThread(motorStatus=motorStatus, motorName=name) for name in motorNames]
    for motor in motors: motor.start()

    # try: 
    while True:
        while not isMotorsAllPrinted(motors): pass
        motorNum = int(input("\r\nSelect motor to control(0-{}, enter 9 to quit): ".format(len(pins)-1)))
        if motorNum==9:
            for motor in motors: motor.join()
            while not isMotorsAllShut(motors): pass
            break
        pwm = int(input("\r\nSet PWM capacity(0-10): "))
        motorNameSelected = "Motor {}".format(motorNum)
        motorStatus[motorNameSelected]["PWM"] = pwm
        motors[motorNum].join()
        while motors[motorNum].is_alive(): pass
        # self.motors[motorNum]._running = False
        newMotor = MotorThread(motorStatus=motorStatus, motorName=motorNameSelected)
        motors[motorNum] = newMotor
        newMotor.start()
    # finally:
    #     GPIO.cleanup()  # cleanup all GPIO



def isMotorsAllPrinted(motors):
    isAllPrinted = True
    for motor in motors:
        if not motor.isPrint: isAllPrinted = False
    return isAllPrinted



def isMotorsAllShut(motors):
    isAllShut = True
    for motor in motors:
        if motor.is_alive(): isAllShut = False
    return isAllShut



class MotorThread(threading.Thread):
    def __init__(self, motorStatus, motorName):
        self._stopevent = threading.Event()
        self.motorName = motorName
        self.pin = motorStatus[self.motorName]["Pin"]
        self.pwm = motorStatus[self.motorName]["PWM"]
        threading.Thread.__init__(self)
        self.isPrint = False
    def run(self):
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        print("\r\n{} at Pin{} starts at {}0% capacity.".format(self.motorName, self.pin, self.pwm))
        self.isPrint = True
        while not self._stopevent.is_set():
            n = 0
            while n<10:
                if n<self.pwm: GPIO.output(self.pin, GPIO.HIGH)
                else: GPIO.output(self.pin, GPIO.LOW)
                n += 1
    def join(self, timeout=None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)
        


if __name__ == '__main__':
    main()



# import RPi.GPIO as GPIO
# import threading, time



# def main():
#     # Pin Setup:
#     GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme

#     pins = [7, 11, 19]
#     motorStatus = {
#         "Motor {}".format(n): {
#             "Pin": pins[n], 
#             "PWM": 0,
#             } 
#         for n in (range(len(pins)))
#     }

#     control = ControlThread(motorStatus=motorStatus)
#     control.start()

#     try: 
#         while control.is_alive(): pass
#     finally:
#         GPIO.cleanup()  # cleanup all GPIO



# class ControlThread(threading.Thread):
#     def __init__(self, motorStatus):
#         self.motorStatus = motorStatus
#         self.numMotors = len(self.motorStatus.items())
#         self.motorNames = [status[0] for status in self.motorStatus.items()]
#         threading.Thread.__init__(self)
#         print("Control Panel is ready!")
#         self.motors = [MotorThread(pin=self.motorStatus[motor]["Pin"], pwm=self.motorStatus[motor]["PWM"]) for motor in self.motorNames]
#         for motor in self.motors: motor.start()
#     def run(self):
#         while True:
#             while not self.isMotorsAllPrint(): pass
#             motorNum = int(input("\r\nSelect motor to control(0-{}, enter 9 to quit): ".format(self.numMotors-1)))
#             if motorNum==9:
#                 for motor in self.motors: motor.join()
#                 while not self.isMotorsAllShut: pass
#                 return
#             pwm = int(input("\r\nSet PWM capacity(0-10): "))
#             motorSelected = "Motor {}".format(motorNum)
#             self.motorStatus[motorSelected]["PWM"] = pwm
#             self.motors[motorNum].join()
#             while self.motors[motorNum].is_alive(): pass
#             # self.motors[motorNum]._running = False
#             newMotor = MotorThread(pin=self.motorStatus[motorSelected]["Pin"], pwm=self.motorStatus[motorSelected]["PWM"])
#             self.motors[motorNum] = newMotor
#             newMotor.start()
#     def isMotorsAllPrint(self):
#         isAllPrint = True
#         for motor in self.motors:
#             if not motor.isPrint: isAllPrint = False
#         return isAllPrint
#     def isMotorsAllShut(self):
#         isAllShut = True
#         for motor in self.motors:
#             if motor.is_alive(): isAllShut = False
#         return isAllShut



# class MotorThread(threading.Thread):
#     def __init__(self, pin, pwm):
#         self._stopevent = threading.Event()
#         self.pin = pin
#         self.pwm = pwm
#         threading.Thread.__init__(self)
#         self.isPrint = False
#     def run(self):
#         GPIO.setup(self.pin, GPIO.OUT)
#         GPIO.output(self.pin, GPIO.LOW)
#         print("\r\nMotor at Pin{} starts at {}0% capacity.".format(self.pin, self.pwm))
#         self.isPrint = True
#         while not self._stopevent.is_set():
#             n = 0
#             while n<10:
#                 if n<self.pwm: GPIO.output(self.pin, GPIO.HIGH)
#                 else: GPIO.output(self.pin, GPIO.LOW)
#                 n += 1
#     def join(self, timeout=None):
#         self._stopevent.set()
#         threading.Thread.join(self, timeout)
        


# if __name__ == '__main__':
#     main()




# import RPi.GPIO as GPIO
# import threading, time



# def main():
#     # Pin Setup:
#     GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme

#     pins = [7, 11, 19]
#     motorStatus = {
#         "Motor {}".format(n): {
#             "Pin": pins[n], 
#             "PWM": 0,
#             } 
#         for n in (range(len(pins)))
#     }

#     control = ControlThread(motorStatus=motorStatus)
#     control.start()

#     try: 
#         while control.is_alive(): pass
#     finally:
#         GPIO.cleanup()  # cleanup all GPIO



# class ControlThread(threading.Thread):
#     def __init__(self, motorStatus):
#         self.motorStatus = motorStatus
#         self.numMotors = len(self.motorStatus.items())
#         # self.motorNames = [status[0] for status in self.motorStatus.items()]
#         threading.Thread.__init__(self)
#         print("Control Panel is ready!")
#         self.motors = MotorThread(self.motorStatus)
#         self.motors.start()
#     def run(self):
#         while True:
#             while not self.motors.isPrint: pass
#             motorNum = int(input("\r\nSelect motor to control(0-{}, enter 9 to quit): ".format(self.numMotors-1)))
#             if motorNum==9:
#                 self.motors.join()
#                 while self.motors.is_alive(): pass
#                 return
#             pwm = int(input("\r\nSet PWM capacity(0-10): "))
#             motorSelected = "Motor {}".format(motorNum)
#             self.motorStatus[motorSelected]["PWM"] = pwm
#             self.motors.join()
#             while self.motors.is_alive(): pass
#             self.motors = MotorThread(self.motorStatus)
#             self.motors.start()


# class MotorThread(threading.Thread):
#     def __init__(self, motorStatus):
#         self._stopevent = threading.Event()
#         self.motorStatus = motorStatus
#         self.motorNames = [status[0] for status in self.motorStatus.items()]
#         threading.Thread.__init__(self)
#         self.isPrint = False
#     def run(self):
#         for motor in self.motorNames:
#             pin = self.motorStatus[motor]["Pin"]
#             pwm = self.motorStatus[motor]["PWM"]
#             GPIO.setup(pin, GPIO.OUT)
#             GPIO.output(pin, GPIO.LOW)
#             print("\r\nMotor at Pin{} starts at {}0% capacity.".format(pin, pwm))
#         self.isPrint = True
#         while not self._stopevent.is_set():
#             n = 0
#             while n<10:
#                 for motor in self.motorNames:
#                     pin = self.motorStatus[motor]["Pin"]
#                     pwm = self.motorStatus[motor]["PWM"]
#                     if n<pwm: GPIO.output(pin, GPIO.HIGH)
#                     else: GPIO.output(pin, GPIO.LOW)
#                 n += 1
#     def join(self, timeout=None):
#         self._stopevent.set()
#         threading.Thread.join(self, timeout)
        


# if __name__ == '__main__':
#     main()
