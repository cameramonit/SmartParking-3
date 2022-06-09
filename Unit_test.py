import RPi.GPIO as GPIO
import time
import os
from cloudconnect import Cloud
from ultrasonic import Ultrasonic
from led import Led
from camera import Camera
from licenseplate import LicensePlate
from buzzer import Buzzer

def cameraTest():
    pass
def ultrasonicTest():
    pass
def ledTest():
    pass
def servoTest():
    pass
def buzzerTest():
    pass
def parkingPriceTest():
    pass
def licensePlateTest():
    pass
def cloudConnectTest():
    pass

if __name__ == '__main__':    
    GPIO.setmode(GPIO.BCM)
    while(True):
        choice=0
        print('Enter the component to test')
        print('1: Camera 2: Ultrasonic')
        print('3: Led 4: Servo')
        print('5: Buzzer 6: ParkingPrice')
        print('7: LicensePlate 8: Cloud')
        print('9: ExitTest')
        try:
            choice=int(input())
        except:
            print('Input Error')
            time.sleep(3)
            os.system('clear')
            continue;
        if(choice==1):
            pass
        elif(choice==2):
            pass
        elif(choice==3):
            pass
        elif(choice==4):
            pass
        elif(choice==5):
            pass
        elif(choice==6):
            pass
        elif(choice==7):
            pass
        elif(choice==8):
            pass
        elif(choice==9):
            exit()
