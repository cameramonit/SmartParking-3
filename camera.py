from picamera import PiCamera
import os


class Camera:
    PATH_TO_IMAGE = '/home'
    camera = 1

    def __init__(self, PATH_TO_IMAGE):
        self.PATH_TO_IMAGE = PATH_TO_IMAGE
        self.camera = PiCamera()
        self.camera.rotation = 180

    def capture(self):
        self.camera.capture(self.PATH_TO_IMAGE)

    def __del__(self):
        self.camera.close()
