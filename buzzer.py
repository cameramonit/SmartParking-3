import RPi.GPIO as GPIO


class Buzzer:
    BUZZER_PIN = 2

    def __init__(self, BUZZER_PIN):
        self.BUZZER_PIN = BUZZER_PIN
        GPIO.setup(BUZZER_PIN, GPIO.OUT)

    def makeSound(self):
        GPIO.output(self.BUZZER_PIN, True)

    def stopSound(self):
        GPIO.output(self.BUZZER_PIN, False)
