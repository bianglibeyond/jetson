import RPi.GPIO as GPIO
import threading



def main():
    pwmStrength = 0

    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme

    motor1 = MotorThread(name="Motor1", jetsonPin=12, pwmStrength=pwmStrength)
    motor1.run()

    try:
        while True:
            pwmStrength = int(input("Set PWM capacity(0-10): "))
            motor1.join()
            while motor1.is_alive():
                pass
            motor1 = MotorThread(name="Motor1", jetsonPin=12, pwmStrength=pwmStrength)
            motor1.run()
            print("Outputting {} to Pin {}".format(pwmStrength, 12))
    finally:
        GPIO.cleanup()  # cleanup all GPIO
    


class MotorThread(threading.Thread):
    def __init__(self, name, jetsonPin, pwmStrength):
        self._stopevent = threading.Event()
        self._sleepperiod = 1.0
        threading.Thread.__init__(self, name=name)
        self.jetsonPin = jetsonPin
        self.pwmStrength = pwmStrength
    def run(self):
        GPIO.setup(self.jetsonPin, GPIO.OUT)
        GPIO.output(self.jetsonPin, GPIO.LOW)
        print("Motor at Pin{} starts.".format(self.jetsonPin))
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