from picamera import PiCamera
import os


class Camera:
    FileName = 'image.jpg'
    camera = None

    def __init__(self, FileName):
        '''def __init__(self, PATH_TO_IMAGE):'''
        '''self.PATH_TO_IMAGE = PATH_TO_IMAGE'''
        self.PATH_TO_IMAGE=os.getcwd()+'/'+FileName
        self.camera = PiCamera()
        self.camera.rotation = 180

    def capture(self):
        self.camera.capture(self.PATH_TO_IMAGE)


#Tests
#c=Camera('image.jpg')
#c.capture()
