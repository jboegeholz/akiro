import RPi.GPIO as GPIO
import time
import os

SHUTDOWN_PIN = 17

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        while True:
            if GPIO.input(SHUTDOWN_PIN) == GPIO.LOW:
                print("Shutdown Raspberry...")
                os.system("sudo shutdown now")
                break
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
