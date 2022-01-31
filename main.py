import RPi.GPIO as GPIO
import time

# Pin Definitons:
motorPin12 = 12  # BOARD pin 12

def main():
    pwmStrength = 2
    pwmTimeUnit = 0.001

    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(motorPin12, GPIO.OUT)
    GPIO.output(motorPin12, GPIO.LOW)
    print("Starting demo now! Press CTRL+C to exit")
    try:
        isPWM = True
        while True:
            
            if isPWM:
                for round in range(10):
                    # 10ms as a round, 100 in total is 1s
                    n = 0
                    while n<10:
                        if n<pwmStrength:
                            curr_sig = GPIO.HIGH
                            GPIO.output(motorPin12, curr_sig)
                        else:
                            curr_sig = GPIO.LOW
                            GPIO.output(motorPin12, curr_sig)
                        n += 1
                        time.sleep(0.01)
                isPWM = not isPWM
                print("Outputting {} to Pin {}".format(pwmStrength, motorPin12))
            else:
                GPIO.output(motorPin12, GPIO.HIGH)
                isPWM = not isPWM
                print("Outputting {} to Pin {}".format(10, motorPin12))
                time.sleep(1)
            
            print("\r\nTime is {}\r\n".format(time.now))
    finally:
        GPIO.cleanup()  # cleanup all GPIO



# def setMotorPinPWM(pin, )

if __name__ == '__main__':
    main()