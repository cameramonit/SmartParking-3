import RPi.GPIO as GPIO


class Led:
    LED_PIN = 2

    def __init__(self, LED_PIN):
        self.BUZZER_PIN = LED_PIN
        GPIO.setup(LED_PIN, GPIO.OUT)

    def turnOn(self):
        GPIO.output(self.BUZZER_PIN, True)

    def turnOff(self):
        GPIO.output(self.BUZZER_PIN, False)
