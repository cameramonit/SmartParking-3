#sudo pigpiod
from gpiozero import Servo
from time import sleep
import os
from gpiozero.pins.pigpio import PiGPIOFactory


#Tests
os.system('sudo pigpiod')
factory = PiGPIOFactory()

servo = Servo(21, pin_factory=factory)


print("Go to max")
servo.max()
sleep(1)
print("And back to middle")
servo.mid()
sleep(0.1)
#servo.value = None