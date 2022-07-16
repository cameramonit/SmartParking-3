import RPi.GPIO as GPIO
import time

class Led:
    LED_PIN = 2

    def __init__(self, LED_PIN):
        self.LED_PIN = LED_PIN
        GPIO.setup(LED_PIN, GPIO.OUT)

    def turnOn(self):
        GPIO.output(self.BUZZER_PIN, True)

    def turnOff(self):
        GPIO.output(self.BUZZER_PIN, False)


#Tests
#GPIO.setmode(GPIO.BCM)
#led=Led(4)
#led.turnOn()
#time.sleep(9)
#led.turnOff()
