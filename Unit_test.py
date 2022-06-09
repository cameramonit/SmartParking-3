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
    c=Camera('image.jpg')
    c.capture()
    
def ultrasonicTest():
    print('Enter Trigger Pin Number')
    t=int(input())
    print('Enter Echo Pin Number')
    e=int(input())
    us=Ultrasonic(t,e)
    dis=us.getDistance()
    if(dis==-1):
        raise Exception('Ultrasonic Connection Loose')
    print('Distance'+dis)
    
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
        os.system('clear')
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
            try:
                cameraTest()
            except:
                print('TestFailed')
                continue;
            print('TestPassed')
        elif(choice==2):
            try:
                ultrasonicTest()
            except:
                print('TestFailed')
                continue;
            print('TestPassed')
        elif(choice==3):
            try:
                
            except:
                print('TestFailed')
                continue;
            print('TestPassed')
        elif(choice==4):
            try:
                
            except:
                print('TestFailed')
                continue;
            print('TestPassed')
        elif(choice==5):
            try:
                
            except:
                print('TestFailed')
                continue;
            print('TestPassed')
        elif(choice==6):
            try:
                
            except:
                print('TestFailed')
                continue;
            print('TestPassed')
        elif(choice==7):
            try:
                
            except:
                print('TestFailed')
                continue;
            print('TestPassed')
        elif(choice==8):
            try:
                
            except:
                print('TestFailed')
                continue;
            print('TestPassed')
        elif(choice==9):
            exit()
