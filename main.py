import time
import os
import RPi.GPIO as GPIO

from cloudconnect import cloud
from ultrasonic import Ultrasonic
from led import Led
from camera import Camera
from licenseplate import LicensePlate
from buzzer import Buzzer
from firebase_admin import firestore


LED_PIN1 = 1
LED_PIN2 = 1
LED_PIN3 = 1
BUZZER_PIN1 = 1
BUZZER_PIN2 = 1
BUZZER_PIN3 = 1

SERVO_PIN1 = 1
SERVO_PIN2 = 1

TRIGGER_PIN1 = 1
ECHO_PIN1 = 1
TRIGGER_PIN2 = 1
ECHO_PIN2 = 1
TRIGGER_PIN3 = 1
ECHO_PIN31 = 1

FIRST_SLOT_NO = 1
LAST_SLOT_NO = 4

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    usarray=[]
    usarray.append(Ultrasonic(2,3))
    usarray.append(Ultrasonic(27,22))
    usarray.append(Ultrasonic(10,9))
    
    us0=usarray[2].getDistance()

    c=cloud('smartparkingsystem-5ffb7-2f4717e68ead.json', FIRST_SLOT_NO, LAST_SLOT_NO,firestore.firestore.GeoPoint(12, 12))
    c.setSlotStatus(1,False)
