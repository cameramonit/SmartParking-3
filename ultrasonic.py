# Libraries
import RPi.GPIO as GPIO
import time


class Ultrasonic:
    TRIGGER = 1
    ECHO = 2

    def __init__(self, TRIGGER, ECHO) -> None:
        self.TRIGGER = TRIGGER
        self.ECHO = ECHO
        GPIO.setup(self.TRIGGER, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def getDistance(self):
        # set Trigger to HIGH
        GPIO.output(self.TRIGGER, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime
        while GPIO.input(self.ECHO) == 0:
            StartTime = time.time()
        # save time of arrival
        while GPIO.input(self.ECHO) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        return distance
    
#Tests
#GPIO.setmode(GPIO.BCM)
#us=Ultrasonic(4,27)
#dis=us.getDistance()
#print(dis)