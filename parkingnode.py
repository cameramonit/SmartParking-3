import RPi.GPIO as GPIO
import time
import os
from cloudconnect import Cloud
from ultrasonic import Ultrasonic
from led import Led
from buzzer import Buzzer

#Parking Node is the node at the parking slot

#Area ID in which the parking node is deployed
AREA_ID='1'
#COORDINATES of Area 
AREA_COORDINATES=[10,12]

# MINIMUM DISTANCE FOR THE ULTRASONIC SENSOR TO DETECT THE VEHICLE
THRESHOLD_DISTANCE=10


#LED PINS
LED_PIN1 = 1
LED_PIN2 = 1
LED_PIN3 = 1
#BUZZER PINS
BUZZER_PIN1 = 1
BUZZER_PIN2 = 1
BUZZER_PIN3 = 1

#FIRST ULTRASONIC SENSOR
TRIGGER_PIN1 = 1
ECHO_PIN1 = 1
#SECOND ULTRASONIC SENSOR
TRIGGER_PIN2 = 1
ECHO_PIN2 = 1
#THIRD ULTRASONIC SENSOR
TRIGGER_PIN3 = 1
ECHO_PIN3 = 1

#NUMBER OF SLOTS
FIRST_SLOT_NO = 1
LAST_SLOT_NO = 3

if __name__ == '__main__':    
    GPIO.setmode(GPIO.BCM)
    #INITIALIZE CLOUD 
    cloudfirestore=Cloud('smartparkingsystem-5ffb7-2f4717e68ead.json',AREA_ID,AREA_COORDINATES)
    ################################################################################
    ultrasonicArray=[]
    ultrasonicArray.append(Ultrasonic(TRIGGER_PIN1,ECHO_PIN1))
    ultrasonicArray.append(Ultrasonic(TRIGGER_PIN2,ECHO_PIN2))
    ultrasonicArray.append(Ultrasonic(TRIGGER_PIN3,ECHO_PIN3))

    cnt=0

    for i in ultrasonicArray:
        cnt+=1

        #GET THE VEHICLE DISTANCE FROM THE SLOT
        dist=i.getDistance()

        slotStaus:bool
        #CHECK IF THE VEHICLES ARE IN THE PARKING SLOTS

        #if object is present
        if(dist<THRESHOLD_DISTANCE):
            slotStaus=False
        else:
            slotStaus=True

        cloudfirestore.setSlotStatus(cnt,slotStaus)