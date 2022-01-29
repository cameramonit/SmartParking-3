from picamera import PiCamera
import os


class Camera:
    IMAGE_NAME = 'image'
    camera = 1

    def __init__(self, PATH_TO_IMAGE):
        self.PATH_TO_IMAGE = PATH_TO_IMAGE
        self.camera = PiCamera()
        self.camera.rotation = 180
    def __init(self):
        self.camera=PiCamera()
        self.camera.rotation=180

    def capture(self):
        self.camera.capture(output=self.IMAGE_NAME,format='jpeg')

    def capure(self,OUTPUT):
        self.camera.capture(output=OUTPUT,format='jpeg')
