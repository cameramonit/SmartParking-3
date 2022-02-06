from picamera import PiCamera
import os


class Camera:
    IMAGE_NAME = 'image.jpeg'
    camera = 1
    Height=500
    Width=500

    def __init__(self, IMAGE_NAME,Height,Width):
        self.IMAGE_NAME = IMAGE_NAME
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution=(Height,Width)
        
    def __init(self):
        self.camera=PiCamera()
        self.camera.rotation=180
        self.camera.resolution=(self.Height,self.Width)
        
    def __init(self,IMAGE_NAME):
        self.IMAGE_NAME = IMAGE_NAME
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution=(self.Height,self.Width)
        
    def capture(self):
        self.camera.capture(output=self.IMAGE_NAME,format='jpeg')

    def capure(self,OUTPUT):
        self.camera.capture(output=OUTPUT,format='jpeg')
