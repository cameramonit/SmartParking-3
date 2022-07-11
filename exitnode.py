from errno import ENETUNREACH
import RPi.GPIO as GPIO
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from cloudconnect import Cloud
from ultrasonic import Ultrasonic
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from led import Led
from camera import Camera
import pytz
import datetime
from parkingprice import calculate_parking_price
from licenseplate import LicensePlate
from buzzer import Buzzer

RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0


# Exit Node is the node with the camera at the EXIT GATE OF THE PARKING AREA

# MINIMUM DISTANCE FOR THE ULTRASONIC SENSOR TO DETECT THE VEHICLE
THRESHOLD_DISTANCE = 15
# WAIT TIME FOR THE SENSOR TO WAIT FOR THE OBJECT TO NOT MOVE
WAIT_TIME = 3
# REPEAT CHECK IF THE DISTANCE OF THE OBJECT REMAINS THE SAME FOR SOME NUMBER OF TIMES
REPEAT_DISTANCE_CHECKS = 3

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
SERVO_PIN = 21


# ULTRASONIC SENSOR PINS
TRIGGER_PIN1 = 14
ECHO_PIN1 = 15

ser=False

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
    # Initialize library.
    disp.begin()
    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
    
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
    if ser:        
        factory = PiGPIOFactory()
        servo = Servo(SERVO_PIN, pin_factory=factory)
        servo.mid()
    ###################################################################################

    # Car detection at EXIT GATE infinite loop
    while(True):
        font=ImageFont.truetype('arial.ttf',12)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x+5, top),       'SMART',  font=font, fill=255)
        draw.text((x+25, top+10),       'PARKING',  font=font, fill=255)
        draw.text((x+55, top+20),       'SYSTEM',  font=font, fill=255)
        disp.image(image)
        disp.display()
        
        disp.image(image)
        disp.display()
        
        car_distance = exitUltrasonicSensor.getDistance()
        time.sleep(WAIT_TIME)
        print(car_distance)
        ##########################################
        # Object Detect Flag
        flag = 0

        # Check if object is a waiting car
        for i in range(0, REPEAT_DISTANCE_CHECKS):
            car_distance = exitUltrasonicSensor.getDistance()
            print(car_distance)
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
        print(registration_no)
        fontsize=15
        font = ImageFont.truetype('arial.ttf',fontsize)
    
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),       'REG_NO: '+str(registration_no),  font=font, fill=255)
        disp.image(image)
        disp.display()
        if(registration_no == None):
            # OPTION-> ADD BUZZER TO SEND THE STRAY OBJECT AWAY FROM PARKING AREA
            continue

        # Valid License plate number is acquired from cloud compute
        res = cloudfirestore.searchRegistrationNumber(registration_no)

        if(res == None):
            # CAR NUMBER PLATE DIDNT MATCH ANY CAR IN THE DATABASE
            
            #draw.rectangle((0,0,width,height), outline=0, fill=0)
            font=ImageFont.truetype('arial.ttf',15)
            draw.text((x, top+20),       "CAR NOT FOUND",  font=font, fill=255)
            disp.image(image)
            disp.display()
            print('Car Not found')
            exit_barricade_distance=exitUltrasonicSensor.getDistance()
            while(exit_barricade_distance<=THRESHOLD_DISTANCE):
            
                exit_barricade_distance = exitUltrasonicSensor.getDistance()
            
                time.sleep(3)
            
            continue
            
        slot_no = res[0]
        entry_time = res[1]

        exit_time = datetime.datetime.now(IST)
        total_parking_time = exit_time-entry_time

        total_parking_time = str(total_parking_time)
        total_parking_time = total_parking_time.split(' days, ')
            
        price = 0
        print(total_parking_time)
        if(len(total_parking_time) == 1):
            # time in hours,mins,seconds format
            total_parking_time = str(total_parking_time[0]).split(':')    
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
        print('Parking Price')
        print(price)
            
        exit_barricade_distance=0
        paid=False

        cloudfirestore.setPaymentInfo(registration_no,entry_time,exit_time,price)
        
        while(not paid):
            paid=cloudfirestore.isPaymentComplete()
            time.sleep(2)
        
        if ser:
            print('Open Barricade')
            servo.max()
            
        print('Parking Payment Complete')
        while(exit_barricade_distance<=THRESHOLD_DISTANCE):
            
            exit_barricade_distance = exitUltrasonicSensor.getDistance()
            
            time.sleep(3)
        cloudfirestore.clearSlot(slot_no)
        # Open the EXIT BARRICADE
        if ser:
            servo.mid()
        time.sleep(2)
    #####################################################
