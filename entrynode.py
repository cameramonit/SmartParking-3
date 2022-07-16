import RPi.GPIO as GPIO
import time
import os
from gpiozero import Servo
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from gpiozero.pins.pigpio import PiGPIOFactory
from cloudconnect import Cloud
from ultrasonic import Ultrasonic
from led import Led
from camera import Camera
from licenseplate import LicensePlate
from buzzer import Buzzer

# Entry Node is the node with the camera at the ENTRY GATE OF THE PARKING AREA

# MAXIMUM DISTANCE FOR THE ULTRASONIC SENSOR TO DETECT THE VEHICLE
THRESHOLD_DISTANCE=14
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
SERVO_PIN = 21


#ULTRASONIC SENSOR PINS
TRIGGER_PIN1 = 4
ECHO_PIN1 = 27

ser=False

if __name__ == '__main__':    
    GPIO.setmode(GPIO.BCM)
    RST = None     # on the PiOLED this pin isnt used
    # Note the following are only used with SPI:
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0

    
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

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
    

    # Load default font.
    font = ImageFont.load_default()
    draw.rectangle((0,0,width,height), outline=0, fill=0)
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
    if ser:
        factory = PiGPIOFactory()
        servo = Servo(SERVO_PIN, pin_factory=factory)
        servo.min()
    ###################################################################################


    #Car detection at ENTRY GATE infinite loop 
    while(True):
        # get Distance of car from entry parking booth
        font=ImageFont.truetype('arial.ttf',15)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x+5, top),       'SMART',  font=font, fill=255)
        draw.text((x+25, top+10),       'PARKING',  font=font, fill=255)
        draw.text((x+55, top+20),       'SYSTEM',  font=font, fill=255)
        disp.image(image)
        disp.display()
        
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
        font=ImageFont.truetype('arial.ttf',14)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),       'REG_NO: '+str(registration_no),  font=font, fill=255)
        disp.image(image)
        disp.display()
        
        if(registration_no==None):
            #OPTION-> ADD BUZZER TO SEND THE STRAY OBJECT AWAY FROM PARKING AREA
            print('Registration number NONE')
            font=ImageFont.truetype('arial.ttf',11)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((x, top+20),       'CAR NOT DETECTED',  font=font, fill=255)
            disp.image(image)
            disp.display()
            time.sleep(10)
            continue


        #Check if a slot is assigned for the vehicle
        datareg=cloudfirestore.searchRegistrationNumber(registration_no)
        if(datareg!=None):
            #WAIT TILL THE CAR ENTERS THE FRONT GATE
            while(car_dist<THRESHOLD_DISTANCE):
                car_dist=entryUltrasonicSensor.getDistance()
                print(car_dist)
                time.sleep(2)
            time.sleep(2)
            #CLOSE THE BARRICADE
            if ser:
                servo.mid()
            


        #Valid License plate number is acquired from cloud compute
        #Get the free parking slot from the Cloud database 
        free_slot_number=cloudfirestore.getFreeSlot()
        print(free_slot_number)
        
        if free_slot_number!=-1:            
            font=ImageFont.truetype('arial.ttf',14)
            draw.text((x, top+20),'SLOT NO: '+str(free_slot_number),  font=font, fill=255)
            disp.image(image)
            disp.display()
            
        

        #FREE PARKING SLOT AVAILABLE
        if free_slot_number!=-1:
            cloudfirestore.assignSlot(free_slot_number,registration_no)
            if ser:
                servo.max()
            car_dist=-1e9

            #WAIT TILL THE CAR ENTERS THE FRONT GATE
            while(car_dist<THRESHOLD_DISTANCE):
                car_dist=entryUltrasonicSensor.getDistance()
                print(car_dist)
                time.sleep(2)
            time.sleep(2)
            #CLOSE THE BARRICADE
            if ser:
                servo.mid()

        #FREE PARKING SLOT NOT AVAILABLE
        else:
            print('NO FREE PARKING SLOT AVAILABLE')
            ont=ImageFont.truetype('arial.ttf',12)
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((x+5, top), 'SLOT',  font=font, fill=255)
            draw.text((x+25, top+10), 'NOT',  font=font, fill=255)
            draw.text((x+45, top+20), 'AVAILABLE',  font=font, fill=255)
            disp.image(image)
            disp.display()
            
            while(free_slot_number==-1):
                free_slot_number=cloudfirestore.getFreeSlot()
                print('check free slot availability')
                time.sleep(3)
            
    #####################################################
    