import RPi.GPIO as GPIO
import threading, time



def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme

    control = ControlThread()
    control.start()

    try: 
        while True: pass
    finally:
        GPIO.cleanup()  # cleanup all GPIO
    


class ControlThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Control Panel is ready!")
        self.motor1 = MotorThread(jetsonPin=12, pwmStrength=0)
        self.motor1.start()
        while not self.motor1.is_alive(): pass
    def run(self):
        while(True):
            while not self.motor1.isPrint: pass
            pwmStrength = int(input("\r\nSet PWM capacity(0-10): "))
            self.motor1.join()
            while self.motor1.is_alive(): pass
            self.motor1 = MotorThread(jetsonPin=12, pwmStrength=pwmStrength)
            self.motor1.start()
            print("Outputting {} to Pin {}".format(pwmStrength, 12))



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
        print("\r\nMotor at Pin{} starts at {}%% capacity.".format(self.jetsonPin, self.pwmStrength))
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