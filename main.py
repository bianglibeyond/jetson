import RPi.GPIO as GPIO
import time

# Pin Definitons:
motorPin12 = 12  # BOARD pin 12

def main():
    prev_value = None

    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(motorPin12, GPIO.OUT)

    curr_sig = GPIO.LOW
    oppo_sig = GPIO.HIGH
    GPIO.output(motorPin12, curr_sig)
    print("Starting demo now! Press CTRL+C to exit")
    try:
        while True:
            GPIO.output(motorPin12, oppo_sig)
            temp = oppo_sig
            oppo_sig = curr_sig
            curr_sig = temp
            print("Outputting {} to Pin {}".format(curr_sig, motorPin12))
            time.sleep(1)
    finally:
        GPIO.cleanup()  # cleanup all GPIO

if __name__ == '__main__':
    main()