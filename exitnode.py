from errno import ENETUNREACH
import RPi.GPIO as GPIO
import time
import os
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from cloudconnect import Cloud
from ultrasonic import Ultrasonic
from led import Led
from camera import Camera
import pytz
import datetime
from parkingprice import calculate_parking_price
from licenseplate import LicensePlate
from buzzer import Buzzer

# Exit Node is the node with the camera at the EXIT GATE OF THE PARKING AREA

# MINIMUM DISTANCE FOR THE ULTRASONIC SENSOR TO DETECT THE VEHICLE
THRESHOLD_DISTANCE = 40
# WAIT TIME FOR THE SENSOR TO WAIT FOR THE OBJECT TO NOT MOVE
WAIT_TIME = 3
# REPEAT CHECK IF THE DISTANCE OF THE OBJECT REMAINS THE SAME FOR SOME NUMBER OF TIMES
REPEAT_DISTANCE_CHECKS = 2

# Area ID in which the parking node is deployed
AREA_ID = '1'
# COORDINATES of Area
AREA_COORDINATES = [10, 12]

# Indian time zone
IST = pytz.timezone('Asia/Kolkata')

# LED PINS
LED_PIN1 = 1
LED_PIN2 = 1
LED_PIN3 = 1

# BUZZER PINS
BUZZER_PIN1 = 1
BUZZER_PIN2 = 1
BUZZER_PIN3 = 1

# SERVO PIN
SERVO_PIN = 22


# ULTRASONIC SENSOR PINS
TRIGGER_PIN1 = 4
ECHO_PIN1 = 27


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    # Initialize Entry Sensor
    exitUltrasonicSensor = Ultrasonic(TRIGGER_PIN1, ECHO_PIN1)
    ####################################
    # Initialize camera object
    FileName = 'image.jpg'
    cam = Camera(FileName)
    ######################################
    # Initialize Cloud
    cloudfirestore = Cloud(
        'smartparkingsystem-5ffb7-2f4717e68ead.json', AREA_ID, AREA_COORDINATES)
    ###################################################################################
    # Initialize Servo
    factory = PiGPIOFactory()
    servo = Servo(SERVO_PIN, pin_factory=factory)
    servo.min()
    ###################################################################################

    # Car detection at EXIT GATE infinite loop
    while(True):
        # get Distance of car from exit parking booth
        car_distance = exitUltrasonicSensor.getDistance()
        time.sleep(WAIT_TIME)
        ##########################################
        # Object Detect Flag
        flag = 0

        # Check if object is a waiting car
        for i in range(1, REPEAT_DISTANCE_CHECKS):
            car_distance = exitUltrasonicSensor.getDistance()
            time.sleep(1)
            if(car_distance > THRESHOLD_DISTANCE):
                flag = 1
                break
        ##########################################

        # Object was not a waiting car
        if(flag == 1):
            continue

        # Object was a car waiting at EXIT GATE
        cam.capture()
        lp = LicensePlate(FileName)
        registration_no = lp.getLicensePlateNumber()

        if(registration_no == None):
            # OPTION-> ADD BUZZER TO SEND THE STRAY OBJECT AWAY FROM PARKING AREA
            continue

        # Valid License plate number is acquired from cloud compute
        res = cloudfirestore.searchRegistrationNumber(registration_no)

        if(res == None):
            # CAR NUMBER PLATE DIDNT MATCH ANY CAR IN THE DATABASE
            pass
        slot_no = res[0]
        entry_time = res[1]

        exit_time = datetime.datetime.now(IST)
        total_parking_time = exit_time-entry_time

        total_parking_time = str(total_parking_time)
        total_parking_time = total_parking_time.split(' days, ')

        price = 0

        if(len(total_parking_time) == 1):
            # time in hours,mins,seconds format
            total_parking_time = str(total_parking_time).split(':')
            days = 0
            hours = int(total_parking_time[0])
            minutes = int(total_parking_time[1])
            price = calculate_parking_price(days, hours, minutes)
        else:
            # time in date,hours,mins,seconds format
            days = int(total_parking_time[0])
            timex = total_parking_time[1].split(':')
            hours = int(timex[0])
            minutes = int(timex[1])
            price = calculate_parking_price(days, hours, minutes)

        print(price)
        servo.max()
        exit_barricade_distance=0
        while(exit_barricade_distance<=THRESHOLD_DISTANCE):
            exit_barricade_distance = exitUltrasonicSensor.getDistance()
            time.sleep(2)

        # Open the EXIT BARRICADE
        servo.min()
        time.sleep(2)
    #####################################################
