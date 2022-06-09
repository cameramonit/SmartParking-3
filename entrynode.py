import RPi.GPIO as GPIO
import time
import os
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from cloudconnect import Cloud
from ultrasonic import Ultrasonic
from led import Led
from camera import Camera
from licenseplate import LicensePlate
from buzzer import Buzzer

# Entry Node is the node with the camera at the ENTRY GATE OF THE PARKING AREA

# MINIMUM DISTANCE FOR THE ULTRASONIC SENSOR TO DETECT THE VEHICLE
THRESHOLD_DISTANCE=20
# WAIT TIME FOR THE SENSOR TO WAIT FOR THE OBJECT TO NOT MOVE 
WAIT_TIME=3
# REPEAT CHECK IF THE DISTANCE OF THE OBJECT REMAINS THE SAME FOR SOME NUMBER OF TIMES
REPEAT_DISTANCE_CHECKS=2

#Area ID in which the parking node is deployed
AREA_ID='1'
#COORDINATES of Area 
AREA_COORDINATES=[10,12]

#LED PINS
LED_PIN1 = 1
LED_PIN2 = 1
LED_PIN3 = 1

#BUZZER PINS
BUZZER_PIN1 = 1
BUZZER_PIN2 = 1
BUZZER_PIN3 = 1

#SERVO PIN
SERVO_PIN = 22


#ULTRASONIC SENSOR PINS
TRIGGER_PIN1 = 4
ECHO_PIN1 = 27


if __name__ == '__main__':    
    GPIO.setmode(GPIO.BCM)

    #Initialize Entry Sensor
    entryUltrasonicSensor=Ultrasonic(TRIGGER_PIN1,ECHO_PIN1)
    ####################################
    #Initialize camera object
    FileName='image.jpg'
    cam=Camera(FileName)
    ######################################
    #Initialize Cloud
    cloudfirestore=Cloud('smartparkingsystem-5ffb7-2f4717e68ead.json',AREA_ID,AREA_COORDINATES)
    ###################################################################################
    #Initialize Servo 
    #factory = PiGPIOFactory()
    #servo = Servo(SERVO_PIN, pin_factory=factory)
    #servo.min()
    ###################################################################################


    #Car detection at ENTRY GATE infinite loop 
    while(True):
        # get Distance of car from entry parking booth
        car_distance=entryUltrasonicSensor.getDistance()
        print(car_distance)
        time.sleep(WAIT_TIME)
        if(car_distance==-1):
            print('Ultrasonic Error')
            time.sleep(2)
            continue
        ##########################################
        #Object Detect Flag
        flag=0

        #Check if object is a waiting car
        for i in range(1,REPEAT_DISTANCE_CHECKS):
            car_distance=entryUltrasonicSensor.getDistance()
            print(car_distance)
            time.sleep(1)
            if(car_distance>THRESHOLD_DISTANCE):
                flag=1
                break
        ##########################################
            
        #Object was not a waiting car
        if(flag==1):
            continue

        #Object was a car waiting at Front GATE
        cam.capture()
        lp=LicensePlate(FileName)
        registration_no=lp.getLicensePlateNumber()
        print(registration_no)

        if(registration_no==None):
            #OPTION-> ADD BUZZER TO SEND THE STRAY OBJECT AWAY FROM PARKING AREA
            continue

        #Valid License plate number is acquired from cloud compute
        #Get the free parking slot from the Cloud database 
        free_slot_number=cloudfirestore.getFreeSlot()
        print(free_slot_number)

        #FREE PARKING SLOT AVAILABLE
        if free_slot_number!=-1:
            cloudfirestore.assignSlot(free_slot_number,registration_no)
            #servo.max()
            car_dist=-1e9

            #WAIT TILL THE CAR ENTERS THE FRONT GATE
            while(car_dist<THRESHOLD_DISTANCE):
                car_dist=entryUltrasonicSensor.getDistance()
                time.sleep(2)
            time.sleep(2)
            #CLOSE THE BARRICADE
            #servo.min()

        #FREE PARKING SLOT NOT AVAILABLE
        else:
            print('NO FREE PARKING SLOT AVAILABLE')
        
    #####################################################
    