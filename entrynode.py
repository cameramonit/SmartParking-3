import RPi.GPIO as GPIO
import time
import os
from cloudconnect import Cloud
from ultrasonic import Ultrasonic
from led import Led
from camera import Camera
from licenseplate import LicensePlate
from buzzer import Buzzer

# Entry Node is the node with the camera 

THRESHOLD_DISTANCE=40
WAIT_TIME=3
REPEAT_DISTANCE=2

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

    #Initialize Entry Sensor
    entrySensor=Ultrasonic(1,2)

    #Initialize camera object
    FileName='image.jpg'
    cam=Camera(FileName)

    #Initialize Cloud
    cloudfirestore=Cloud('smartparkingsystem-5ffb7-2f4717e68ead.json')

    #Car detecting infinite loop 
    while(True):
        # Distance of car from entry parking booth
        car_distance=entrySensor.getDistance()
        time.sleep(WAIT_TIME)
        #Object Detect Flag
        flag=0
        #Check if object is a waiting car
        for i in range(1,REPEAT_DISTANCE):
            car_distance=entrySensor.getDistance()
            time.sleep(1)
            if(car_distance>THRESHOLD_DISTANCE):
                flag=1
                break
            
        #Object was not a waiting car
        if(flag==1):
            continue
        cam.capture()
        lp=LicensePlate(FileName)
        registration_no=lp.getLicensePlateNumber()
        if(registration_no==None):
            continue
        

        

    
