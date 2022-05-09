import RPi.GPIO as GPIO
import time
import os
from cloudconnect import cloud
from ultrasonic import Ultrasonic
from led import Led
from camera import Camera
from licenseplate import LicensePlate
from buzzer import Buzzer



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
    u=Ultrasonic(12,13)
    
